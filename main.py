"""
AutoSound - Oktatási forgatókönyv TTS generáló
Fő program fájl
"""

import os
import json
import csv
from dotenv import load_dotenv
from script_parser import ScriptParser
from voice_manager import VoiceManager
from tts_generator import TTSGenerator


def save_json(data: list, output_path: str):
    """Menti a strukturált adatokat JSON formátumban."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📄 JSON mentve: {output_path}")


def save_csv(data: list, output_path: str):
    """Menti a strukturált adatokat CSV formátumban."""
    if not data:
        return
    
    # CSV mezők
    fieldnames = ['scene', 'slide_number', 'character', 'text', 'voice_id', 'file_name', 'success']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in data:
            # Csak a szükséges mezők
            csv_row = {key: row.get(key, '') for key in fieldnames}
            writer.writerow(csv_row)
    
    print(f"📊 CSV mentve: {output_path}")


def print_summary(parser_data: dict, voice_manager: VoiceManager):
    """Kiírja a projekt összefoglalóját."""
    print("\n" + "="*60)
    print("📋 FORGATÓKÖNYV ÖSSZEFOGLALÓ")
    print("="*60)
    
    # Metaadatok
    metadata = parser_data['metadata']
    if metadata:
        print(f"\n📌 Cím: {metadata.get('title', 'N/A')}")
        if 'subtitle' in metadata:
            print(f"   Alcím: {metadata['subtitle']}")
        print(f"   Szint: {metadata.get('level', 'N/A')}")
    
    # Szereplők
    characters = parser_data['characters']
    print(f"\n👥 Szereplők ({len(characters)}):")
    for char, desc in characters.items():
        voice_id = voice_manager.get_voice_id(char)
        print(f"   • {char}: {desc}")
        print(f"     Voice ID: {voice_id}")
    
    # Jelenetek
    scenes = parser_data['scenes']
    total_dialogues = sum(len(scene['dialogues']) for scene in scenes)
    print(f"\n🎬 Jelenetek: {len(scenes)} slide")
    print(f"💬 Összes párbeszéd: {total_dialogues}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Fő program futási logika."""
    
    print("🎵 AutoSound - Oktatási TTS Generátor")
    print("="*60)
    
    # 1. Környezeti változók betöltése (.env fájl)
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key:
        print("❌ Hiba: ELEVENLABS_API_KEY nincs beállítva!")
        print("   1. Másold le a .env.example fájlt .env néven")
        print("   2. Írd be az API kulcsodat a .env fájlba")
        print("   3. Az API kulcsot itt szerezheted be: https://elevenlabs.io/")
        return
    
    # 2. Forgatókönyv fájl bekérése
    script_file = input("\n📄 Forgatókönyv fájl elérési útja (Enter = example_script.txt): ").strip()
    if not script_file:
        script_file = "example_script.txt"
    
    if not os.path.exists(script_file):
        print(f"❌ Hiba: A fájl nem található: {script_file}")
        return
    
    # 3. Forgatókönyv feldolgozása
    print(f"\n📖 Forgatókönyv beolvasása: {script_file}")
    parser = ScriptParser(script_file)
    parser_data = parser.parse()
    
    # 4. Hangprofilok hozzárendelése
    print("🎤 Hangprofilok hozzárendelése...")
    
    # Egyedi mappingek megadása (opcionális)
    # Példa: {'Lisa': 'young_female_friendly', 'Seller': 'elderly_female_cheerful'}
    custom_mappings = {}
    
    voice_manager = VoiceManager(custom_mappings)
    
    # Automatikus hozzárendelés a leírások alapján
    for character, description in parser_data['characters'].items():
        voice_manager.assign_voice_by_description(character, description)
    
    # Összefoglaló kiírása
    print_summary(parser_data, voice_manager)
    
    # 5. Párbeszédek előkészítése
    dialogues = parser.get_all_dialogues()
    
    if not dialogues:
        print("❌ Nincs párbeszéd a forgatókönyvben!")
        return
    
    # 6. Megerősítés a felhasználótól
    print(f"⚠️  {len(dialogues)} hangfájl kerül legenerálásra.")
    confirmation = input("   Folytatod? (i/n): ").strip().lower()
    
    if confirmation != 'i':
        print("❌ Megszakítva.")
        return
    
    # 7. TTS generálás
    output_dir = "output"
    tts_generator = TTSGenerator(api_key, output_dir)
    
    results = tts_generator.generate_batch(dialogues, voice_manager, delay=0.5)
    
    # 8. Eredmények mentése
    print("\n💾 Eredmények mentése...")
    
    # JSON export
    json_path = os.path.join(output_dir, "dialogues.json")
    save_json(results, json_path)
    
    # CSV export
    csv_path = os.path.join(output_dir, "dialogues.csv")
    save_csv(results, csv_path)
    
    # Voice mappings mentése
    mappings_path = os.path.join(output_dir, "voice_mappings.json")
    with open(mappings_path, 'w', encoding='utf-8') as f:
        json.dump(voice_manager.get_all_mappings(), f, ensure_ascii=False, indent=2)
    print(f"🔊 Voice mappings mentve: {mappings_path}")
    
    # 9. Végső összefoglaló
    print("\n" + "="*60)
    print("✅ KÉSZ!")
    print("="*60)
    print(f"📁 Output mappa: {os.path.abspath(output_dir)}")
    print(f"🎵 Generált hangfájlok: {sum(1 for r in results if r['success'])}/{len(results)}")
    print(f"📄 JSON export: {json_path}")
    print(f"📊 CSV export: {csv_path}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
