"""Мопс і шифри — настільна майстерня для Windows."""
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from ciphers import NAME, KEY, MESSAGE, CIPHER, substitute, vigenere, polybius
from rsa_lab import rsa


def transform(mode, text, key, reverse):
    text = text.strip()
    if not 1 <= len(text) <= 1000:
        raise ValueError("Введіть від 1 до 1000 символів.")
    if mode == "Цезар":
        shift = int(key)
        if not 0 <= shift <= 32:
            raise ValueError("Зсув має бути від 0 до 32.")
        return substitute(text, [shift], reverse)
    if mode == "Віженер ROT2":
        return vigenere(text, key, reverse)
    if mode == "Полібій":
        return polybius(text, reverse)
    if mode == "RSA":
        return rsa(text.replace("|", " "), reverse)
    raise ValueError("Оберіть алгоритм.")


class Workshop:
    def __init__(self, root):
        self.root = root
        root.title("Мопс і шифри · Варіант 28")
        root.geometry("940x720")
        root.minsize(650, 560)
        root.configure(bg="#fff3f9")
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 11), background="#fff3f9", foreground="#49243e")
        style.configure("TButton", background="#f0ddff", borderwidth=0, padding=(12, 7))
        style.map("TButton", background=[("active", "#e7c8fa")])
        style.configure("Pug.TButton", background="#a73d77", foreground="#ffffff")
        style.map("Pug.TButton", background=[("active", "#8e2d65")])
        style.configure("TEntry", fieldbackground="#ffffff", padding=4)
        style.configure("TCombobox", fieldbackground="#ffffff", padding=4)
        style.configure("TCheckbutton", background="#fff3f9")
        self.mode = tk.StringVar(value="Цезар")
        self.reverse = tk.BooleanVar()
        self.key = tk.StringVar(value="5")
        self.status = tk.StringVar()
        self.counter = tk.StringVar()
        self.steps = []
        self.position = 0
        self.result = ""

        banner = tk.Frame(root, bg="#f3ddfb")
        banner.pack(fill="x", padx=22, pady=(15, 10))
        self.pug = tk.Canvas(banner, width=161, height=135, bg="#f3ddfb", highlightthickness=0)
        self.pug.pack(side="left", padx=(18, 10))
        self.pug.bind("<Button-1>", lambda event: self.react("pet"))
        banner_text = tk.Frame(banner, bg="#f3ddfb")
        banner_text.pack(side="left", fill="x", expand=True, pady=12)
        tk.Label(banner_text, text="Мопс і шифри", font=("Segoe UI", 32, "bold"),
                 bg="#f3ddfb", fg="#49243e").pack(anchor="w")
        self.guide = tk.StringVar()
        tk.Label(banner_text, textvariable=self.guide, font=("Segoe UI", 12),
                 bg="#f3ddfb", fg="#70335b", wraplength=480, justify="left").pack(anchor="w")
        self.react("ready")

        form = ttk.Frame(root, padding=(22, 0, 22, 14))
        form.pack(fill="both", expand=True)
        controls = ttk.Frame(form)
        controls.pack(fill="x", pady=(0, 8))
        picker = ttk.Combobox(controls, state="readonly", textvariable=self.mode,
                             values=("Цезар", "Віженер ROT2", "Полібій", "RSA"), width=17)
        picker.pack(side="left")
        picker.bind("<<ComboboxSelected>>", self.select)
        ttk.Checkbutton(controls, text="Розшифрування", variable=self.reverse).pack(side="left", padx=10)
        ttk.Button(controls, text="Приклад варіанта", command=self.sample).pack(side="left")
        self.key_label = ttk.Label(form, text="Зсув або ключ")
        self.key_label.pack(anchor="w")
        self.key_input = ttk.Entry(form, textvariable=self.key)
        self.key_input.pack(fill="x", pady=(3, 8))
        ttk.Label(form, text="Вхідні дані").pack(anchor="w")
        self.message = tk.Text(form, height=3, wrap="word", bg="#ffffff", fg="#49243e", relief="flat", padx=10, pady=7, font=("Segoe UI", 12))
        self.message.pack(fill="x", pady=(3, 8))
        ttk.Button(form, text="Обчислити", style="Pug.TButton", command=self.run).pack(anchor="w")
        ttk.Label(form, textvariable=self.status, foreground="#8d4230").pack(anchor="w", pady=4)
        ttk.Label(form, text="Результат").pack(anchor="w")
        self.output = tk.Text(form, height=3, wrap="word", state="disabled", bg="#faf0ff", fg="#49243e", relief="flat", padx=10, pady=7, font=("Segoe UI", 12))
        self.output.pack(fill="x", pady=(3, 8))
        row = ttk.Frame(form)
        row.pack(fill="x")
        ttk.Button(row, text="← Крок", command=lambda: self.move(-1)).pack(side="left")
        ttk.Button(row, text="Крок →", command=lambda: self.move(1)).pack(side="left", padx=5)
        ttk.Label(row, textvariable=self.counter).pack(side="left", padx=8)
        ttk.Button(row, text="Зберегти TXT", command=self.save).pack(side="right")
        self.trace = tk.Text(form, height=3, wrap="word", state="disabled", bg="#faf0ff", fg="#49243e", relief="flat", padx=10, pady=7, font=("Consolas", 12))
        self.trace.pack(fill="both", expand=True, pady=(8, 4))
        ttk.Label(form, text="Ставісюк Олександра Сергіївна · Варіант 28").pack(anchor="w")
        self.sample()

    def react(self, mood):
        messages = {
            "ready": "Я Плюша! Обери шифр, а я покажу кожен крок.",
            "pet": "Мурк… тобто гав! Спробуй «Приклад варіанта».",
            "success": "Гав! Готово. Гортай кроки або збережи протокол.",
            "error": "Ой, лапка зісковзнула. Підказка під кнопкою.",
        }
        self.guide.set(messages[mood])
        c = self.pug
        c.delete("all")
        c.create_oval(20, 6, 142, 128, fill="#fff6fc", outline="")
        c.create_oval(28, 88, 134, 133, fill="#f4b9d7", outline="")
        c.create_oval(16, 28, 55, 95, fill="#5b3942", outline="")
        c.create_oval(107, 28, 146, 95, fill="#5b3942", outline="")
        c.create_oval(30, 19, 132, 116, fill="#efc797", outline="#9a655d", width=2)
        for x in (52, 100):
            if mood in ("success", "pet"):
                c.create_arc(x-6, 51, x+8, 68, start=0, extent=180, style="arc", outline="#432733", width=3)
            else:
                c.create_oval(x-5, 51, x+7, 65, fill="#432733", outline="")
                c.create_oval(x-1, 53, x+2, 56, fill="#fff9fd", outline="")
            c.create_oval(x-10, 71, x+9, 80, fill="#e9a2a8", outline="")
        c.create_arc(67, 28, 94, 46, start=20, extent=140, style="arc", outline="#bc8a71", width=2)
        c.create_oval(58, 67, 104, 105, fill="#694655", outline="")
        c.create_oval(73, 72, 90, 81, fill="#392632", outline="")
        if mood == "error":
            c.create_oval(77, 87, 86, 95, outline="#ffe6ed", width=2)
        else:
            c.create_arc(69, 77, 94, 95, start=180, extent=180, style="arc", outline="#ffe6ed", width=2)
        c.create_polygon(106, 19, 97, 9, 97, 29, 106, 23, 117, 30, 117, 9, fill="#b44783")
        c.create_oval(102, 16, 112, 26, fill="#f180b2", outline="")
        if mood in ("success", "pet"):
            c.create_text(145, 18, text="♥", fill="#ba4486", font=("Segoe UI", 15, "bold"))

    @staticmethod
    def show(widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def select(self, event=None):
        self.key.set("5" if self.mode.get() == "Цезар" else KEY)
        self.key_input.configure(state="normal" if self.mode.get() in ("Цезар", "Віженер ROT2") else "disabled")
        self.sample()

    def sample(self):
        mode = self.mode.get()
        if mode == "RSA":
            example = CIPHER if self.reverse.get() else MESSAGE
        elif self.reverse.get():
            try:
                example = transform(mode, NAME, self.key.get(), False)[0]
            except ValueError as error:
                self.status.set(str(error))
                self.react("error")
                return
        else:
            example = NAME
        self.message.delete("1.0", "end")
        self.message.insert("1.0", example)

    def run(self):
        try:
            self.result, self.steps = transform(
                self.mode.get(), self.message.get("1.0", "end"), self.key.get(), self.reverse.get()
            )
        except ValueError as error:
            self.result, self.steps = "", []
            self.status.set(str(error))
            self.react("error")
        else:
            self.status.set("Готово")
            self.react("success")
        self.position = 0
        self.show(self.output, self.result)
        self.move(0)

    def move(self, offset):
        if not self.steps:
            self.counter.set("")
            self.show(self.trace, "")
            return
        self.position = min(max(self.position + offset, 0), len(self.steps) - 1)
        self.counter.set(f"{self.position + 1} / {len(self.steps)}")
        self.show(self.trace, self.steps[self.position])

    def save(self):
        if not self.steps:
            self.status.set("Спочатку виконайте обчислення.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текст", "*.txt")])
        if path:
            try:
                Path(path).write_text(self.result + "\n\n" + "\n".join(self.steps), encoding="utf-8")
            except OSError as error:
                self.status.set(str(error))


def main():
    root = tk.Tk()
    Workshop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
