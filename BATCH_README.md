# 📁 Batch Mode - Több Forgatókönyv Automatikus Feldolgozása

## 🎯 Mi az a Batch Mode?

A **Batch Mode** lehetővé teszi, hogy egy mappába helyezett **összes forgatókönyv fájlt** (.txt vagy .docx) egyszerre feldolgozd, és minden forgatókönyvhöz külön almappát készíts a hangfájlokkal.

---

## 🚀 Gyors Használat

### 1. Készítsd elő a forgatókönyveket

Hozz létre egy mappát (pl. `scripts/`) és rakd bele az összes .docx vagy .txt forgatókönyv fájlodat:

```
scripts/
├── 01_At_the_Market.docx
├── 02_In_the_Restaurant.docx
├── 03_At_the_Hotel.txt
└── 04_Shopping.docx
```

### 2. Telepítsd az új függőséget

```bash
pip install -r requirements.txt
```

(Ez telepíti a `python-docx` library-t is)

### 3. Futtasd a batch programot

```bash
python batch_main.py
```

### 4. Add meg az input mappát

```
Input mappa elérési útja: c:/Users/YourName/scripts
```

### 5. Nyomj Enter az output mappánál (vagy adj meg egyedit)

```
Output alap mappa (Enter = 'batch_output'): [ENTER]
```

### 6. Erősítsd meg

```
⚠️  4 fájl feldolgozása kezdődik. Folytatod? (i/n): i
```

---

## 📂 Output Struktúra

A program minden forgatókönyvhöz külön almappát hoz létre:

```
batch_output/
├── 01_At_the_Market/
│   ├── 01_Lisa_001.mp3
│   ├── 01_Seller_002.mp3
│   ├── ...
│   ├── dialogues.json
│   ├── dialogues.csv
│   └── voice_mappings.json
│
├── 02_In_the_Restaurant/
│   ├── 01_Waiter_001.mp3
│   ├── 01_Customer_002.mp3
│   ├── ...
│   ├── dialogues.json
│   ├── dialogues.csv
│   └── voice_mappings.json
│
├── 03_At_the_Hotel/
│   └── ...
│
├── 04_Shopping/
│   └── ...
│
└── batch_summary.json  ← Összesítő jelentés
```

---

## 📄 Támogatott Fájlformátumok

### ✅ .txt fájlok

Sima szöveges fájlok, ugyanazzal a formátummal mint az `example_script.txt`:

```
Cím
Alcím
Level: A1

Characters:
• Szereplő1 – leírás
• Szereplő2 – leírás

Slide 1
Scene: A market                      ← NEM generálódik! ✅
Dialogue:
Szereplő1: Párbeszéd szövege...      ← Generálódik ✅
Szereplő2: Válasz szöveg...          ← Generálódik ✅

Slide 2
Setting: Restaurant                  ← NEM generálódik! ✅
Dialogue:
Szereplő1: Szöveg...
Szereplő2: Válasz szöveg...

💡 **Kredit megtakarítás**: `Scene:`, `Setting:`, `Location:` stb. leíró sorok automatikusan kiszűrődnek!
```

### ✅ .docx fájlok (Microsoft Word)

Word dokumentumok bármilyen formázással. A program:
- Kinyeri a bekezdéseket
- Feldolgozza a táblázatokat
- Automatikusan felismeri a szerkezetet

⚠️ **Fontos**: A .docx fájloknak is ugyanazt a logikai struktúrát kell követniük (Slide 1, Dialogue, Szereplő: Szöveg)

---

## 🎛️ Speciális Beállítások

### Egyedi Hang Párosítások

Ha minden forgatókönyvhöz ugyanazokat a szereplőket szeretnéd ugyanazzal a hanggal:

Szerkeszd a `batch_main.py` fájlt, 65. sor körül:

```python
custom_mappings = {
    'Lisa': 'young_female_friendly',
    'Teacher': 'female_professional',
    'Student': 'male_young'
}
```

### Output Mappa Átnevezése

Alapértelmezetten a program a fájl nevét használja a mappához (pl. `01_At_the_Market.docx` → `01_At_the_Market/`)

Ha más struktúrát szeretnél, módosítsd a `batch_processor.py` `create_output_directory()` metódusát.

---

## 📊 Batch Summary JSON

A `batch_output/batch_summary.json` tartalmazza az összesítő jelentést:

```json
{
  "timestamp": "2025-10-16T14:30:00",
  "input_directory": "c:/scripts",
  "output_directory": "batch_output",
  "total_files": 4,
  "processed_files": 4,
  "failed_files": [],
  "results": [
    {
      "file": "scripts/01_At_the_Market.docx",
      "name": "01_At_the_Market",
      "success": true,
      "dialogues_count": 15,
      "generated_count": 15,
      "output_dir": "batch_output/01_At_the_Market"
    },
    ...
  ]
}
```

---

## 🐛 Hibaelhárítás

### "No module named 'docx'"

```bash
pip install python-docx
```

### "Nincs párbeszéd a forgatókönyvben"

- Ellenőrizd, hogy a .docx vagy .txt fájl tartalmazza a "Slide X" és "Dialogue:" részeket
- Nyisd meg a fájlt és nézd meg, hogy a formátum helyes-e

### Egy fájl feldolgozása sikertelen, de a többi folytatódik

Ez normális! A batch processor folytatja a többi fájllal, és az összesítőben jelzi a sikertelen fájlokat.

### .docx fájl üres szöveget ad vissza

- Ellenőrizd, hogy a szöveg nem képként vagy text boxban van-e (ezeket a program nem tudja kinyerni)
- Próbáld meg "Save As" → `.txt` és használd azt

---

## 💡 Tippek

### 1. Fájlnevek számozása

Használj számozott fájlneveket a helyes sorrendhez:
```
01_Lesson_One.docx
02_Lesson_Two.docx
03_Lesson_Three.docx
```

### 2. Nagy mennyiségű fájl

Ha 10+ fájlod van, érdemes őket almappákba szervezni és részletekben feldolgozni (API rate limit miatt).

### 3. Előnézet

Használd először az egyetlen-fájl módot (`python main.py`) hogy ellenőrizd a formátumot, aztán kapcsolj batch módra.

### 4. Backup

Készíts biztonsági mentést a forgatókönyveidről feldolgozás előtt!

---

## 🔄 Workflow Példa

1. **Word dokumentumok készítése** az oktatási forgatókönyvekből
2. **Mappába helyezés** (pl. `c:/my_scripts/`)
3. **Batch futtatás**: `python batch_main.py`
4. **Input mappa megadása**: `c:/my_scripts/`
5. **Eredmény**: `batch_output/` mappában minden forgatókönyv külön almappában

---

## 📈 Skálázhatóság

- ✅ 1-5 fájl: Gyors (pár perc)
- ✅ 5-20 fájl: Közepes (10-30 perc)
- ⚠️ 20+ fájl: Lassú (API rate limit miatt érdemes részletekben)

---

## 🆘 Segítség

Ha problémába ütközöl:
1. Ellenőrizd a `batch_summary.json` fájlt a hiba részleteiért
2. Próbáld meg először egyetlen fájllal (`python main.py`)
3. Nézd meg a `failed_files` listát az összesítőben

---

**Készítette**: AutoSound Batch Processor v1.0
