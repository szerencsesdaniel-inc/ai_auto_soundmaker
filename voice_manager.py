"""
Hangprofil kezelő modul
Feladata: Szereplőkhöz hozzárendelni a megfelelő ElevenLabs hangprofilokat.
"""

from typing import Dict, Optional


class VoiceManager:
    """
    Hangprofil menedzser osztály.
    Szereplőkhöz rendeli a megfelelő ElevenLabs voice ID-kat.
    """
    
    # Előre definiált ElevenLabs voice ID-k
    # Ezek példa ID-k - helyettesítsd be a saját választott hangokkal!
    # A teljes hanglista: https://elevenlabs.io/voice-library
    
    VOICE_PROFILES = {
        # Női hangok
        'young_female_friendly': 'EXAVITQu4vr4xnSDxMaL',      # Sarah - soft, young
        'young_female_neutral': 'pNInz6obpgDQGcFmaJgB',       # Adam -> használható női helyett
        'elderly_female_cheerful': 'XB0fDUnXU5powFXDhCwa',    # Charlotte - warm, middle-aged
        'female_professional': 'ThT5KcBeYPX3keUQqHPh',        # Dorothy - pleasant
        
        # Férfi hangok  
        'male_young': 'pNInz6obpgDQGcFmaJgB',                 # Adam - neutral
        'male_elderly': 'yoZ06aMxZJJ28mfd3POQ',               # Sam - raspy, old
        'male_professional': 'VR6AewLTigWG4xSOukaG',          # Arnold - strong
        
        # Alapértelmezett
        'default': 'EXAVITQu4vr4xnSDxMaL'
    }
    
    def __init__(self, custom_mappings: Optional[Dict[str, str]] = None):
        """
        Inicializálja a voice managert.
        
        Args:
            custom_mappings: Egyedi szereplő -> voice_profile párosítások
        """
        self.custom_mappings = custom_mappings or {}
        self.character_voice_map = {}
    
    def assign_voice_by_description(self, character: str, description: str) -> str:
        """
        Automatikusan hozzárendel egy hangprofilt a leírás alapján.
        
        Args:
            character: Szereplő neve
            description: Szereplő leírása (pl. "friendly and polite")
            
        Returns:
            str: ElevenLabs voice ID
        """
        # Ha van egyedi mapping, azt használjuk
        if character in self.custom_mappings:
            profile = self.custom_mappings[character]
            voice_id = self.VOICE_PROFILES.get(profile, self.VOICE_PROFILES['default'])
            self.character_voice_map[character] = voice_id
            return voice_id
        
        # Automatikus felismerés kulcsszavak alapján
        description_lower = description.lower()
        
        # Kor szerinti felismerés
        is_young = any(word in description_lower for word in ['young', 'teenager', 'student', 'child'])
        is_elderly = any(word in description_lower for word in ['elderly', 'old', 'senior', 'grandmother', 'grandfather'])
        
        # Nem szerinti felismerés
        is_female = any(word in description_lower for word in ['lady', 'woman', 'girl', 'female', 'mother', 'sister'])
        is_male = any(word in description_lower for word in ['man', 'boy', 'male', 'father', 'brother'])
        
        # Hangulat
        is_cheerful = any(word in description_lower for word in ['cheerful', 'happy', 'jovial', 'upbeat'])
        is_friendly = any(word in description_lower for word in ['friendly', 'polite', 'kind', 'helpful'])
        is_professional = any(word in description_lower for word in ['professional', 'formal', 'business'])
        
        # Logika: női + kor + hangulat
        if is_female:
            if is_elderly and is_cheerful:
                profile = 'elderly_female_cheerful'
            elif is_young and is_friendly:
                profile = 'young_female_friendly'
            elif is_professional:
                profile = 'female_professional'
            else:
                profile = 'young_female_neutral'
        elif is_male:
            if is_elderly:
                profile = 'male_elderly'
            elif is_young:
                profile = 'male_young'
            elif is_professional:
                profile = 'male_professional'
            else:
                profile = 'male_young'
        else:
            # Alapértelmezett
            profile = 'default'
        
        voice_id = self.VOICE_PROFILES[profile]
        self.character_voice_map[character] = voice_id
        
        return voice_id
    
    def get_voice_id(self, character: str) -> str:
        """
        Visszaadja a szereplőhöz tartozó voice ID-t.
        
        Args:
            character: Szereplő neve
            
        Returns:
            str: ElevenLabs voice ID
        """
        return self.character_voice_map.get(character, self.VOICE_PROFILES['default'])
    
    def get_all_mappings(self) -> Dict[str, str]:
        """Visszaadja az összes szereplő -> voice ID párosítást."""
        return self.character_voice_map.copy()
