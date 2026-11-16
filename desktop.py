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
        root.geometry("900x650")
        root.minsize(650, 560)
        root.configure(bg="#f9f3e8")
        self.mode = tk.StringVar(value="Цезар")
        self.reverse = tk.BooleanVar()
        self.key = tk.StringVar(value="5")
        self.status = tk.StringVar()
        self.counter = tk.StringVar()
        self.steps = []
        self.position = 0
        self.result = ""

        banner = tk.Frame(root, bg="#f9f3e8")
        banner.pack(fill="x", padx=22, pady=12)
        pug = tk.Canvas(banner, width=98, height=84, bg="#f9f3e8", highlightthickness=0)
        pug.pack(side="left")
        pug.create_oval(5, 5, 30, 56, fill="#53362d", outline="")
        pug.create_oval(68, 5, 93, 56, fill="#53362d", outline="")
        pug.create_oval(17, 12, 81, 77, fill="#e8bc85", outline="#53362d", width=2)
        for x in (34, 59):
            pug.create_oval(x, 33, x + 7, 40, fill="#38251e", outline="")
        pug.create_oval(31, 46, 67, 69, fill="#53362d", outline="")
        pug.create_arc(40, 49, 58, 62, start=180, extent=180, outline="#fff4dd", width=2, style="arc")
        tk.Label(banner, text="Мопс і шифри", font=("Segoe UI", 30, "bold"),
                 bg="#f9f3e8", fg="#38251e").pack(side="left", padx=12)

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
        self.message = tk.Text(form, height=3, wrap="word", font=("Segoe UI", 12))
        self.message.pack(fill="x", pady=(3, 8))
        ttk.Button(form, text="Обчислити", command=self.run).pack(anchor="w")
        ttk.Label(form, textvariable=self.status, foreground="#8d4230").pack(anchor="w", pady=4)
        ttk.Label(form, text="Результат").pack(anchor="w")
        self.output = tk.Text(form, height=3, wrap="word", state="disabled", font=("Segoe UI", 12))
        self.output.pack(fill="x", pady=(3, 8))
        row = ttk.Frame(form)
        row.pack(fill="x")
        ttk.Button(row, text="← Крок", command=lambda: self.move(-1)).pack(side="left")
        ttk.Button(row, text="Крок →", command=lambda: self.move(1)).pack(side="left", padx=5)
        ttk.Label(row, textvariable=self.counter).pack(side="left", padx=8)
        ttk.Button(row, text="Зберегти TXT", command=self.save).pack(side="right")
        self.trace = tk.Text(form, height=3, wrap="word", state="disabled", font=("Consolas", 12))
        self.trace.pack(fill="both", expand=True, pady=(8, 4))
        ttk.Label(form, text="Ставісюк Олександра Сергіївна · Варіант 28").pack(anchor="w")
        self.sample()

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
            example = transform(mode, NAME, self.key.get(), False)[0]
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
        else:
            self.status.set("Готово")
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
