"""
AutoSound - Modern GUI Application
Text-to-Speech generator oktatási forgatókönyvekhez - Modern felülettel
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
import threading
from dotenv import load_dotenv

from script_parser import ScriptParser
from docx_parser import DocxParser
from voice_manager import VoiceManager
from tts_generator import TTSGenerator
from batch_processor import BatchProcessor


class AutoSoundGUI(ctk.CTk):
    """Modern GUI AutoSound TTS Generator-hez."""
    
    def __init__(self):
        super().__init__()
        
        # Ablak beállítások
        self.title("🎵 AutoSound - TTS Generator")
        self.geometry("900x700")
        
        # Téma beállítás
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # API kulcs betöltése
        load_dotenv()
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        
        # Változók
        self.mode = ctk.StringVar(value="single")  # "single" vagy "batch"
        self.input_file_path = ctk.StringVar()
        self.input_folder_path = ctk.StringVar()
        self.output_dir_path = ctk.StringVar(value="output")
        self.speed_value = ctk.DoubleVar(value=0.7)
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Felhasználói felület összeállítása."""
        
        # ===== HEADER =====
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎵 AutoSound TTS Generator",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Oktatási forgatókönyvek → Brit angol hangfájlok 🇬🇧",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # ===== MAIN CONTENT =====
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # === MODE SELECTION ===
        mode_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_section.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            mode_section,
            text="🎯 Feldolgozási mód",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        mode_frame = ctk.CTkFrame(mode_section, fg_color="#1a1a1a", corner_radius=10)
        mode_frame.pack(fill="x", pady=5)
        
        mode_buttons_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        mode_buttons_frame.pack(pady=15, padx=15)
        
        self.single_radio = ctk.CTkRadioButton(
            mode_buttons_frame,
            text="📄 Egy fájl feldolgozása",
            variable=self.mode,
            value="single",
            command=self.on_mode_change,
            font=ctk.CTkFont(size=14)
        )
        self.single_radio.pack(side="left", padx=20)
        
        self.batch_radio = ctk.CTkRadioButton(
            mode_buttons_frame,
            text="📂 Batch - Teljes mappa feldolgozása",
            variable=self.mode,
            value="batch",
            command=self.on_mode_change,
            font=ctk.CTkFont(size=14)
        )
        self.batch_radio.pack(side="left", padx=20)
        
        # === INPUT FILE SECTION ===
        self.input_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.input_section.pack(fill="x", padx=20, pady=(10, 10))
        
        self.input_label = ctk.CTkLabel(
            self.input_section,
            text="📄 Forgatókönyv fájl",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.input_label.pack(anchor="w", pady=(0, 5))
        
        input_row = ctk.CTkFrame(self.input_section, fg_color="transparent")
        input_row.pack(fill="x")
        
        self.input_entry = ctk.CTkEntry(
            input_row,
            textvariable=self.input_file_path,
            placeholder_text="Válassz egy .txt vagy .docx fájlt...",
            height=40
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(
            input_row,
            text="📂 Tallózás",
            command=self.browse_input_file,
            width=120,
            height=40
        )
        self.browse_btn.pack(side="right")
        
        # === OUTPUT FOLDER SECTION ===
        output_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        output_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            output_section,
            text="💾 Output mappa",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        output_row = ctk.CTkFrame(output_section, fg_color="transparent")
        output_row.pack(fill="x")
        
        self.output_entry = ctk.CTkEntry(
            output_row,
            textvariable=self.output_dir_path,
            height=40
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_browse_btn = ctk.CTkButton(
            output_row,
            text="📂 Tallózás",
            command=self.browse_output_folder,
            width=120,
            height=40
        )
        output_browse_btn.pack(side="right")
        
        # === SETTINGS SECTION ===
        settings_section = ctk.CTkFrame(main_frame, fg_color="transparent")
        settings_section.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            settings_section,
            text="⚙️ Beállítások",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Speed slider
        speed_frame = ctk.CTkFrame(settings_section, fg_color="transparent")
        speed_frame.pack(fill="x", pady=5)
        
        speed_label_frame = ctk.CTkFrame(speed_frame, fg_color="transparent")
        speed_label_frame.pack(fill="x")
        
        ctk.CTkLabel(
            speed_label_frame,
            text="🎚️ Beszéd sebessége:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")
        
        self.speed_value_label = ctk.CTkLabel(
            speed_label_frame,
            text=f"{self.speed_value.get():.1f}x",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="cyan"
        )
        self.speed_value_label.pack(side="right")
        
        speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=0.25,
            to=2.0,
            variable=self.speed_value,
            command=self.update_speed_label,
            height=20
        )
        speed_slider.pack(fill="x", pady=(5, 0))
        
        # Info labels
        info_frame = ctk.CTkFrame(settings_section, fg_color="#1a1a1a", corner_radius=10)
        info_frame.pack(fill="x", pady=(10, 0), padx=10)
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Model: Eleven v3 (alpha) | Stability: Max | Brit angol 🇬🇧",
            font=ctk.CTkFont(size=12),
            text_color="lightblue"
        ).pack(pady=10)
        
        # === LOG SECTION ===
        log_section = ctk.CTkFrame(main_frame)
        log_section.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            log_section,
            text="📋 Napló",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.log_textbox = ctk.CTkTextbox(
            log_section,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # === ACTION BUTTONS ===
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Generálás indítása",
            command=self.start_generation,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Napló törlése",
            command=self.clear_log,
            height=50,
            width=150,
            fg_color="gray30",
            hover_color="gray20"
        )
        clear_btn.pack(side="right")
        
        # API kulcs ellenőrzés
        if not self.api_key:
            self.log_message("❌ HIBA: ELEVENLABS_API_KEY nincs beállítva a .env fájlban!", "error")
            self.start_btn.configure(state="disabled")
        else:
            self.log_message("✅ API kulcs betöltve", "success")
    
    def on_mode_change(self):
        """Mód váltás kezelése (Single/Batch)."""
        mode = self.mode.get()
        
        if mode == "single":
            # Single mód
            self.input_label.configure(text="📄 Forgatókönyv fájl")
            self.input_entry.configure(
                textvariable=self.input_file_path,
                placeholder_text="Válassz egy .txt vagy .docx fájlt..."
            )
            self.browse_btn.configure(command=self.browse_input_file)
            self.output_dir_path.set("output")
            self.log_message("🔄 Mód: Egy fájl feldolgozása", "info")
        else:
            # Batch mód
            self.input_label.configure(text="📂 Input mappa (több fájl)")
            self.input_entry.configure(
                textvariable=self.input_folder_path,
                placeholder_text="Válassz egy mappát .docx/.txt fájlokkal..."
            )
            self.browse_btn.configure(command=self.browse_input_folder)
            self.output_dir_path.set("batch_output")
            self.log_message("🔄 Mód: Batch - Teljes mappa feldolgozása", "info")
    
    def browse_input_file(self):
        """Input fájl tallózása (Single mód)."""
        filename = filedialog.askopenfilename(
            title="Válassz forgatókönyv fájlt",
            filetypes=[
                ("Minden támogatott", "*.txt *.docx"),
                ("Szöveges fájlok", "*.txt"),
                ("Word dokumentumok", "*.docx"),
                ("Minden fájl", "*.*")
            ]
        )
        if filename:
            self.input_file_path.set(filename)
            self.log_message(f"📄 Fájl kiválasztva: {Path(filename).name}", "info")
    
    def browse_input_folder(self):
        """Input mappa tallózása (Batch mód)."""
        folder = filedialog.askdirectory(title="Válassz input mappát (.docx/.txt fájlokkal)")
        if folder:
            self.input_folder_path.set(folder)
            # Fájlok számolása
            files = list(Path(folder).glob("*.txt")) + list(Path(folder).glob("*.docx"))
            self.log_message(f"📂 Mappa kiválasztva: {folder}", "info")
            self.log_message(f"   📄 Talált fájlok: {len(files)} db", "info")
    
    def browse_output_folder(self):
        """Output mappa tallózása."""
        folder = filedialog.askdirectory(title="Válassz output mappát")
        if folder:
            self.output_dir_path.set(folder)
            self.log_message(f"💾 Output mappa: {folder}", "info")
    
    def update_speed_label(self, value):
        """Sebesség címke frissítése."""
        self.speed_value_label.configure(text=f"{float(value):.1f}x")
    
    def log_message(self, message, msg_type="info"):
        """Üzenet hozzáadása a naplóhoz."""
        colors = {
            "info": "white",
            "success": "lightgreen",
            "warning": "yellow",
            "error": "red"
        }
        
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")
        self.update()
    
    def clear_log(self):
        """Napló törlése."""
        self.log_textbox.delete("1.0", "end")
    
    def start_generation(self):
        """Generálás indítása."""
        if self.is_processing:
            messagebox.showwarning("Figyelem", "Már folyamatban van egy feldolgozás!")
            return
        
        mode = self.mode.get()
        
        # Ellenőrzések
        if mode == "single":
            input_file = self.input_file_path.get()
            if not input_file or not os.path.exists(input_file):
                messagebox.showerror("Hiba", "Válassz egy létező forgatókönyv fájlt!")
                return
        else:  # batch
            input_folder = self.input_folder_path.get()
            if not input_folder or not os.path.exists(input_folder):
                messagebox.showerror("Hiba", "Válassz egy létező mappát!")
                return
        
        # Generálás indítása külön szálon
        self.is_processing = True
        self.start_btn.configure(state="disabled", text="⏳ Feldolgozás...")
        
        if mode == "single":
            thread = threading.Thread(target=self.process_file, daemon=True)
        else:
            thread = threading.Thread(target=self.process_batch, daemon=True)
        
        thread.start()
    
    def process_file(self):
        """Fájl feldolgozása (külön szálon fut)."""
        try:
            input_file = Path(self.input_file_path.get())
            output_dir = self.output_dir_path.get()
            
            self.log_message("="*60, "info")
            self.log_message("🎬 FELDOLGOZÁS INDÍTÁSA", "info")
            self.log_message("="*60, "info")
            
            # Parser választás
            if input_file.suffix.lower() == '.docx':
                parser = DocxParser(str(input_file))
                self.log_message("📖 Word dokumentum feldolgozása...", "info")
            else:
                parser = ScriptParser(str(input_file))
                self.log_message("📖 Szöveges fájl feldolgozása...", "info")
            
            # Forgatókönyv beolvasása
            parser_data = parser.parse()
            
            self.log_message(f"📌 Cím: {parser_data['metadata'].get('title', 'N/A')}", "info")
            self.log_message(f"👥 Szereplők: {len(parser_data['characters'])}", "info")
            self.log_message(f"🎬 Jelenetek: {len(parser_data['scenes'])}", "info")
            
            # Voice Manager
            voice_manager = VoiceManager()
            
            if parser_data['characters']:
                for character, description in parser_data['characters'].items():
                    voice_manager.assign_voice_by_description(character, description)
            else:
                self.log_message("⚠️  Nincs Characters szekció - név alapú hangválasztás", "warning")
                dialogues = parser.get_all_dialogues()
                unique_characters = set(d['character'] for d in dialogues)
                for character in unique_characters:
                    voice_manager.assign_voice_by_description(character, "")
            
            # Párbeszédek
            dialogues = parser.get_all_dialogues()
            total = len(dialogues)
            
            if total == 0:
                self.log_message("❌ Nincs párbeszéd a forgatókönyvben!", "error")
                return
            
            self.log_message(f"\n💬 Összes párbeszéd: {total}", "info")
            self.log_message(f"🎚️ Sebesség: {self.speed_value.get():.1f}x\n", "info")
            
            # TTS Generator
            tts = TTSGenerator(self.api_key, output_dir)
            
            # SEBESSÉG BEÁLLÍTÁSA (módosítjuk a generate_speech-et dinamikusan)
            original_generate = tts.generate_speech
            
            def custom_generate(text, voice_id, filename, model="eleven_v3"):
                # Itt módosítjuk a sebességet
                import requests
                url = f"{tts.base_url}/text-to-speech/{voice_id}"
                headers = {
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": tts.api_key
                }
                data = {
                    "text": text,
                    "model_id": model,
                    "voice_settings": {
                        "stability": 1.0,
                        "similarity_boost": 0.25,
                        "style": 0.0,
                        "use_speaker_boost": True,
                        "speed": self.speed_value.get()  # GUI-ból vesszük
                    }
                }
                
                try:
                    response = requests.post(url, json=data, headers=headers, timeout=30)
                    if response.status_code == 200:
                        filepath = os.path.join(tts.output_dir, filename)
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        return filepath
                    else:
                        return None
                except Exception:
                    return None
            
            tts.generate_speech = custom_generate
            
            # Generálás
            self.log_message("🎤 Hangfájlok generálása...\n", "info")
            
            success_count = 0
            for i, dialogue in enumerate(dialogues, 1):
                char = dialogue['character']
                text = dialogue['text']
                slide_num = dialogue['slide_number']  # Közvetlenül integer formátumban
                
                voice_id = voice_manager.get_voice_id(char)
                filename = f"{slide_num:02d}_{char}_{i:03d}.mp3"
                
                self.log_message(f"  [{i}/{total}] {filename}...", "info")
                
                result = tts.generate_speech(text, voice_id, filename)
                
                if result:
                    success_count += 1
                    self.log_message(f"        ✅ Kész", "success")
                else:
                    self.log_message(f"        ❌ Hiba", "error")
            
            # Összesítés
            self.log_message("\n" + "="*60, "info")
            self.log_message(f"✅ KÉSZ! {success_count}/{total} sikeres", "success")
            self.log_message(f"📁 Output: {output_dir}", "info")
            self.log_message("="*60, "info")
            
            messagebox.showinfo("Kész!", f"Generálás befejezve!\n\n{success_count}/{total} sikeres")
            
        except Exception as e:
            self.log_message(f"\n❌ HIBA: {str(e)}", "error")
            messagebox.showerror("Hiba", f"Feldolgozási hiba:\n{str(e)}")
        
        finally:
            self.is_processing = False
            self.start_btn.configure(state="normal", text="🚀 Generálás indítása")
    
    def process_batch(self):
        """Batch feldolgozás - teljes mappa (külön szálon fut)."""
        try:
            input_folder = Path(self.input_folder_path.get())
            output_base = self.output_dir_path.get()
            
            self.log_message("="*60, "info")
            self.log_message("🎬 BATCH FELDOLGOZÁS INDÍTÁSA", "info")
            self.log_message("="*60, "info")
            
            # Fájlok listázása
            files = sorted(list(input_folder.glob("*.txt")) + list(input_folder.glob("*.docx")))
            
            if not files:
                self.log_message("❌ Nincs .txt vagy .docx fájl a mappában!", "error")
                messagebox.showerror("Hiba", "Nincs feldolgozható fájl a kiválasztott mappában!")
                return
            
            self.log_message(f"📂 Input mappa: {input_folder}", "info")
            self.log_message(f"📁 Output mappa: {output_base}", "info")
            self.log_message(f"📄 Talált fájlok: {len(files)}", "info")
            self.log_message("", "info")
            
            # BatchProcessor inicializálása
            batch_processor = BatchProcessor(str(input_folder), output_base, self.api_key)
            
            # Feldolgozás fájlonként
            success_count = 0
            total_dialogues = 0
            
            for i, file_path in enumerate(files, 1):
                self.log_message(f"[{i}/{len(files)}]", "info")
                self.log_message("="*60, "info")
                self.log_message(f"📄 Feldolgozás: {file_path.name}", "info")
                self.log_message("="*60, "info")
                
                try:
                    # Parser választás
                    if file_path.suffix.lower() == '.docx':
                        parser = DocxParser(str(file_path))
                    else:
                        parser = ScriptParser(str(file_path))
                    
                    # Parse
                    parser_data = parser.parse()
                    
                    self.log_message(f"📌 Forgatókönyv: {parser_data['metadata'].get('title', file_path.stem)}", "info")
                    self.log_message(f"👥 Szereplők: {len(parser_data['characters'])}", "info")
                    self.log_message(f"🎬 Jelenetek: {len(parser_data['scenes'])}", "info")
                    
                    # Voice Manager
                    voice_manager = VoiceManager()
                    if parser_data['characters']:
                        for character, description in parser_data['characters'].items():
                            voice_manager.assign_voice_by_description(character, description)
                    else:
                        dialogues_temp = parser.get_all_dialogues()
                        unique_characters = set(d['character'] for d in dialogues_temp)
                        for character in unique_characters:
                            voice_manager.assign_voice_by_description(character, "")
                    
                    # Output mappa
                    output_dir = os.path.join(output_base, file_path.stem)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    self.log_message(f"📁 Output mappa: {output_dir}", "info")
                    
                    # Párbeszédek
                    dialogues = parser.get_all_dialogues()
                    self.log_message(f"💬 Párbeszédek: {len(dialogues)}", "info")
                    self.log_message("", "info")
                    
                    # TTS Generator  
                    tts = TTSGenerator(self.api_key, output_dir)
                    
                    # Generálás
                    self.log_message(f"🎬 Összesen {len(dialogues)} párbeszéd generálása...\n", "info")
                    
                    file_success = 0
                    for j, dialogue in enumerate(dialogues, 1):
                        char = dialogue['character']
                        text = dialogue['text']
                        slide_num = dialogue['slide_number']  # Közvetlenül integer formátumban
                        
                        voice_id = voice_manager.get_voice_id(char)
                        filename = f"{slide_num:02d}_{char}_{j:03d}.mp3"
                        
                        # Sebesség figyelembevételével
                        import requests
                        url = f"{tts.base_url}/text-to-speech/{voice_id}"
                        headers = {
                            "Accept": "audio/mpeg",
                            "Content-Type": "application/json",
                            "xi-api-key": tts.api_key
                        }
                        data = {
                            "text": text,
                            "model_id": "eleven_v3",
                            "voice_settings": {
                                "stability": 1.0,
                                "similarity_boost": 0.25,
                                "style": 0.0,
                                "use_speaker_boost": True,
                                "speed": self.speed_value.get()
                            }
                        }
                        
                        try:
                            response = requests.post(url, json=data, headers=headers, timeout=30)
                            if response.status_code == 200:
                                filepath = os.path.join(output_dir, filename)
                                with open(filepath, 'wb') as f:
                                    f.write(response.content)
                                file_success += 1
                                self.log_message(f"  ✅ {filename}", "success")
                            else:
                                self.log_message(f"  ❌ {filename} - Hiba: {response.status_code}", "error")
                        except Exception as e:
                            self.log_message(f"  ❌ {filename} - {str(e)}", "error")
                    
                    self.log_message(f"\n✅ Sikeres: {file_success}/{len(dialogues)}\n", "success")
                    
                    if file_success == len(dialogues):
                        success_count += 1
                    total_dialogues += file_success
                    
                except Exception as e:
                    self.log_message(f"❌ Hiba a fájl feldolgozásakor: {str(e)}", "error")
                
                self.log_message("", "info")
            
            # Összesítés
            self.log_message("="*60, "info")
            self.log_message("✅ BATCH FELDOLGOZÁS BEFEJEZVE!", "success")
            self.log_message("="*60, "info")
            self.log_message(f"📄 Összes fájl: {len(files)}", "info")
            self.log_message(f"✅ Sikeres: {success_count}", "success")
            self.log_message(f"❌ Sikertelen: {len(files) - success_count}", "error" if success_count < len(files) else "info")
            self.log_message(f"💬 Összes párbeszéd: {total_dialogues}", "info")
            self.log_message(f"📁 Output: {output_base}", "info")
            self.log_message("="*60, "info")
            
            messagebox.showinfo("Kész!", f"Batch feldolgozás befejezve!\n\n{success_count}/{len(files)} fájl sikeres\n{total_dialogues} hangfájl generálva")
            
        except Exception as e:
            self.log_message(f"\n❌ HIBA: {str(e)}", "error")
            messagebox.showerror("Hiba", f"Batch feldolgozási hiba:\n{str(e)}")
        
        finally:
            self.is_processing = False
            self.start_btn.configure(state="normal", text="🚀 Generálás indítása")


def main():
    """Alkalmazás indítása."""
    app = AutoSoundGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
