# 🎵 AutoSound - Oktatási Forgatókönyv TTS Generátor

Automatikusan generál hangfájlokat oktatási forgatókönyvekből az ElevenLabs Text-to-Speech API segítségével.

## ✨ Funkciók

- 📖 **Forgatókönyv elemzés**: Automatikusan felismeri a jeleneteket, szereplőket és párbeszédeket
- 🎤 **Intelligens hangprofil hozzárendelés**: A szereplők leírása alapján választ megfelelő hangot
- 🔊 **ElevenLabs TTS integráció**: Professzionális minőségű hangok 29+ nyelven
- 📁 **Strukturált kimenet**: JSON és CSV export az oktatási appokba való importáláshoz
- 🎯 **Batch feldolgozás**: Több párbeszéd generálása egyszerre
- 📂 **Batch Mode**: Több .docx/.txt fájl automatikus feldolgozása mappánként szervezve
- 📄 **Word támogatás**: .docx fájlok közvetlen feldolgozása

## 📋 Követelmények

- Python 3.7+
- ElevenLabs API kulcs ([regisztráció itt](https://elevenlabs.io/))

## 🚀 Telepítés és Használat

### 1. Függőségek telepítése

```bash
pip install -r requirements.txt
```

### 2. Program futtatása

#### Alapvető futtatás (egy fájl)

```bash
python main.py
```

A program bekéri a forgatókönyv fájl elérési útját. Ha entert nyomsz, az `example_script.txt` lesz használva.

#### 🔥 Batch Mode (több fájl egyszerre)

```bash
python batch_main.py
```

**Több forgatókönyv automatikus feldolgozása:**
- Rakd az összes .docx vagy .txt fájlt egy mappába
- A program mindegyiket feldolgozza
- Minden forgatókönyvhöz külön almappa készül

📖 **Részletek**: Olvasd el a [BATCH_README.md](BATCH_README.md) fájlt!

## 📝 Forgatókönyv formátum

A forgatókönyvnak a következő struktúrát kell követnie:

```
Cím sor (pl. 8 Food and Drink)
Alcím sor (pl. 8.2 – At the Market)
Level: A1

Characters:
• Szereplő1 – leírás (pl. friendly and polite)
• Szereplő2 – leírás (pl. elderly lady, cheerful)

Slide 1
Dialogue:
Szereplő1: Párbeszéd szövege...
Szereplő2: Válasz szöveg...

Slide 2
Dialogue:
Szereplő1: Következő jelenet...
Szereplő2: Válasz...
```

### Példa

Nézd meg az `example_script.txt` fájlt egy teljes példáért:
- 3 slide
- 2 szereplő (Lisa és Seller)
- 12 párbeszéd összesen

## 📂 Kimenet

A program az `output/` mappába menti az eredményeket:

### Hangfájlok

**Fájlnév formátum**: `{slide_szám}_{szereplő}_{sorszám}.mp3`

**Példák**:
- `01_Lisa_001.mp3` - Lisa első mondata az 1. slide-on
- `01_Seller_002.mp3` - Seller második mondata az 1. slide-on
- `02_Lisa_003.mp3` - Lisa mondata a 2. slide-on

### Strukturált adatok

#### `dialogues.json`
Teljes párbeszéd lista strukturálva:
```json
[
  {
    "scene": "Slide 1",
    "slide_number": 1,
    "character": "Lisa",
    "text": "Good morning.",
    "line_number": 1,
    "voice_id": "EXAVITQu4vr4xnSDxMaL",
    "file_name": "01_Lisa_001.mp3",
    "file_path": "output/01_Lisa_001.mp3",
    "success": true
  }
]
```

#### `dialogues.csv`
Táblázat formátumban az összes adat (Excel-ben megnyitható).

#### `voice_mappings.json`
Szereplő → Voice ID párosítások:
```json
{
  "Lisa": "EXAVITQu4vr4xnSDxMaL",
  "Seller": "XB0fDUnXU5powFXDhCwa"
}
```

## 🎨 Hangprofilok

### Automatikus felismerés

A program automatikusan hozzárendeli a hangokat a szereplők leírása alapján:

| Kulcsszó kategória | Felismert szavak | Eredmény |
|-------------------|------------------|----------|
| **Kor** | young, elderly, old, teenager, child | Életkorhoz illő hang |
| **Nem** | female, male, lady, man, girl, boy | Női/férfi hang |
| **Stílus** | friendly, cheerful, professional, polite | Hangulat beállítás |

### Előre konfigurált hangprofilok

A `voice_manager.py` tartalmazza a következő profilokat:

- `young_female_friendly` - Fiatal, barátságos női hang
- `young_female_neutral` - Semleges fiatal női hang
- `elderly_female_cheerful` - Idősebb, vidám női hang
- `female_professional` - Professzionális női hang
- `male_young` - Fiatal férfi hang
- `male_elderly` - Idősebb férfi hang
- `male_professional` - Professzionális férfi hang

### Hangok testreszabása

#### Módszer 1: Egyedi mapping a main.py-ban

```python
# main.py, 74. sor körül
custom_mappings = {
    'Lisa': 'young_female_friendly',
    'Teacher': 'female_professional',
    'Student': 'male_young'
}
```

#### Módszer 2: Voice ID-k módosítása

Szerkeszd a `voice_manager.py` `VOICE_PROFILES` dictionary-jét más ElevenLabs voice ID-kkal.

Elérhető hangok: [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)

## 🎛️ TTS beállítások - PONTOSSÁG OPTIMALIZÁLVA

A program a **legpontosabb szövegkövetésre** van beállítva:

```python
"voice_settings": {
    "stability": 0.85,          # MAGASABB = pontosabb, szó szerinti (0-1)
    "similarity_boost": 0.50,   # ALACSONYABB = kevésbé kreatív (0-1)
    "style": 0.0,               # 0 = minimális stílus (0-1)
    "use_speaker_boost": True   # Beszélő hangerő optimalizálás
}
```

**Model**: `eleven_turbo_v2` - gyorsabb és pontosabb mint a multilingual_v2

### Paraméterek magyarázata:
- **stability (0.85)**: Magas érték = konzisztens, pontos kiejtés (nem improvizál)
- **similarity_boost (0.50)**: Alacsony érték = kevesebb "kreatív" interpretáció
- **style (0.0)**: Zéró = teljesen semleges, szó szerinti felolvasás

⚠️ **Ha mégis eltérést tapasztalsz**, növeld a stability értéket 0.95-re a `tts_generator.py` 63. sorában

## 📊 Projekt struktúra

```
AutoSound/
│
├── main.py                 # Fő program (egy fájl feldolgozása)
├── batch_main.py           # Batch program (több fájl egyszerre) 🆕
├── script_parser.py        # Forgatókönyv elemző (.txt)
├── docx_parser.py          # DOCX forgatókönyv elemző (.docx) 🆕
├── batch_processor.py      # Batch feldolgozó modul 🆕
├── voice_manager.py        # Hangprofil menedzser
├── tts_generator.py        # ElevenLabs TTS integráció
│
├── requirements.txt        # Python függőségek
├── .env                    # API kulcs (git ignore!)
├── .env.example           # Példa .env fájl
│
├── README.md              # Fő dokumentáció
├── BATCH_README.md        # Batch mode dokumentáció 🆕
├── QUICKSTART.md          # Gyors kezdés
│
├── example_script.txt     # Példa forgatókönyv
├── output/                # Egy fájl output (main.py)
└── batch_output/          # Batch output (batch_main.py) 🆕
    ├── Script_1/
    ├── Script_2/
    └── batch_summary.json
```

## 🔧 Hibakeresés

### "ELEVENLABS_API_KEY nincs beállítva"
- Ellenőrizd, hogy létezik-e a `.env` fájl
- Ellenőrizd, hogy az API kulcs helyesen van-e beírva

### "Quota exceeded" vagy rate limit hibák
- Az ingyenes ElevenLabs csomag havi 10,000 karakterre korlátozza a TTS használatot
- Módosítsd a `delay` paramétert a `tts_generator.generate_batch()` hívásban (növeld 0.5-ről 1.0-ra)

### Forgatókönyv nem felismerhető
- Ellenőrizd, hogy a "Slide X" felirat külön sorban van-e
- Ellenőrizd, hogy a párbeszédek "Szereplő: Szöveg" formátumban vannak-e
- A szereplő neve betűkből álljon (számok és speciális karakterek nélkül)

## 🚀 Bővítési lehetőségek

A kód könnyen bővíthető:

1. **Több nyelv támogatása**: Módosítsd a `model` paramétert (pl. `eleven_turbo_v2`)
2. **Hangeffektek**: Adj hozzá background zajokat vagy zenét
3. **SSML támogatás**: Használj SSML tageket a szövegben szünetekhez, hangsúlyozáshoz
4. **UI interfész**: Tkinter vagy web-based felület
5. **Batch export**: Automatikus exportálás LMS platformokra (Moodle, Canvas)

## 📄 Licenc

Ez a projekt oktatási célokra készült. Szabadon használható és módosítható.

## 🆘 Támogatás

Ha kérdésed van vagy problémába ütközöl, ellenőrizd:
1. A Python verziódat (3.7+)
2. Az API kulcs érvényességét
3. Az internetkapcsolatot
4. A forgatókönyv formátumát

---

**Készítette**: AutoSound TTS Generator
**Verzió**: 1.0
**Utolsó frissítés**: 2025. október