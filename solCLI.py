import customtkinter as ctk
from tkinter import filedialog
import subprocess, threading, os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class C3SolCLI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("C3 SOL CLI 2025 — Vanity Grinder")
        self.geometry("1100x650")
        self.configure(fg_color="#000000")

        # === sidebar ===
        self.sidebar = ctk.CTkFrame(self, corner_radius=12, width=240)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="⚡ C3 SOL CLI 2025 ⚡", font=("Consolas", 22, "bold"), text_color="#14F195").pack(pady=(20,10))
        ctk.CTkLabel(self.sidebar, text="Vanity Key Grinder", text_color="#00FFA3", font=("Consolas", 14, "bold")).pack(pady=(5,15))

        # inputs
        self.start_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Starts With (ex: SOL)", text_color="#14F195")
        self.start_entry.pack(pady=5, fill="x", padx=10)
        self.end_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ends With (optional)", text_color="#14F195")
        self.end_entry.pack(pady=5, fill="x", padx=10)
        self.qty_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Quantity (ex: 5)", text_color="#14F195")
        self.qty_entry.pack(pady=5, fill="x", padx=10)

        self.ignore_case = ctk.CTkCheckBox(self.sidebar, text="Ignore Case", text_color="#00FFA3")
        self.ignore_case.pack(pady=5)

        self.btn_grind = ctk.CTkButton(self.sidebar, text="🚀  Start Grinding", fg_color="#111111", hover_color="#00FFA3", text_color="#14F195", command=self.start_grind)
        self.btn_grind.pack(pady=(10,20), fill="x", padx=10)

        # keypair selector
        self.keypair_path = None
        self.keypair_btn = ctk.CTkButton(self.sidebar, text="⚙️  Set Keypair", command=self.choose_keypair, fg_color="#111111", hover_color="#00FFA3", text_color="#14F195")
        self.keypair_btn.pack(pady=5, fill="x", padx=10)

        # network toggle
        self.net = "mainnet-beta"
        self.network_btn = ctk.CTkButton(self.sidebar, text="🌐  Toggle Network (Mainnet)", command=self.toggle_network, fg_color="#111111", hover_color="#00FFA3", text_color="#14F195")
        self.network_btn.pack(pady=5, fill="x", padx=10)

        # === console ===
        self.console = ctk.CTkTextbox(self, font=("Consolas", 12), text_color="#00FFA3", fg_color="#050505")
        self.console.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.log("🚀 Welcome to C3 SOL CLI 2025\nUse the sidebar to grind custom Solana vanity keys.\n")

        # progress bar
        self.progress = ctk.CTkProgressBar(self.sidebar)
        self.progress.pack(pady=10, fill="x", padx=10)
        self.progress.set(0)

    # === helpers ===
    def log(self, text):
        self.console.insert("end", text + "\n")
        self.console.see("end")

    def run_stream(self, cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            self.log(line.strip())
        process.wait()
        return process.returncode

    # === features ===
    def start_grind(self):
        prefix = self.start_entry.get().strip()
        suffix = self.end_entry.get().strip()
        qty = self.qty_entry.get().strip() or "1"
        ignore = "--ignore-case" if self.ignore_case.get() else ""
        parts = []

        if prefix:
            parts.append(f"--starts-with {prefix}:{qty}")
        if suffix:
            parts.append(f"--ends-with {suffix}:{qty}")
        if not parts:
            self.log("❌ Please enter a prefix or suffix to grind.")
            return

        command = f"solana-keygen grind {ignore} {' '.join(parts)}"
        self.log(f"🔮 Running: {command}")
        self.progress.set(0)
        threading.Thread(target=self._grind_thread, args=(command,)).start()

    def _grind_thread(self, command):
        self.progress.set(0.1)
        self.run_stream(command)
        self.progress.set(1)
        self.log("✨ Grind complete. Keys saved to current directory.")

    def choose_keypair(self):
        path = filedialog.askopenfilename(title="Select Keypair JSON")
        if path:
            self.keypair_path = path
            cmd = f"solana config set --keypair {path}"
            self.log(f"⚙️ Setting keypair: {path}")
            threading.Thread(target=lambda: self.run_stream(cmd)).start()

    def toggle_network(self):
        self.net = "devnet" if self.net == "mainnet-beta" else "mainnet-beta"
        cmd = f"solana config set --url https://api.{self.net}.solana.com"
        self.network_btn.configure(text=f"🌐  Toggle Network ({'Devnet' if self.net=='devnet' else 'Mainnet'})")
        self.log(f"🌐 Switching to {self.net} ...")
        threading.Thread(target=lambda: self.run_stream(cmd)).start()

if __name__ == "__main__":
    app = C3SolCLI()
    app.mainloop()
