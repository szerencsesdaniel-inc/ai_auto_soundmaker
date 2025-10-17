"""
Forgatókönyv szöveg elemző modul
Feladata: A strukturálatlan szöveget feldolgozni és kinyerni a jeleneteket, 
szereplőket és párbeszédeket.
"""

import re
from typing import List, Dict, Optional


class ScriptParser:
    """
    Oktatási forgatókönyv parser osztály.
    Felismeri a slide-okat, szereplőket és párbeszédeket.
    """
    
    def __init__(self, script_path: str):
        """
        Inicializálja a parsert egy forgatókönyv fájl elérési útjával.
        
        Args:
            script_path: A forgatókönyv fájl elérési útja (.txt vagy .md)
        """
        self.script_path = script_path
        self.characters = {}  # Szereplők leírásaikkal
        self.metadata = {}    # Script metaadatok (cím, szint, stb.)
        self.scenes = []      # Jelenet lista
        
    def parse(self) -> Dict:
        """
        Feldolgozza a teljes forgatókönyvet és visszaadja a strukturált adatot.
        
        Returns:
            Dict: Strukturált adatok (metadata, characters, scenes)
        """
        with open(self.script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Metaadatok kinyerése (első sorok)
        self._extract_metadata(content)
        
        # Szereplők kinyerése
        self._extract_characters(content)
        
        # Jelenetek és párbeszédek kinyerése
        self._extract_scenes(content)
        
        return {
            'metadata': self.metadata,
            'characters': self.characters,
            'scenes': self.scenes
        }
    
    def _extract_metadata(self, content: str):
        """Kinyeri a metaadatokat (cím, alcím, szint)."""
        lines = content.split('\n')
        
        # Első nem-üres sorok általában a metaadatok
        for line in lines[:10]:
            line = line.strip()
            if not line:
                continue
                
            # Szint felismerése
            if line.lower().startswith('level:'):
                self.metadata['level'] = line.split(':', 1)[1].strip()
            # Cím (számmal kezdődik)
            elif re.match(r'^\d+', line) and 'title' not in self.metadata:
                self.metadata['title'] = line
            # Alcím (számmal és gondolatjellel)
            elif '–' in line or '—' in line:
                self.metadata['subtitle'] = line
    
    def _extract_characters(self, content: str):
        """Kinyeri a szereplőket és leírásukat."""
        # Keresünk egy "Characters:" szekciót (több variáció)
        char_patterns = [
            r'Characters?:\s*\n((?:•|\*|-|\d+\.)\s*.+\n?)+',  # Lista formátum
            r'Characters?:\s*(.+?)(?:\n\n|Slide|Scene)',      # Szabad szöveg formátum
        ]
        
        for pattern in char_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            
            if match:
                char_section = match.group(1)
                
                # TÖBB FORMÁTUM FELISMERÉSE:
                # 1. Bold formátum: "• **Tom:** 20 years old..."
                # 2. Sima formátum: "• Tom – 20 years old..."
                # 3. Gondolatjel formátum: "Tom - description"
                
                char_patterns_v2 = [
                    # Bold + kettőspont: "**Tom:** description" vagy "Tom: description"
                    r'[•\*\-\d\.]*\s*\*{0,2}([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\*{0,2}\s*:\s*(.+?)(?=\n|$)',
                    # Gondolatjel: "Tom – description" vagy "Tom - description"
                    r'[•\*\-\d\.]*\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[–—-]\s*(.+?)(?=\n|$)',
                ]
                
                for cp in char_patterns_v2:
                    char_lines = re.findall(cp, char_section, re.MULTILINE)
                    
                    for name, description in char_lines:
                        # Tisztítás (bold ** jelek eltávolítása ha maradtak)
                        name_clean = name.replace('*', '').strip()
                        desc_clean = description.replace('*', '').strip()
                        
                        if name_clean and desc_clean:
                            self.characters[name_clean] = desc_clean
                    
                    if self.characters:
                        break
                
                if self.characters:
                    break  # Ha találtunk szereplőket, kilépünk
    
    def _extract_scenes(self, content: str):
        """Kinyeri a jeleneteket és a párbeszédeket."""
        # Slide-ok keresése (Slide 1, Slide 2, stb.)
        slide_pattern = r'Slide\s+(\d+)\s*\n'
        slides = list(re.finditer(slide_pattern, content))
        
        for i, slide_match in enumerate(slides):
            slide_num = slide_match.group(1)
            start_pos = slide_match.end()
            
            # A slide vége: következő slide kezdete vagy fájl vége
            if i + 1 < len(slides):
                end_pos = slides[i + 1].start()
            else:
                end_pos = len(content)
            
            slide_content = content[start_pos:end_pos]
            
            # Párbeszédek kinyerése ebből a slide-ból
            dialogues = self._extract_dialogues(slide_content)
            
            if dialogues:
                self.scenes.append({
                    'slide_number': int(slide_num),
                    'dialogues': dialogues
                })
    
    def _extract_dialogues(self, slide_content: str) -> List[Dict]:
        """
        Kinyeri a párbeszédeket egy slide szövegéből.
        
        Args:
            slide_content: Egy slide szövege
            
        Returns:
            List[Dict]: Párbeszéd lista (character, text)
        """
        dialogues = []
        
        # Kizáró lista - ezek NEM szereplők, hanem leíró szavak (ne generáljuk le!)
        EXCLUDED_KEYWORDS = [
            'scene', 'setting', 'location', 'context', 'dialogue', 
            'note', 'description', 'action', 'stage', 'background',
            'sound', 'music', 'time', 'place', 'situation'
        ]
        
        # Párbeszéd formátum: "Szereplő: Szöveg"
        dialogue_pattern = r'^([A-Za-z]+):\s*(.+)$'
        
        lines = slide_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = re.match(dialogue_pattern, line)
            if match:
                character = match.group(1).strip()
                text = match.group(2).strip()
                
                # Kiszűrjük a leíró sorokat (Scene:, Setting:, stb.)
                if character.lower() in EXCLUDED_KEYWORDS:
                    continue
                
                dialogues.append({
                    'character': character,
                    'text': text
                })
        
        return dialogues
    
    def get_all_dialogues(self) -> List[Dict]:
        """
        Visszaadja az összes párbeszédet sorszámozva és jelenet információval.
        
        Returns:
            List[Dict]: Teljes párbeszéd lista strukturálva
        """
        all_dialogues = []
        global_line_num = 1
        
        for scene in self.scenes:
            slide_num = scene['slide_number']
            
            for dialogue in scene['dialogues']:
                all_dialogues.append({
                    'scene': f"Slide {slide_num}",
                    'slide_number': slide_num,
                    'character': dialogue['character'],
                    'text': dialogue['text'],
                    'line_number': global_line_num
                })
                global_line_num += 1
        
        return all_dialogues
