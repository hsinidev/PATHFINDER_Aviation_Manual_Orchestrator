import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

import ingest
import rag_engine

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PATHFINDER - Aviation Manual Orchestrator")
        self.geometry("1400x950")
        
        ctk.set_appearance_mode("dark")
        self.BG_COLOR = "#0b0f19"
        self.CONTAINER_BG = "#161f30"
        self.ACCENT_COLOR = "#06b6d4"
        self.ACCENT_HOVER = "#0891b2"
        self.SECONDARY_COLOR = "#10b981"
        self.ALERT_COLOR = "#ef4444"
        self.TEXT_COLOR = "#f8fafc"
        self.BORDER_COLOR = "#1e293b"

        self.configure(fg_color=self.BG_COLOR)

        self.engine = rag_engine.RAGEngine()
        self.selected_model = ctk.StringVar(value="llava")
        self.is_indexing = False

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.create_sidebar()
        self.create_center_canvas()
        self.create_right_panel()
        self.create_bottom_chat()

        self.refresh_library()
        self.render_formula(r"\text{Glide Ratio} = \frac{C_L}{C_D} = \frac{\text{Lift}}{\text{Drag}}")

        # --- Persistent Contact Button (Bottom-Right) ---
        self.floating_contact_btn = ctk.CTkButton(
            self, text="👤", width=40, height=40, corner_radius=20,
            fg_color="gray20", hover_color=self.ACCENT_COLOR,
            command=self.open_contact_modal,
            font=ctk.CTkFont(size=18),
            border_width=1, border_color=self.BORDER_COLOR
        )
        self.floating_contact_btn.place(relx=0.98, rely=0.97, anchor="se")
        
        # Load profile photo for modal
        try:
            self.base_profile = Image.open("profile.png").convert("RGBA")
        except:
            self.base_profile = None

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color=self.CONTAINER_BG, border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        title_label = ctk.CTkLabel(self.sidebar, text="SYSTEM PANEL", font=ctk.CTkFont(family="Inter", size=20, weight="bold"), text_color=self.ACCENT_COLOR)
        title_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.section_label(self.sidebar, "MODEL ORCHESTRATION")
        self.model_menu = ctk.CTkOptionMenu(self.sidebar, values=["llava", "gemma3"], variable=self.selected_model, fg_color=self.ACCENT_COLOR, button_hover_color=self.ACCENT_HOVER)
        self.model_menu.pack(pady=5, padx=20, fill="x")

        # Dynamic Ollama List Button
        self.ollama_list_btn = ctk.CTkButton(
            self.sidebar, text="🔄 OLLAMA LIST", command=self.fetch_ollama_models,
            fg_color="#34495e", hover_color="#2c3e50", height=30
        )
        self.ollama_list_btn.pack(pady=5, padx=20, fill="x")

        self.section_label(self.sidebar, "KNOWLEDGE BASE")
        self.index_btn = ctk.CTkButton(self.sidebar, text="Index PDF Documents", command=self.run_ingestion, fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER)
        self.index_btn.pack(pady=5, padx=20, fill="x")
        
        self.section_label(self.sidebar, "INDEXED LIBRARY")
        self.library_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", border_width=1, border_color=self.BORDER_COLOR)
        self.library_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
    def create_center_canvas(self):
        self.center_frame = ctk.CTkFrame(self, fg_color=self.BG_COLOR, corner_radius=0)
        self.center_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.center_frame.grid_rowconfigure(0, weight=0)
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)

        self.latex_frame = ctk.CTkFrame(self.center_frame, fg_color=self.CONTAINER_BG, border_width=1, border_color=self.BORDER_COLOR, height=220)
        self.latex_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.latex_title = ctk.CTkLabel(self.latex_frame, text="VISUAL EVIDENCE CANVAS", font=ctk.CTkFont(size=10, weight="bold"), text_color=self.SECONDARY_COLOR)
        self.latex_title.pack(pady=(10, 5), padx=10, anchor="w")
        self.canvas_widget = None

        self.reader_frame = ctk.CTkFrame(self.center_frame, fg_color=self.CONTAINER_BG, border_width=1, border_color=self.BORDER_COLOR)
        self.reader_frame.grid(row=1, column=0, sticky="nsew")
        self.reader_title = ctk.CTkLabel(self.reader_frame, text="DOCUMENT READER", font=ctk.CTkFont(size=10, weight="bold"), text_color="gray55")
        self.reader_title.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.reader_display = ctk.CTkTextbox(self.reader_frame, fg_color="transparent", font=ctk.CTkFont(size=14), wrap="word", text_color=self.TEXT_COLOR)
        self.reader_display.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.reader_display.configure(state="disabled")

    def create_right_panel(self):
        self.right_panel = ctk.CTkFrame(self, width=380, fg_color=self.CONTAINER_BG, border_width=1, border_color=self.BORDER_COLOR, corner_radius=0)
        self.right_panel.grid(row=0, column=2, rowspan=2, sticky="nsew")
        
        self.section_label(self.right_panel, "FORMULAS / LOGS")
        self.formula_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent", border_width=1, border_color=self.BORDER_COLOR, height=350)
        self.formula_scroll.pack(fill="x", padx=20, pady=(5, 20))
        
        self.section_label(self.right_panel, "CITATIONS INDEX")
        self.citation_scroll = ctk.CTkScrollableFrame(self.right_panel, fg_color="transparent", border_width=1, border_color=self.BORDER_COLOR)
        self.citation_scroll.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    def create_bottom_chat(self):
        self.chat_frame = ctk.CTkFrame(self, fg_color=self.CONTAINER_BG, border_width=1, border_color=self.BORDER_COLOR, corner_radius=15)
        self.chat_frame.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 20))
        
        self.chat_display = ctk.CTkTextbox(self.chat_frame, height=180, fg_color="transparent", font=ctk.CTkFont(size=13), wrap="word", text_color=self.TEXT_COLOR)
        self.chat_display.pack(fill="x", padx=15, pady=10)
        self.chat_display.insert("end", "System Status: Online. Index documentation to query.\n\n")
        self.chat_display.configure(state="disabled")
        
        input_line = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        input_line.pack(fill="x", padx=15, pady=(0, 15))
        
        self.chat_entry = ctk.CTkEntry(input_line, placeholder_text="Enter diagnostic query...", height=40, fg_color=self.BG_COLOR, border_color=self.BORDER_COLOR)
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_entry.bind("<Return>", lambda e: self.submit_query())
        
        self.submit_btn = ctk.CTkButton(input_line, text="Query AI", width=120, height=40, command=self.submit_query, fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER)
        self.submit_btn.pack(side="right")

    def section_label(self, parent, text):
        lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=11, weight="bold"), text_color="gray55")
        lbl.pack(anchor="w", pady=(15, 5), padx=20)
        return lbl

    def refresh_library(self):
        for child in self.library_scroll.winfo_children():
            child.destroy()
        papers = self.engine.list_indexed_papers()
        if not papers:
            empty_lbl = ctk.CTkLabel(self.library_scroll, text="No items indexed.", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray45")
            empty_lbl.pack(pady=20)
            return
        for paper_file, meta in papers.items():
            btn = ctk.CTkButton(
                self.library_scroll, text=f"📄 {paper_file[:22]}\n{meta['author']} ({meta['year']})",
                anchor="w", fg_color="transparent", text_color=self.TEXT_COLOR, hover_color=self.BORDER_COLOR, height=45,
                command=lambda f=paper_file: self.load_paper_content(f)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def load_paper_content(self, filename):
        self.reader_display.configure(state="normal")
        self.reader_display.delete("1.0", "end")
        try:
            results = self.engine.collection.get(where={"source": filename}, include=["documents", "metadatas"])
            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])
            chunk_data = []
            for doc, meta in zip(documents, metadatas):
                if meta.get("type") == "text":
                    chunk_data.append((meta.get("chunk_index", 0), doc))
            chunk_data.sort()
            full_text = "\n\n".join([text for _, text in chunk_data])
            self.reader_display.insert("end", full_text if full_text else "No body text matches.")
        except Exception as e:
            self.reader_display.insert("end", f"Error: {e}")
        self.reader_display.configure(state="disabled")

    def render_formula(self, latex_str):
        if not HAS_MATPLOTLIB:
            if self.canvas_widget:
                self.canvas_widget.destroy()
            fallback_label = ctk.CTkLabel(self.latex_frame, text=latex_str, font=ctk.CTkFont(family="Consolas", size=13), text_color=self.SECONDARY_COLOR)
            fallback_label.pack(pady=20, fill="both", expand=True)
            self.canvas_widget = fallback_label
            return

        if self.canvas_widget:
            self.canvas_widget.destroy()

        formatted_latex = latex_str if latex_str.startswith("$") else f"${latex_str}$"
        fig = Figure(figsize=(6, 1.8), dpi=100)
        fig.patch.set_facecolor("#ffffff" if self.TEXT_COLOR == "#1c1917" else self.CONTAINER_BG)
        ax = fig.add_subplot(111)
        ax.axis("off")
        try:
            ax.text(0.5, 0.5, formatted_latex, size=15, ha="center", va="center", color=self.TEXT_COLOR)
        except Exception as e:
            ax.text(0.5, 0.5, "Formula Render", size=10, ha="center", va="center")
            
        canvas = FigureCanvasTkAgg(fig, master=self.latex_frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        canvas.draw()

    def run_ingestion(self):
        if self.is_indexing:
            return
        pub_directory = filedialog.askdirectory(title="Select Documents Folder")
        if not pub_directory:
            return
        self.is_indexing = True
        self.index_btn.configure(state="disabled", text="Indexing...")
        self.log_chat("Scanning and indexing documents folder...")
        threading.Thread(target=self._ingest_thread, args=(pub_directory,), daemon=True).start()

    def _ingest_thread(self, path):
        try:
            ingestor = ingest.Ingestor()
            results = ingestor.ingest_directory(path)
            success_count = sum(1 for _, res in results if res.get("success", False))
            self.after(0, lambda: self._ingest_completed(success_count, len(results)))
        except Exception as e:
            self.after(0, lambda: self._ingest_failed(e))

    def _ingest_completed(self, success_count, total_count):
        self.is_indexing = False
        self.index_btn.configure(state="normal", text="Index PDF Documents")
        self.log_chat(f"Indexing completed: {success_count}/{total_count} files processed.")
        self.refresh_library()

    def _ingest_failed(self, error):
        self.is_indexing = False
        self.index_btn.configure(state="normal", text="Index PDF Documents")
        self.log_chat(f"Error: {error}")

    def submit_query(self):
        query = self.chat_entry.get().strip()
        if not query:
            return
        self.chat_entry.delete(0, "end")
        self.log_chat(f"User: {query}", is_user=True)
        self.submit_btn.configure(state="disabled", text="Consulting...")
        threading.Thread(target=self._query_thread, args=(self.selected_model.get(), query), daemon=True).start()

    def _query_thread(self, model, query):
        try:
            res = self.engine.generate_response(model_name=model, query=query)
            self.after(0, lambda: self._query_completed(res))
        except Exception as e:
            self.after(0, lambda: self._query_failed(e))

    def _query_completed(self, result):
        self.submit_btn.configure(state="normal", text="Query AI")
        self.log_chat(result['response'])
        self.update_extracted_formulas(result.get("extracted_formulas", []))
        self.update_citations(result.get("citations", []))

    def _query_failed(self, error):
        self.submit_btn.configure(state="normal", text="Query AI")
        self.log_chat(f"Error: {error}")

    def log_chat(self, message, is_user=False):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f">>> {message}\n\n" if is_user else f"{message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def update_extracted_formulas(self, formulas):
        for child in self.formula_scroll.winfo_children():
            child.destroy()
        if not formulas:
            empty_lbl = ctk.CTkLabel(self.formula_scroll, text="No formulas in context.", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray45")
            empty_lbl.pack(pady=15)
            return
        for latex, source in formulas:
            disp = latex[:35] + "..." if len(latex) > 38 else latex
            btn = ctk.CTkButton(
                self.formula_scroll, text=f"∑  {disp}",
                anchor="w", fg_color="transparent", text_color=self.SECONDARY_COLOR, hover_color=self.BORDER_COLOR, height=35,
                command=lambda l=latex: self.render_formula(l)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def update_citations(self, citations):
        for child in self.citation_scroll.winfo_children():
            child.destroy()
        if not citations:
            empty_lbl = ctk.CTkLabel(self.citation_scroll, text="No citations in context.", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray45")
            empty_lbl.pack(pady=15)
            return
        for citation in citations:
            lbl = ctk.CTkLabel(self.citation_scroll, text=f"• {citation}", anchor="w", text_color=self.SECONDARY_COLOR, justify="left", wrap="word")
            lbl.pack(fill="x", pady=4, padx=10)

    # --- Sync Ollama Local Models (Absolute Path Solution) ---
    def fetch_ollama_models(self):
        try:
            import subprocess
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Resolve absolute program path to bypass local environment PATH resolution failures
            ollama_cmd = "ollama"
            if sys.platform == "win32":
                local_app_data = os.getenv("LOCALAPPDATA", "")
                default_path = os.path.join(local_app_data, "Programs", "Ollama", "ollama.exe")
                if os.path.exists(default_path):
                    ollama_cmd = default_path
            
            result = subprocess.check_output(
                [ollama_cmd, "list"], 
                stderr=subprocess.STDOUT, 
                text=True,
                startupinfo=startupinfo
            )
            lines = result.splitlines()
            models = []
            if len(lines) > 1:
                for line in lines[1:]:
                    parts = line.split()
                    if parts:
                        models.append(parts[0])
            
            if models:
                self.model_menu.configure(values=models)
                self.model_menu.set(models[0])
                self.log_chat(f"SYSTEM: Ollama sync completed: {len(models)} models detected.")
            else:
                self.log_chat("SYSTEM: Ollama service running, but no local models found.")
        except Exception as e:
            self.log_chat(f"SYSTEM: Local Ollama service is offline or not installed. Error: {e}")

    # --- Developer Profile Modal (with Light Background inside Circle) ---
    def open_contact_modal(self):
        from PIL import ImageDraw, ImageOps
        modal = ctk.CTkToplevel(self)
        modal.title("Developer Information")
        modal.geometry("380x570")
        modal.attributes("-topmost", True)
        modal.resizable(False, False)
        modal.configure(fg_color="#0d1117" if self.TEXT_COLOR == "#f8fafc" else "#fafaf9")
        
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (380 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (570 // 2)
        modal.geometry(f"+{x}+{y}")

        if self.base_profile:
            size = (140, 140)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)
            
            bg = Image.new("RGBA", size, "#ffffff")
            profile_img = ImageOps.fit(self.base_profile, size, centering=(0.5, 0.5))
            bg.paste(profile_img, (0, 0), profile_img)
            bg.putalpha(mask)
            
            photo = ctk.CTkImage(light_image=bg, dark_image=bg, size=size)
            img_label = ctk.CTkLabel(modal, image=photo, text="")
            img_label.image = photo
            img_label.pack(pady=(30, 20))

        info_frame = ctk.CTkFrame(modal, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=30)

        name_label = ctk.CTkLabel(info_frame, text="HSINI MOHAMED", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.ACCENT_COLOR)
        name_label.pack()

        title_label = ctk.CTkLabel(info_frame, text="Enterprise Systems Architect", font=ctk.CTkFont(size=14), text_color="gray70")
        title_label.pack(pady=(0, 20))

        self.create_modal_button(info_frame, "WhatsApp: +212 658 029 773", "https://wa.me/212658029773", "#2ecc71")
        self.create_modal_button(info_frame, "Email: hsini.moahmed@gmail.com", "mailto:hsini.moahmed@gmail.com", "#e74c3c")
        self.create_modal_button(info_frame, "Website: hsini.dev", "https://hsini.dev", self.ACCENT_COLOR)
        self.create_modal_button(info_frame, "LinkedIn Profile", "https://www.linkedin.com/in/moahmed-hsini-6059281a1/", "#2980b9")
        self.create_modal_button(info_frame, "GitHub Repository", "https://github.com/hsinimoahmed", "#34495e")

    def create_modal_button(self, parent, text, link, color):
        import webbrowser
        btn = ctk.CTkButton(
            parent, text=text, fg_color=color, height=40,
            command=lambda: webbrowser.open(link),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        btn.pack(pady=6, fill="x")

if __name__ == "__main__":
    app = App()
    app.mainloop()
