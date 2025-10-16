"""
AutoSound - Batch Mode
Több forgatókönyv fájl automatikus feldolgozása
"""

import os
from dotenv import load_dotenv
from batch_processor import BatchProcessor


def print_banner():
    """Kiírja a program bannerét."""
    print("\n" + "="*60)
    print("🎵 AutoSound - BATCH MODE")
    print("   Több forgatókönyv automatikus feldolgozása")
    print("="*60 + "\n")


def print_summary(batch_result: dict):
    """Kiírja a batch feldolgozás összefoglalóját."""
    if not batch_result.get('success'):
        return
    
    print("\n" + "="*60)
    print("✅ BATCH FELDOLGOZÁS BEFEJEZVE!")
    print("="*60)
    print(f"📄 Összes fájl: {batch_result['total_files']}")
    print(f"✅ Sikeres: {batch_result['processed']}")
    print(f"❌ Sikertelen: {batch_result['failed']}")
    
    if batch_result['failed'] > 0:
        print(f"\n⚠️  Sikertelen fájlok:")
        for result in batch_result['results']:
            if not result['success']:
                print(f"   • {result['name']}: {result['error']}")
    
    print(f"\n📊 Összesítő jelentés: batch_output/batch_summary.json")
    print("="*60 + "\n")
    
    # Részletes statisztikák
    total_dialogues = sum(r['dialogues_count'] for r in batch_result['results'])
    total_generated = sum(r['generated_count'] for r in batch_result['results'])
    
    print("📈 Statisztikák:")
    print(f"   💬 Összes párbeszéd: {total_dialogues}")
    print(f"   🎵 Generált hangfájlok: {total_generated}")
    print(f"   📁 Output mappák:")
    
    for result in batch_result['results']:
        if result['success']:
            print(f"      • {result['name']}/  ({result['generated_count']} fájl)")
    
    print()


def main():
    """Fő program futási logika."""
    
    print_banner()
    
    # 1. API kulcs betöltése
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key:
        print("❌ Hiba: ELEVENLABS_API_KEY nincs beállítva!")
        print("   Ellenőrizd a .env fájlt.")
        return
    
    # 2. Input mappa bekérése
    print("📂 BATCH FELDOLGOZÁS BEÁLLÍTÁSOK\n")
    
    input_dir = input("Input mappa elérési útja (ahol a .docx/.txt fájlok vannak): ").strip()
    
    if not input_dir:
        print("❌ Hiba: Input mappa megadása kötelező!")
        return
    
    if not os.path.exists(input_dir):
        print(f"❌ Hiba: A mappa nem található: {input_dir}")
        return
    
    # 3. Output mappa bekérése (opcionális)
    output_dir = input("Output alap mappa (Enter = 'batch_output'): ").strip()
    if not output_dir:
        output_dir = "batch_output"
    
    # 4. Egyedi hang mappingek (opcionális)
    print("\n💡 Tipp: Ha szeretnél egyedi hang-párosításokat megadni,")
    print("   szerkeszd a voice_manager.py fájlt a futtatás előtt.\n")
    
    custom_mappings = {}
    # Példa egyedi mappingekre:
    # custom_mappings = {
    #     'Lisa': 'young_female_friendly',
    #     'Teacher': 'female_professional'
    # }
    
    # 5. Batch processor létrehozása és futtatása
    processor = BatchProcessor(
        input_dir=input_dir,
        output_base_dir=output_dir,
        api_key=api_key
    )
    
    # Összes fájl feldolgozása
    batch_result = processor.process_all(custom_mappings)
    
    # 6. Összefoglaló kiírása
    if batch_result.get('success'):
        print_summary(batch_result)
    elif batch_result.get('cancelled'):
        print("\n⚠️  Feldolgozás megszakítva a felhasználó által.\n")
    else:
        print(f"\n❌ Hiba a batch feldolgozás során: {batch_result.get('error')}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Megszakítva (Ctrl+C)\n")
    except Exception as e:
        print(f"\n❌ Váratlan hiba: {e}\n")
