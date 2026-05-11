import tkinter as tk
from tkinter import filedialog, ttk


class ModernTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Text Editor")
        self.root.geometry("1000x650")
        self.root.minsize(700, 500)

        self.base_font_family = "Segoe UI"
        self.base_font_size = 12
        self.base_font = (self.base_font_family, self.base_font_size)
        self.dark_mode = False
        self.find_window = None
        self.replace_window = None

        self.setup_colors()
        self.create_menu_bar()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        self.bind_hotkeys()
        self.apply_theme()

    def setup_colors(self):
        self.bg_light = "#f0f0f0"
        self.text_bg_light = "#ffffff"
        self.text_fg_light = "#2c3e50"
        self.toolbar_bg_light = "#e0e0e0"

        self.bg_dark = "#2d2d2d"
        self.text_bg_dark = "#1e1e1e"
        self.text_fg_dark = "#d4d4d4"
        self.toolbar_bg_dark = "#3c3c3c"

        self.accent = "#3498db"
        self.root.configure(bg=self.bg_light)

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Очистить", command=self.clear_text)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Найти", command=self.open_find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Заменить", command=self.open_replace, accelerator="Ctrl+H")

        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=theme_menu)
        theme_menu.add_command(label="Светлая тема", command=self.light_theme)
        theme_menu.add_command(label="Темная тема", command=self.dark_theme)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg=self.toolbar_bg_light, height=40)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.create_btn("📂 Открыть", self.open_file)
        self.create_btn("💾 Сохранить", self.save_file)
        self.create_btn("🗑 Очистить", self.clear_text)

        tk.Frame(self.toolbar, width=2, bg="#999").pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.create_btn("🔍 Найти", self.open_find)
        self.create_btn("🔄 Заменить", self.open_replace)

        tk.Frame(self.toolbar, width=2, bg="#999").pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.create_btn("B", self.make_bold, width=3, font=("Segoe UI", 10, "bold"))
        self.create_btn("I", self.make_italic, width=3, font=("Segoe UI", 10, "italic"))
        self.create_btn("U", self.make_underline, width=3, font=("Segoe UI", 10, "underline"))

        tk.Frame(self.toolbar, width=2, bg="#999").pack(side=tk.LEFT, padx=5, fill=tk.Y)

        tk.Label(self.toolbar, text="Шрифт:", bg=self.toolbar_bg_light,
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 5))
        self.font_family_var = tk.StringVar(value=self.base_font_family)
        self.font_combo = ttk.Combobox(
            self.toolbar, textvariable=self.font_family_var,
            values=["Segoe UI", "Arial", "Courier New", "Verdana"],
            state="readonly", width=12
        )
        self.font_combo.pack(side=tk.LEFT, padx=5)
        self.font_combo.bind("<<ComboboxSelected>>", self.change_font)

        tk.Label(self.toolbar, text="Размер:", bg=self.toolbar_bg_light,
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.font_size_var = tk.StringVar(value=str(self.base_font_size))
        self.size_combo = ttk.Combobox(
            self.toolbar, textvariable=self.font_size_var,
            values=["10", "11", "12", "14", "16", "18", "20", "24"],
            state="readonly", width=5
        )
        self.size_combo.pack(side=tk.LEFT, padx=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.change_font)

        tk.Frame(self.toolbar, width=2, bg="#999").pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.theme_btn = tk.Button(
            self.toolbar, text="🌙", font=("Segoe UI", 12),
            bg=self.toolbar_bg_light, fg=self.text_fg_light,
            bd=0, padx=15, cursor="hand2", command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)

    def create_btn(self, text, command, width=None, font=None):
        btn = tk.Button(
            self.toolbar,
            text=text,
            command=command,
            bg=self.toolbar_bg_light,
            fg=self.text_fg_light,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            font=font if font else ("Segoe UI", 10),
            width=width
        )
        btn.pack(side=tk.LEFT, padx=2)
        return btn

    def create_text_area(self):
        frame = tk.Frame(self.root, bg=self.accent, padx=2, pady=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = tk.Scrollbar(frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.text = tk.Text(
            frame, wrap=tk.WORD, undo=True, font=self.base_font,
            bg=self.text_bg_light, fg=self.text_fg_light,
            insertbackground=self.accent, relief=tk.FLAT,
            padx=15, pady=15, selectbackground=self.accent,
            selectforeground="white",
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.text.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.text.yview)
        scroll_x.config(command=self.text.xview)

        self.text.tag_configure("bold", font=(self.base_font_family, self.base_font_size, "bold"))
        self.text.tag_configure("italic", font=(self.base_font_family, self.base_font_size, "italic"))
        self.text.tag_configure("underline", font=(self.base_font_family, self.base_font_size, "underline"))
        self.text.tag_configure("found", background="yellow")

    def create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=self.accent, height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            self.status_bar, text="Готов", bg=self.accent,
            fg="white", font=("Segoe UI", 9), padx=10
        )
        self.status_label.pack(side=tk.LEFT)

        self.cursor_label = tk.Label(
            self.status_bar, text="Строка 1, Столбец 1",
            bg=self.accent, fg="white", font=("Segoe UI", 9), padx=10
        )
        self.cursor_label.pack(side=tk.RIGHT)

        self.text.bind("<KeyRelease>", self.update_cursor)
        self.text.bind("<ButtonRelease-1>", self.update_cursor)

    def update_cursor(self, event=None):
        pos = self.text.index(tk.INSERT)
        line, col = pos.split('.')
        self.cursor_label.config(text=f"Строка {line}, Столбец {int(col) + 1}")

    def update_status(self, msg):
        self.status_label.config(text=msg)
        self.root.after(2000, lambda: self.status_label.config(text="Готов"))

    def make_bold(self):
        self.apply_format("bold")

    def make_italic(self):
        self.apply_format("italic")

    def make_underline(self):
        self.apply_format("underline")

    def apply_format(self, tag):
        try:
            if self.text.tag_ranges("sel"):
                start = self.text.index("sel.first")
                end = self.text.index("sel.last")
                if tag in self.text.tag_names(start):
                    self.text.tag_remove(tag, start, end)
                else:
                    self.text.tag_add(tag, start, end)
        except Exception:
            pass

    def change_font(self, event=None):
        family = self.font_family_var.get()
        size = int(self.font_size_var.get())
        try:
            if self.text.tag_ranges("sel"):
                start = self.text.index("sel.first")
                end = self.text.index("sel.last")
                tag = f"font_{family}_{size}"
                self.text.tag_add(tag, start, end)
                self.text.tag_config(tag, font=(family, size))
            else:
                self.base_font_family = family
                self.base_font_size = size
                self.text.config(font=(family, size))
                self.text.tag_configure("bold", font=(family, size, "bold"))
                self.text.tag_configure("italic", font=(family, size, "italic"))
                self.text.tag_configure("underline", font=(family, size, "underline"))
        except Exception:
            pass

    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    self.text.delete("1.0", tk.END)
                    self.text.insert("1.0", f.read())
                self.update_status(f"Открыт: {file}")
            except Exception as e:
                self.update_status(f"Ошибка: {e}")

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            try:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(self.text.get("1.0", tk.END))
                self.update_status(f"Сохранен: {file}")
            except Exception as e:
                self.update_status(f"Ошибка: {e}")

    def clear_text(self):
        self.text.delete("1.0", tk.END)
        self.update_status("Текст очищен")

    def apply_theme(self):
        if self.dark_mode:
            bg = self.bg_dark
            text_bg = self.text_bg_dark
            text_fg = self.text_fg_dark
            toolbar_bg = self.toolbar_bg_dark
            sep_bg = "#666666"
            combo_bg = "#4a4a4a"
            combo_fg = "#ffffff"
            menu_bg = "#3c3c3c"
            menu_fg = "#d4d4d4"
            theme_icon = "☀️"
        else:
            bg = self.bg_light
            text_bg = self.text_bg_light
            text_fg = self.text_fg_light
            toolbar_bg = self.toolbar_bg_light
            sep_bg = "#999999"
            combo_bg = "#ffffff"
            combo_fg = "#2c3e50"
            menu_bg = "#f0f0f0"
            menu_fg = "#2c3e50"
            theme_icon = "🌙"

        self.root.configure(bg=bg)
        self.toolbar.configure(bg=toolbar_bg)
        self.text.configure(bg=text_bg, fg=text_fg)
        self.theme_btn.config(text=theme_icon, bg=toolbar_bg, fg=text_fg)

        self.status_bar.configure(bg=self.accent)
        self.status_label.config(bg=self.accent, fg="white")
        self.cursor_label.config(bg=self.accent, fg="white")

        for widget in self.toolbar.winfo_children():
            if isinstance(widget, tk.Button) and widget != self.theme_btn:
                widget.config(bg=toolbar_bg, fg=text_fg)
            elif isinstance(widget, tk.Label):
                widget.config(bg=toolbar_bg, fg=text_fg)
            elif isinstance(widget, tk.Frame):
                widget.config(bg=sep_bg)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=combo_bg,
            background=combo_bg,
            foreground=combo_fg,
            arrowcolor=combo_fg
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", combo_bg)],
            foreground=[("readonly", combo_fg)],
            background=[("readonly", combo_bg)]
        )

        if self.dark_mode:
            self.root.option_add('*TCombobox*Listbox.Background', '#4a4a4a')
            self.root.option_add('*TCombobox*Listbox.Foreground', '#ffffff')
        else:
            self.root.option_add('*TCombobox*Listbox.Background', '#ffffff')
            self.root.option_add('*TCombobox*Listbox.Foreground', '#2c3e50')

        self.root.option_add('*TCombobox*Listbox.SelectBackground', self.accent)
        self.root.option_add('*TCombobox*Listbox.SelectForeground', 'white')

        self._set_menu_theme(self.root.nametowidget(self.root.cget("menu")), menu_bg, menu_fg)

    def _set_menu_theme(self, menu, bg, fg):
        try:
            menu.configure(bg=bg, fg=fg, activebackground=self.accent, activeforeground="white")
            end = menu.index("end")
            if end is not None:
                for i in range(end + 1):
                    try:
                        submenu = menu.entrycget(i, "menu")
                        if submenu:
                            self._set_menu_theme(menu.nametowidget(submenu), bg, fg)
                    except Exception:
                        pass
        except Exception:
            pass

    def light_theme(self):
        self.dark_mode = False
        self.apply_theme()

    def dark_theme(self):
        self.dark_mode = True
        self.apply_theme()

    def toggle_theme(self):
        if self.dark_mode:
            self.light_theme()
        else:
            self.dark_theme()

    def clear_search_highlight(self):
        self.text.tag_remove("found", "1.0", tk.END)

    def find_text(self, word):
        self.clear_search_highlight()
        if not word:
            return
        start = "1.0"
        count = 0
        while True:
            pos = self.text.search(word, start, tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            self.text.tag_add("found", pos, end)
            start = end
            count += 1
        if count > 0:
            self.update_status(f"Найдено {count} совпадений")
            self.text.see("found.first")
        else:
            self.update_status("Ничего не найдено")

    def open_find(self):
        if self.find_window and self.find_window.winfo_exists():
            self.find_window.destroy()
        self.find_window = tk.Toplevel(self.root)
        self.find_window.title("Поиск")
        self.find_window.geometry("300x120")
        self.find_window.resizable(False, False)
        tk.Label(self.find_window, text="Найти:", font=("Segoe UI", 10)).pack(pady=(10, 0))
        entry = tk.Entry(self.find_window, font=("Segoe UI", 10), width=30)
        entry.pack(pady=5, padx=10)

        def on_find():
            self.find_text(entry.get())

        def on_close():
            self.clear_search_highlight()
            self.find_window.destroy()

        tk.Button(self.find_window, text="Найти", command=on_find,
                  bg=self.accent, fg="white", padx=20, cursor="hand2").pack(pady=10)
        entry.bind("<Return>", lambda e: on_find())
        self.find_window.protocol("WM_DELETE_WINDOW", on_close)

    def open_replace(self):
        if self.replace_window and self.replace_window.winfo_exists():
            self.replace_window.destroy()
        self.replace_window = tk.Toplevel(self.root)
        self.replace_window.title("Замена")
        self.replace_window.geometry("300x170")
        self.replace_window.resizable(False, False)
        tk.Label(self.replace_window, text="Найти:", font=("Segoe UI", 10)).pack(pady=(10, 0))
        find_entry = tk.Entry(self.replace_window, font=("Segoe UI", 10), width=30)
        find_entry.pack(pady=5, padx=10)
        tk.Label(self.replace_window, text="Заменить на:", font=("Segoe UI", 10)).pack()
        replace_entry = tk.Entry(self.replace_window, font=("Segoe UI", 10), width=30)
        replace_entry.pack(pady=5, padx=10)

        def on_replace():
            self.replace_text(find_entry.get(), replace_entry.get())

        def on_close():
            self.clear_search_highlight()
            self.replace_window.destroy()

        tk.Button(self.replace_window, text="Заменить все", command=on_replace,
                  bg=self.accent, fg="white", padx=20, cursor="hand2").pack(pady=10)
        self.replace_window.protocol("WM_DELETE_WINDOW", on_close)

    def replace_text(self, find_text, replace_text):
        if not find_text:
            return
        self.clear_search_highlight()
        content = self.text.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", new_content)
        count = content.count(find_text)
        self.update_status(f"Заменено {count} раз: '{find_text}' → '{replace_text}'")

    def bind_hotkeys(self):
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-f>", lambda e: self.open_find())
        self.root.bind("<Control-h>", lambda e: self.open_replace())
        self.root.bind("<Control-b>", lambda e: self.make_bold())
        self.root.bind("<Control-i>", lambda e: self.make_italic())
        self.root.bind("<Control-u>", lambda e: self.make_underline())


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTextEditor(root)
    root.mainloop()