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
        # Keresünk egy "Characters:" szekciót
        char_pattern = r'Characters?:\s*\n((?:•|\*|-|\d+\.)\s*.+\n?)+'
        match = re.search(char_pattern, content, re.MULTILINE | re.IGNORECASE)
        
        if match:
            char_section = match.group(1)
            # Minden szereplő egy sorban van
            char_lines = re.findall(r'[•\*\-\d\.]\s*(.+?)\s*[–—-]\s*(.+)', char_section)
            
            for name, description in char_lines:
                self.characters[name.strip()] = description.strip()
    
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
        
        # Párbeszéd formátum: "Szereplő: Szöveg"
        dialogue_pattern = r'^([A-Za-z]+):\s*(.+)$'
        
        lines = slide_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.lower() == 'dialogue:':
                continue
            
            match = re.match(dialogue_pattern, line)
            if match:
                character = match.group(1).strip()
                text = match.group(2).strip()
                
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
