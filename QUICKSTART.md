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
Scene: Helyszín leírás       ← NEM generálódik le! ✅
Dialogue:
Szereplő1: Mondat...          ← Generálódik ✅
Szereplő2: Válasz...          ← Generálódik ✅
```

💡 **Kredit megtakarítás**: A `Scene:`, `Setting:`, `Location:` stb. leíró sorok automatikusan kiszűrődnek!

---

## ⚙️ Beállítások

### Voice ID-k módosítása

A program **brit angol 🇬🇧 hangokat** használ alapból (Lily, Matilda, Charlotte, Callum, George, stb.)

Ha más hangokat szeretnél, szerkeszd a `voice_manager.py` fájlt, `VOICE_PROFILES` dictionary:

```python
VOICE_PROFILES = {
    'young_female_friendly': 'ÚJ_VOICE_ID_ITT',  # Új hang ID
    ...
}
```

### TTS beállítások - Lassú, pontos beszéd

A program **lassú, pontos beszédre** van optimalizálva:

```python
"voice_settings": {
    "stability": 0.95,        # NAGYON MAGAS = lassú, pontos beszéd
    "similarity_boost": 0.40, # ALACSONY = kevesebb improvizáció
    "style": 0.0,            # 0 = semleges, pontos felolvasás
}
```

**Model**: `eleven_turbo_v2` (gyorsabb és pontosabb)

💡 **Tempó állítás**:
- **Még lassabb**: Növeld a stability-t 0.98-ra (`tts_generator.py`, 63. sor)
- **Gyorsabb**: Csökkentsd a stability-t 0.75-0.80-ra

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
