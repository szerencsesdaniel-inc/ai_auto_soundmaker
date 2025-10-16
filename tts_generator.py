"""
Text-to-Speech generátor modul
Feladata: ElevenLabs API-val hangfájlokat generálni.
"""

import os
import requests
from typing import Optional
import time


class TTSGenerator:
    """
    ElevenLabs Text-to-Speech generátor osztály.
    MP3 fájlokat generál a párbeszédekből.
    """
    
    def __init__(self, api_key: str, output_dir: str = "output"):
        """
        Inicializálja a TTS generátort.
        
        Args:
            api_key: ElevenLabs API kulcs
            output_dir: Kimenet mappa neve
        """
        self.api_key = api_key
        self.output_dir = output_dir
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Output mappa létrehozása
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_speech(self, 
                       text: str, 
                       voice_id: str, 
                       filename: str,
                       model: str = "eleven_turbo_v2") -> Optional[str]:
        """
        Generál egy hangfájlt az ElevenLabs API-val.
        
        Args:
            text: A mondandó szöveg
            voice_id: ElevenLabs voice ID
            filename: A mentendő fájl neve (pl. "01_Lisa_001.mp3")
            model: ElevenLabs model (alapért: eleven_multilingual_v2)
            
        Returns:
            Optional[str]: A mentett fájl teljes elérési útja, vagy None hiba esetén
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        # TTS beállítások - PONTOSSÁG + LASSÍTOTT TEMPÓ
        data = {
            "text": text,
            "model_id": model,
            "voice_settings": {
                "stability": 0.95,           # NAGYON MAGAS = lassabb, pontosabb beszéd (0-1)
                "similarity_boost": 0.40,    # ALACSONY = kevésbé kreatív, lassabb (0-1)
                "style": 0.0,                # 0 = minimális stílus, szó szerinti (0-1)
                "use_speaker_boost": True    # Beszélő hangerő optimalizálás
            }
        }
        
        try:
            print(f"  🎤 Generálás: {filename}...", end=" ")
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # MP3 mentése
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Kész ({len(response.content)} bytes)")
                return filepath
            else:
                print(f"❌ Hiba: {response.status_code}")
                print(f"     Válasz: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout hiba")
            return None
        except Exception as e:
            print(f"❌ Kivétel: {e}")
            return None
    
    def generate_batch(self, dialogues: list, voice_manager, delay: float = 0.5) -> list:
        """
        Több párbeszédet generál egymás után.
        
        Args:
            dialogues: Párbeszéd lista (dict-ek listája)
            voice_manager: VoiceManager instance a voice ID-khoz
            delay: Késleltetés az API hívások között (másodpercben)
            
        Returns:
            list: Generált fájlok adatai (bővített dialogues lista)
        """
        results = []
        
        print(f"\n🎬 Összesen {len(dialogues)} párbeszéd generálása indítása...\n")
        
        for i, dialogue in enumerate(dialogues, 1):
            # Fájlnév generálás
            slide_num = f"{dialogue['slide_number']:02d}"
            character = dialogue['character']
            line_num = f"{dialogue['line_number']:03d}"
            filename = f"{slide_num}_{character}_{line_num}.mp3"
            
            # Voice ID lekérése
            voice_id = voice_manager.get_voice_id(character)
            
            # Hangfájl generálása
            filepath = self.generate_speech(
                text=dialogue['text'],
                voice_id=voice_id,
                filename=filename
            )
            
            # Eredmény hozzáadása
            result = dialogue.copy()
            result['voice_id'] = voice_id
            result['file_name'] = filename
            result['file_path'] = filepath
            result['success'] = filepath is not None
            
            results.append(result)
            
            # Késleltetés az API rate limit miatt
            if i < len(dialogues):
                time.sleep(delay)
        
        # Statisztika
        success_count = sum(1 for r in results if r['success'])
        print(f"\n✅ Sikeres: {success_count}/{len(dialogues)}")
        
        return results
    
    def get_available_voices(self) -> Optional[dict]:
        """
        Lekéri az elérhető hangokat az ElevenLabs API-ból.
        
        Returns:
            Optional[dict]: Hangok listája vagy None hiba esetén
        """
        url = f"{self.base_url}/voices"
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Hiba a hangok lekérésekor: {response.status_code}")
                return None
        except Exception as e:
            print(f"Kivétel a hangok lekérésekor: {e}")
            return None
