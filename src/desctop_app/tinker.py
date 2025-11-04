import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

from cryptall_2.encode_decode import encode_file, decode_file

DEFAULT_SEED = 0


class EncoderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Encoder/Decoder - Professional Edition")
        self.geometry("900x700")
        self.configure(bg="white")

        self.create_menu()
        self.create_main_page()

    def create_menu(self):
        menubar = tk.Menu(self, bg="black", fg="white", activebackground="gray20")
        nav_menu = tk.Menu(menubar, tearoff=0, bg="white", fg="black")

        nav_menu.add_command(label="Main Page", command=self.show_main)
        nav_menu.add_command(label="Documentation", command=self.show_docs)
        nav_menu.add_command(label="About", command=self.show_about)

        menubar.add_cascade(label="Navigate", menu=nav_menu)
        self.config(menu=menubar)

    def clear_frame(self):
        for widget in self.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()

    def show_main(self):
        self.clear_frame()
        self.create_main_page()

    def show_docs(self):
        self.clear_frame()
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=50, pady=50)

        title = tk.Label(frame, text="Documentation", font=("Arial", 24, "bold"), bg="white")
        title.pack(pady=10)

        content = tk.Label(
            frame,
            text=(
                "This application allows you to encode and decode files.\n\n"
                "Features:\n"
                "• Select any file for processing\n"
                "• Choose output destination\n"
                "• Encode files for security\n"
                "• Decode previously encoded files\n"
                "• Real-time status updates\n\n"
                "Use the main page to process your files."
            ),
            justify="left",
            bg="white",
        )
        content.pack(pady=20, anchor="w")

    def show_about(self):
        self.clear_frame()
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=50, pady=50)

        title = tk.Label(frame, text="About", font=("Arial", 24, "bold"), bg="white")
        title.pack(pady=10)

        content = tk.Label(
            frame,
            text=(
                "File Encoder/Decoder Application\n\n"
                "Version: 2.0\n"
                "Built with: Tkinter\n\n"
                "This application provides a simple and intuitive interface\n"
                "for encoding and decoding files using custom algorithms.\n\n"
                "Features a clean black and white design for\n"
                "professional appearance and ease of use."
            ),
            justify="left",
            bg="white",
        )
        content.pack(pady=20, anchor="w")

    def create_main_page(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        title = tk.Label(
            frame,
            text="File Encoder/Decoder",
            font=("Arial", 32, "bold"),
            bg="white",
            fg="black",
        )
        title.pack(pady=10)

        # File Selection
        file_group = ttk.LabelFrame(frame, text="File Selection")
        file_group.pack(fill="x", pady=10)

        self.file_var = tk.StringVar()
        entry_file = ttk.Entry(file_group, textvariable=self.file_var)
        entry_file.pack(fill="x", padx=10, pady=5)

        btn_file = ttk.Button(file_group, text="Select File", command=self.select_file)
        btn_file.pack(padx=10, pady=5)

        # Seed input
        seed_group = ttk.LabelFrame(frame, text="Configuration")
        seed_group.pack(fill="x", pady=10)

        self.seed_var = tk.StringVar()
        entry_seed = ttk.Entry(seed_group, textvariable=self.seed_var)
        entry_seed.insert(0, str(DEFAULT_SEED))
        entry_seed.pack(fill="x", padx=10, pady=5)

        # Save Path
        save_group = ttk.LabelFrame(frame, text="Output Destination")
        save_group.pack(fill="x", pady=10)

        self.save_var = tk.StringVar()
        entry_save = ttk.Entry(save_group, textvariable=self.save_var)
        entry_save.pack(fill="x", padx=10, pady=5)

        btn_save = ttk.Button(save_group, text="Select Save Path", command=self.select_save)
        btn_save.pack(padx=10, pady=5)

        # Action Buttons
        action_group = ttk.LabelFrame(frame, text="Actions")
        action_group.pack(fill="x", pady=10)

        btn_encode = ttk.Button(action_group, text="[ENCODE] Encode File", command=self.encode_action)
        btn_decode = ttk.Button(action_group, text="[DECODE] Decode File", command=self.decode_action)
        btn_swap = ttk.Button(action_group, text="Swap [ENCODE]<->[DECODE]", command=self.swap_paths)

        btn_encode.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        btn_decode.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        btn_swap.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # Status
        self.status_box = tk.Text(frame, height=8, wrap="word", bg="#f5f5f5", relief="solid", borderwidth=1)
        self.status_box.pack(fill="both", expand=True, pady=10)

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)

    # -------------- Utility Methods ----------------
    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            self.file_var.set(file_path)
            self.update_status(f"[+] Selected file: {file_path}")

    def select_save(self):
        save_path = filedialog.asksaveasfilename(title="Select save path")
        if save_path:
            self.save_var.set(save_path)
            self.update_status(f"[+] Save path set: {save_path}")

    def swap_paths(self):
        file_path, save_path = self.file_var.get(), self.save_var.get()
        if not file_path or not save_path:
            return
        self.file_var.set(save_path)
        self.save_var.set(file_path)
        self.update_status(f"[_] Swapped paths: {save_path} <-> {file_path}")

    def update_status(self, text):
        self.status_box.insert("end", text + "\n")
        self.status_box.see("end")

    def validate_inputs(self):
        file_path = self.file_var.get()
        save_path = self.save_var.get()

        if not os.path.exists(file_path):
            messagebox.showwarning("Invalid Input", f"Input file [{file_path}] does not exist.")
            return None, None, None

        if file_path == save_path:
            messagebox.showwarning("Invalid Input", "Cannot overwrite the same file. Choose another save path.")
            return None, None, None

        seed_text = self.seed_var.get().strip()
        seed = int(seed_text) if seed_text.isdigit() else DEFAULT_SEED

        return file_path, save_path, seed

    # -------------- Encoding / Decoding ----------------
    def encode_action(self):
        file_path, save_path, seed = self.validate_inputs()
        if not file_path:
            return
        threading.Thread(target=self.run_encode, args=(file_path, save_path, seed), daemon=True).start()

    def decode_action(self):
        file_path, save_path, seed = self.validate_inputs()
        if not file_path:
            return
        threading.Thread(target=self.run_decode, args=(file_path, save_path, seed), daemon=True).start()

    def run_encode(self, file_path, save_path, seed):
        self.progress.start(10)
        try:
            encode_file(file_path, save_path, seed)
            self.update_status(f"[ENCODED] {file_path} -> {save_path} (seed={seed})")
            messagebox.showinfo("Success", f"File encoded successfully!\nSeed: {seed}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status(f"[ERROR] {e}")
        finally:
            self.progress.stop()

    def run_decode(self, file_path, save_path, seed):
        self.progress.start(10)
        try:
            decode_file(file_path, save_path, seed)
            self.update_status(f"[DECODED] {file_path} -> {save_path} (seed={seed})")
            messagebox.showinfo("Success", f"File decoded successfully!\nSeed: {seed}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.update_status(f"[ERROR] {e}")
        finally:
            self.progress.stop()


if __name__ == "__main__":
    app = EncoderApp()
    app.mainloop()
