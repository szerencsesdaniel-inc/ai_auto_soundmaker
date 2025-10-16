# ⚡ Batch Mode - Gyors Útmutató

## 🎯 3 lépésben több forgatókönyv feldolgozása

### 1️⃣ Készítsd elő a forgatókönyveket

Hozz létre egy mappát és rakd bele az összes .docx vagy .txt fájlodat:

```
c:/Users/YourName/my_scripts/
├── 01_At_the_Market.docx
├── 02_In_the_Restaurant.docx
├── 03_At_the_Hotel.txt
└── 04_Shopping.docx
```

### 2️⃣ Telepítsd az új függőséget

```bash
pip install -r requirements.txt
```

Ez telepíti a `python-docx` library-t is a .docx támogatáshoz.

### 3️⃣ Futtasd a batch programot

```bash
python batch_main.py
```

Majd:
1. **Add meg az input mappát**: `c:/Users/YourName/my_scripts`
2. **Nyomj Enter** az output mappánál (vagy adj meg egyedit)
3. **Írd be: `i`** a megerősítésnél

---

## 📂 Eredmény

```
batch_output/
├── 01_At_the_Market/          ← Külön mappa minden forgatókönyvhöz
│   ├── 01_Lisa_001.mp3
│   ├── 01_Seller_002.mp3
│   ├── dialogues.json
│   ├── dialogues.csv
│   └── voice_mappings.json
│
├── 02_In_the_Restaurant/
│   ├── 01_Waiter_001.mp3
│   ├── 01_Customer_002.mp3
│   └── ...
│
├── 03_At_the_Hotel/
│   └── ...
│
├── 04_Shopping/
│   └── ...
│
└── batch_summary.json         ← Összesítő jelentés
```

---

## 🎨 Előnyök

✅ **Automatikus**: Végigmegy minden fájlon  
✅ **Szervezett**: Külön mappa minden forgatókönyvhöz  
✅ **Hibaállóság**: Ha egy fájl sikertelen, folytatja a többivel  
✅ **Összesítő**: Részletes jelentés a végén  

---

## 📝 Támogatott fájlok

- ✅ `.txt` - Sima szöveges fájlok
- ✅ `.docx` - Microsoft Word dokumentumok

**Fontos**: Mindkét formátumnak ugyanazt a logikai struktúrát kell követnie:
```
Slide 1
Dialogue:
Szereplő: Szöveg...
```

---

## 💡 Tippek

### Fájlnevek számozása
```
01_Lesson_One.docx
02_Lesson_Two.docx
03_Lesson_Three.docx
```

### Tesztelés
Próbáld először 1-2 fájllal:
```bash
python batch_main.py
```

### Nagy mennyiség
10+ fájlnál érdemes részletekben dolgozni (API rate limit).

---

## 🆘 Problémák?

### "No module named 'docx'"
```bash
pip install python-docx
```

### Fájl nem található
- Ellenőrizd az elérési utat (pl. `c:/Users/...`)
- Windows-on használj `/` vagy `\\` a mappák között

### .docx nem dolgozódik fel
- Nyisd meg Wordben és mentsd el újra
- Ellenőrizd, hogy a szöveg nem képként van-e

---

**Részletek**: [BATCH_README.md](BATCH_README.md)
