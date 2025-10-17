# 🎨 AutoSound GUI - Használati útmutató

Modern, letisztult grafikus felület az AutoSound TTS Generator-hez.

## 🚀 Indítás

```bash
python gui_main.py
```

## 🖥️ Felület áttekintése

### 📄 Forgatókönyv fájl
- **Tallózás gomb**: Válassz egy `.txt` vagy `.docx` forgatókönyv fájlt
- **Támogatott formátumok**: 
  - `.txt` - Sima szöveges fájlok
  - `.docx` - Microsoft Word dokumentumok

### 💾 Output mappa
- **Alapértelmezett**: `output/` mappa
- **Testreszabás**: Kattints a tallózás gombra és válassz saját mappát

### ⚙️ Beállítások

#### 🎚️ Beszéd sebessége
- **Csúszka**: 0.25x - 2.0x
- **Ajánlott oktatáshoz**: 0.7x - 0.9x (lassabb, érthetőbb)
- **Normál sebesség**: 1.0x
- **Gyors sebesség**: 1.2x - 2.0x

### 📋 Napló
- **Valós idejű naplózás**: Látod a folyamatot lépésről lépésre
- **Színkódolt üzenetek**:
  - ⚪ Fehér = Info
  - 🟢 Zöld = Siker
  - 🟡 Sárga = Figyelmeztetés
  - 🔴 Piros = Hiba

## 🎯 Használat lépései

1. **Tallózd be** a forgatókönyv fájlt
2. **Állítsd be** a sebességet (opcionális)
3. **Válaszd ki** az output mappát (opcionális)
4. Kattints a **🚀 Generálás indítása** gombra
5. **Várd meg** amíg elkészülnek a hangfájlok
6. **Kész!** ✅

## 🎨 Funkciók

✅ **Modern Dark Mode** design  
✅ **Drag & Drop** támogatás (tervezett)  
✅ **Valós idejű progress** követés  
✅ **Sebesség testreszabás** csúszkával  
✅ **Multi-threading** - a felület nem fagy be generálás közben  
✅ **Brit angol hangok** 🇬🇧  
✅ **Eleven v3 model** - a legpontosabb szövegkövetés  

## ⚠️ Fontos

- Győződj meg róla, hogy az **API kulcs** be van állítva a `.env` fájlban
- A generálás **pár percet** is igénybe vehet nagyobb forgatókönyveknél
- A felület **nem fagy be** - a folyamat külön szálon fut

## 🛠️ Hibakeresés

### "API kulcs nincs beállítva"
→ Ellenőrizd a `.env` fájlt, hogy tartalmazza: `ELEVENLABS_API_KEY=...`

### "Fájl nem található"
→ Győződj meg róla, hogy a fájl elérési útja helyes és a fájl létezik

### A program lefagy
→ Ez normális, nagyobb fájloknál a generálás időbe telhet. Nézd a naplót!

---

**Élvezd a modern felületet!** 🎵✨
