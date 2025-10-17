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
    
    # Előre definiált ElevenLabs voice ID-k - BRITISH ENGLISH 🇬🇧
    # Csak brit angol hangok a helyes kiejtéshez!
    # A teljes hanglista: https://elevenlabs.io/voice-library
    
    VOICE_PROFILES = {
        # Női brit hangok 🇬🇧
        'young_female_friendly': 'pFZP5JQG7iQjIQuC4Bku',      # Lily - British, young, warm
        'young_female_neutral': 'XrExE9yKIg1WjnnlVkGX',       # Matilda - British, young, pleasant
        'elderly_female_cheerful': 'XB0fDUnXU5powFXDhCwa',    # Charlotte - British, middle-aged, warm
        'female_professional': 'z9fAnlkpzviPz146aGWa',        # Serena - British, clear, professional
        
        # Férfi brit hangok 🇬🇧
        'male_young': 'N2lVS1w4EtoT3dr4eOWO',                 # Callum - British, young, neutral
        'male_elderly': 'iP95p4xoKVk53GoZ742B',               # Chris - British, mature, engaging
        'male_professional': 'JBFqnCBsd6RMkjVDRZzb',          # George - British, professional, clear
        
        # Alapértelmezett - brit női hang
        'default': 'pFZP5JQG7iQjIQuC4Bku'                     # Lily - British default
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
        
        # NÉV alapú nem-felismerés (ha nincs leírás)
        character_lower = character.lower()
        
        # Tipikus férfi nevek
        male_names = [
            'tom', 'jake', 'mark', 'john', 'james', 'robert', 'michael', 'david',
            'william', 'daniel', 'matthew', 'chris', 'paul', 'peter', 'andrew',
            'manager', 'waiter', 'clerk', 'man', 'boy', 'father', 'brother', 'mr',
            'callum', 'george', 'jack', 'ben', 'joe', 'steve', 'kevin',
            'doctor', 'receptionist'  # Gyakran férfi szerepek
        ]
        
        # Tipikus női nevek
        female_names = [
            'lisa', 'sarah', 'emma', 'emily', 'julia', 'mia', 'claire', 'anna',
            'maria', 'laura', 'jane', 'kate', 'lucy', 'sophie', 'olivia', 'rachel',
            'seller', 'waitress', 'woman', 'lady', 'girl', 'mother', 'sister', 'mrs',
            'lily', 'matilda', 'charlotte', 'serena', 'jessica', 'amy', 'hannah'
        ]
        
        # Unisex nevek - kontextus alapján döntünk
        unisex_names = ['alex', 'sam', 'charlie', 'taylor', 'jordan', 'casey']
        
        # Név alapú felismerés
        is_male_name = character_lower in male_names
        is_female_name = character_lower in female_names
        is_unisex_name = character_lower in unisex_names
        
        # Automatikus felismerés kulcsszavak alapján (leírásból)
        description_lower = description.lower() if description else ""
        
        # Kor szerinti felismerés
        is_young = any(word in description_lower for word in ['young', 'teenager', 'student', 'child'])
        is_elderly = any(word in description_lower for word in ['elderly', 'old', 'senior', 'grandmother', 'grandfather'])
        
        # Nem szerinti felismerés (leírásból)
        is_female = any(word in description_lower for word in ['lady', 'woman', 'girl', 'female', 'mother', 'sister'])
        is_male = any(word in description_lower for word in ['man', 'boy', 'male', 'father', 'brother'])
        
        # Hangulat
        is_cheerful = any(word in description_lower for word in ['cheerful', 'happy', 'jovial', 'upbeat'])
        is_friendly = any(word in description_lower for word in ['friendly', 'polite', 'kind', 'helpful'])
        is_professional = any(word in description_lower for word in ['professional', 'formal', 'business'])
        
        # JAVÍTOTT LOGIKA: Név prioritás, aztán leírás
        
        # 1. Ha a NÉV egyértelműen férfi
        if is_male_name or is_male:
            if is_elderly:
                profile = 'male_elderly'
            elif is_young:
                profile = 'male_young'
            elif is_professional:
                profile = 'male_professional'
            else:
                profile = 'male_young'  # Alapértelmezett férfi hang
        
        # 2. Ha a NÉV egyértelműen női
        elif is_female_name or is_female:
            if is_elderly and is_cheerful:
                profile = 'elderly_female_cheerful'
            elif is_young and is_friendly:
                profile = 'young_female_friendly'
            elif is_professional:
                profile = 'female_professional'
            else:
                profile = 'young_female_neutral'
        
        # 3. Unisex név - leírás alapján döntünk
        elif is_unisex_name:
            if is_male or 'he' in description_lower or 'his' in description_lower:
                profile = 'male_young'
            elif is_female or 'she' in description_lower or 'her' in description_lower:
                profile = 'young_female_neutral'
            else:
                # Végződés alapján próbálkozunk
                if character_lower.endswith('a'):
                    profile = 'young_female_neutral'
                else:
                    profile = 'male_young'
        
        # 4. Alapértelmezett (ha sem név, sem leírás nem segít)
        else:
            # Próbálkozás: ha a név 'a'-ra, 'ia'-ra stb. végződik → női
            if character_lower.endswith(('a', 'ia', 'ella', 'ette', 'ine', 'ie')):
                profile = 'young_female_neutral'
            else:
                profile = 'male_young'  # Alapért. inkább férfi mint női
        
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
