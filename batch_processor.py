"""
Batch feldolgozó modul
Feladata: Több forgatókönyv fájl automatikus feldolgozása.
"""

import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from script_parser import ScriptParser
from docx_parser import DocxParser
from voice_manager import VoiceManager
from tts_generator import TTSGenerator


class BatchProcessor:
    """
    Batch feldolgozó osztály.
    Több forgatókönyv fájlt dolgoz fel egyszerre.
    """
    
    def __init__(self, 
                 input_dir: str, 
                 output_base_dir: str = "batch_output",
                 api_key: str = None):
        """
        Inicializálja a batch processort.
        
        Args:
            input_dir: Input mappa, ahol a forgatókönyv fájlok vannak
            output_base_dir: Alap output mappa
            api_key: ElevenLabs API kulcs
        """
        self.input_dir = Path(input_dir)
        self.output_base_dir = Path(output_base_dir)
        self.api_key = api_key
        
        # Output mappa létrehozása
        self.output_base_dir.mkdir(exist_ok=True)
        
        self.results = []
        self.total_files = 0
        self.processed_files = 0
        self.failed_files = []
    
    def find_script_files(self) -> List[Path]:
        """
        Megkeresi az összes támogatott forgatókönyv fájlt az input mappában.
        
        Returns:
            List[Path]: Fájlok listája
        """
        supported_extensions = ['.txt', '.docx']
        files = []
        
        for ext in supported_extensions:
            files.extend(self.input_dir.glob(f'*{ext}'))
        
        # Név szerint rendezés
        files.sort()
        
        return files
    
    def create_output_directory(self, script_name: str) -> Path:
        """
        Létrehoz egy output mappát egy forgatókönyvhöz.
        
        Args:
            script_name: Forgatókönyv neve (fájlnév kiterjesztés nélkül)
            
        Returns:
            Path: Output mappa elérési útja
        """
        # Biztonságos mappanév (speciális karakterek eltávolítása)
        safe_name = "".join(c for c in script_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        
        output_dir = self.output_base_dir / safe_name
        output_dir.mkdir(exist_ok=True)
        
        return output_dir
    
    def process_single_file(self, 
                           file_path: Path, 
                           voice_manager: VoiceManager,
                           custom_mappings: Optional[Dict] = None) -> Dict:
        """
        Feldolgoz egy forgatókönyv fájlt.
        
        Args:
            file_path: Forgatókönyv fájl elérési útja
            voice_manager: VoiceManager instance
            custom_mappings: Egyedi hang párosítások (opcionális)
            
        Returns:
            Dict: Feldolgozás eredménye
        """
        result = {
            'file': str(file_path),
            'name': file_path.stem,
            'success': False,
            'error': None,
            'dialogues_count': 0,
            'generated_count': 0,
            'output_dir': None
        }
        
        try:
            print(f"\n{'='*60}")
            print(f"📄 Feldolgozás: {file_path.name}")
            print(f"{'='*60}\n")
            
            # Parser választás a fájltípus alapján
            if file_path.suffix.lower() == '.docx':
                parser = DocxParser(str(file_path))
            else:
                parser = ScriptParser(str(file_path))
            
            # Forgatókönyv feldolgozása
            parser_data = parser.parse()
            
            # Metaadatok kiírása
            print(f"📌 Forgatókönyv: {parser_data['metadata'].get('title', file_path.stem)}")
            print(f"👥 Szereplők: {len(parser_data['characters'])}")
            print(f"🎬 Jelenetek: {len(parser_data['scenes'])}")
            
            # Hangprofilok hozzárendelése
            if custom_mappings:
                for char, profile in custom_mappings.items():
                    if char in parser_data['characters']:
                        voice_manager.custom_mappings[char] = profile
            
            for character, description in parser_data['characters'].items():
                voice_manager.assign_voice_by_description(character, description)
            
            # Output mappa létrehozása
            output_dir = self.create_output_directory(file_path.stem)
            result['output_dir'] = str(output_dir)
            
            print(f"📁 Output mappa: {output_dir}")
            
            # Párbeszédek előkészítése
            dialogues = parser.get_all_dialogues()
            result['dialogues_count'] = len(dialogues)
            
            if not dialogues:
                raise Exception("Nincs párbeszéd a forgatókönyvben!")
            
            print(f"💬 Párbeszédek: {len(dialogues)}\n")
            
            # TTS generálás
            tts_generator = TTSGenerator(self.api_key, str(output_dir))
            generated_results = tts_generator.generate_batch(
                dialogues, 
                voice_manager, 
                delay=0.5
            )
            
            # Sikeres generálások száma
            result['generated_count'] = sum(1 for r in generated_results if r['success'])
            
            # JSON és CSV mentés
            json_path = output_dir / "dialogues.json"
            csv_path = output_dir / "dialogues.csv"
            mappings_path = output_dir / "voice_mappings.json"
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(generated_results, f, ensure_ascii=False, indent=2)
            
            self._save_csv(generated_results, csv_path)
            
            with open(mappings_path, 'w', encoding='utf-8') as f:
                json.dump(voice_manager.get_all_mappings(), f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Sikeres feldolgozás!")
            print(f"   Generált hangok: {result['generated_count']}/{result['dialogues_count']}")
            
            result['success'] = True
            
        except Exception as e:
            print(f"\n❌ Hiba: {e}")
            result['error'] = str(e)
            self.failed_files.append(str(file_path))
        
        return result
    
    def process_all(self, custom_mappings: Optional[Dict] = None) -> Dict:
        """
        Feldolgozza az összes forgatókönyv fájlt az input mappában.
        
        Args:
            custom_mappings: Egyedi hang párosítások (opcionális)
            
        Returns:
            Dict: Batch feldolgozás összesített eredménye
        """
        files = self.find_script_files()
        self.total_files = len(files)
        
        if self.total_files == 0:
            print(f"❌ Nincs forgatókönyv fájl a mappában: {self.input_dir}")
            print("   Támogatott formátumok: .txt, .docx")
            return {'success': False, 'error': 'No files found'}
        
        print(f"\n🎬 BATCH FELDOLGOZÁS INDÍTÁSA")
        print(f"{'='*60}")
        print(f"📂 Input mappa: {self.input_dir}")
        print(f"📁 Output mappa: {self.output_base_dir}")
        print(f"📄 Talált fájlok: {self.total_files}")
        print(f"{'='*60}\n")
        
        # Megerősítés kérése
        confirmation = input(f"⚠️  {self.total_files} fájl feldolgozása kezdődik. Folytatod? (i/n): ").strip().lower()
        
        if confirmation != 'i':
            print("❌ Megszakítva.")
            return {'success': False, 'cancelled': True}
        
        # Voice manager létrehozása
        voice_manager = VoiceManager(custom_mappings)
        
        # Fájlok feldolgozása
        for i, file_path in enumerate(files, 1):
            print(f"\n[{i}/{self.total_files}] ", end="")
            
            result = self.process_single_file(file_path, voice_manager, custom_mappings)
            self.results.append(result)
            
            if result['success']:
                self.processed_files += 1
            
            # Voice manager tisztítása a következő fájlhoz
            voice_manager.character_voice_map.clear()
        
        # Összesítő jelentés mentése
        self._save_summary()
        
        return {
            'success': True,
            'total_files': self.total_files,
            'processed': self.processed_files,
            'failed': len(self.failed_files),
            'results': self.results
        }
    
    def _save_csv(self, data: list, output_path: Path):
        """Menti a párbeszédeket CSV formátumban."""
        if not data:
            return
        
        fieldnames = ['scene', 'slide_number', 'character', 'text', 'voice_id', 'file_name', 'success']
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in data:
                csv_row = {key: row.get(key, '') for key in fieldnames}
                writer.writerow(csv_row)
    
    def _save_summary(self):
        """Mentse az összesített jelentést."""
        summary_path = self.output_base_dir / "batch_summary.json"
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'input_directory': str(self.input_dir),
            'output_directory': str(self.output_base_dir),
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'failed_files': self.failed_files,
            'results': self.results
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Összesítő jelentés mentve: {summary_path}")
