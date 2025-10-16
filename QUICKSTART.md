# ⚡ Gyors Kezdés - AutoSound

## 3 lépésben használatra kész!

### 1️⃣ Függőségek telepítése

```bash
pip install -r requirements.txt
```

### 2️⃣ Program futtatása

```bash
python main.py
```

### 3️⃣ Enter nyomása

Amikor a program kérdezi a forgatókönyv elérési útját, nyomj **Enter**-t a példa fájl használatához.

```
📄 Forgatókönyv fájl elérési útja (Enter = example_script.txt): [ENTER]
```

---

## ✅ Mit fog csinálni a program?

1. Beolvassa az `example_script.txt` fájlt
2. Felismeri Lisa és Seller szereplőket
3. Hozzárendeli a megfelelő hangokat
4. Megkérdez megerősítést
5. Legenerálja a 12 hangfájlt az `output/` mappába
6. Létrehozza a JSON és CSV exportokat

---

## 📁 Eredmény

Az `output/` mappában megtalálod:

**Hangfájlok (12 db)**:
- `01_Lisa_001.mp3` → "Good morning."
- `01_Seller_002.mp3` → "Good morning. What would you like?"
- `01_Lisa_003.mp3` → "I'd like some apples, please."
- ... és így tovább

**Strukturált adatok**:
- `dialogues.json` - Teljes adat JSON formátumban
- `dialogues.csv` - Excel-ben megnyitható táblázat
- `voice_mappings.json` - Szereplő → Hang párosítások

---

## 🎯 Saját forgatókönyv használata

### Módszer 1: Parancssorban

```bash
python main.py
```

Majd add meg a saját fájlod elérési útját:
```
📄 Forgatókönyv fájl elérési útja: c:/path/to/my_script.txt
```

### Módszer 2: Fájl készítése

Hozz létre egy új `.txt` fájlt az alábbi formátumban:

```
Cím
Alcím
Level: A1

Characters:
• Szereplő1 – leírás
• Szereplő2 – leírás

Slide 1
Dialogue:
Szereplő1: Mondat...
Szereplő2: Válasz...
```

---

## ⚙️ Beállítások

### Voice ID-k módosítása

Szerkeszd a `voice_manager.py` fájlt, `VOICE_PROFILES` dictionary:

```python
VOICE_PROFILES = {
    'young_female_friendly': 'ÚJ_VOICE_ID_ITT',
    ...
}
```

### TTS pontosság beállítása

A program már **optimalizálva van pontos szövegkövetésre**:

```python
"voice_settings": {
    "stability": 0.85,        # MAGAS = szó szerinti pontosság
    "similarity_boost": 0.50, # ALACSONY = kevesebb improvizáció
    "style": 0.0,            # 0 = semleges, pontos felolvasás
}
```

**Model**: `eleven_turbo_v2` (gyorsabb és pontosabb)

⚠️ **Ha mégis eltér a szövegtől**, növeld a stability-t 0.95-re (`tts_generator.py`, 63. sor)

---

## 🐛 Gyakori problémák

### ModuleNotFoundError: No module named 'requests'

```bash
pip install requests python-dotenv
```

### API kulcs hiba

Ellenőrizd a `.env` fájlban, hogy az API kulcs helyesen van-e beírva (szóköz nélkül).

### Forgatókönyv nem felismerhető

- Ellenőrizd, hogy minden "Slide X" külön sorban van
- Párbeszédek formátuma: `Szereplő: Szöveg`
- Szereplő neve csak betűkből álljon

---

## 📚 További segítség

Nézd meg a részletes `README.md` fájlt további információkért!

---

**Jó munkát! 🎵**
