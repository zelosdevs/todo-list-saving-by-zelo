import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class TodoApp:
    def __init__(self):
        # A "lists" mappa elérési útja
        self.directory = os.path.join(os.path.dirname(__file__), "lists")
        self.filename = os.path.join(self.directory, "todo_list1.json")

        # Mappa létrehozása, ha nem létezik
        self.ensure_directory_exists()

        # Betöltjük a feladatokat
        self.tasks = self.load_tasks()

    def ensure_directory_exists(self):
        """Ellenőrzi, hogy a `lists` mappa létezik-e, és létrehozza, ha nem."""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print(f"A '{self.directory}' mappa létrehozva.")

    def load_tasks(self):
        """Feladatok betöltése a JSON fájlból."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                print("Hiba történt a fájl olvasásakor. Üres listával indulunk.")
        return []

    def save_tasks(self):
        """Feladatok mentése JSON fájlba."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
            print(f"Feladatok mentve: {self.filename}")
        except IOError as e:
            print(f"Hiba történt a fájl írásakor: {e}")

    def add_task(self, description):
        """Feladat hozzáadása."""
        task = {"description": description, "done": False}
        self.tasks.append(task)
        self.save_tasks()

    def set_filename(self, new_filename):
        """Új fájlnév beállítása mentéshez."""
        self.filename = os.path.join(self.directory, new_filename)
        print(f"Fájlnév módosítva: {self.filename}")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.geometry("400x400")
        self.filename = "todo_list.json"

        self.tasks = self.load_tasks()

        # Kezdő téma (világos) és nyelv (angol)
        self.theme = "Light"
        self.language = "English"

        # Menüsor létrehozása
        self.create_menu()

        # Frame a feladatok listájához és gombokhoz
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        # Listbox a feladatok megjelenítésére
        self.listbox = tk.Listbox(self.frame, width=40, height=10, selectmode=tk.SINGLE)
        self.listbox.grid(row=0, column=0, padx=10)

        # Scrollbar a listboxhoz
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Feladat hozzáadásához egy mező
        self.entry = tk.Entry(self.root, width=30)
        self.entry.pack(pady=10)

        # Gombok
        self.add_button = tk.Button(self.root, text="Add Task", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.done_button = tk.Button(self.root, text="Mark Done", width=20, command=self.mark_done)
        self.done_button.pack(pady=5)

        # Frissítjük a listát és alkalmazzuk az alapértelmezett témát
        self.refresh_listbox()
        self.apply_theme()
        self.change_language()  # Nyelv beállítása indításkor

    def create_menu(self):
        """Menü létrehozása a nyelv és téma választásához"""
        menubar = tk.Menu(self.root)

        # Nyelv menü
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_radiobutton(label="English", value="English", variable=self.language, command=self.change_language)
        language_menu.add_radiobutton(label="Magyar", value="Hungarian", variable=self.language, command=self.change_language)

        # Téma menü
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_radiobutton(label="Light Mode", value="Light", variable=self.theme, command=self.change_theme)
        theme_menu.add_radiobutton(label="Dark Mode", value="Dark", variable=self.theme, command=self.change_theme)

        # Menü hozzáadása a root-hoz
        self.root.config(menu=menubar)

    def change_language(self):
        """Nyelv váltása"""
        # Frissítjük a szövegeket gombokhoz és feliratokhoz
        if self.language == "English":
            self.add_button.config(text="Add Task")
            self.delete_button.config(text="Delete Task")
            self.done_button.config(text="Mark Done")
        elif self.language == "Hungarian":
            self.add_button.config(text="Feladat hozzáadása")
            self.delete_button.config(text="Feladat törlése")
            self.done_button.config(text="Feladat befejezése")

        # Frissítjük a feladatok listáját (amennyiben vannak lefordított szövegek)
        self.refresh_listbox()

    def apply_theme(self):
        """Alkalmazza az aktuális témát (világos/sötét)"""
        if self.theme == "Light":
            self.root.config(bg="white")
            self.frame.config(bg="white")
            self.listbox.config(bg="white", fg="black")
            self.entry.config(bg="white", fg="black")
            self.add_button.config(bg="lightgray", fg="black")
            self.delete_button.config(bg="lightgray", fg="black")
            self.done_button.config(bg="lightgray", fg="black")
        elif self.theme == "Dark":
            self.root.config(bg="black")
            self.frame.config(bg="black")
            self.listbox.config(bg="black", fg="white")
            self.entry.config(bg="black", fg="white")
            self.add_button.config(bg="darkgray", fg="white")
            self.delete_button.config(bg="darkgray", fg="white")
            self.done_button.config(bg="darkgray", fg="white")

    def change_theme(self):
        """Téma váltása"""
        self.apply_theme()

    def load_tasks(self):
        """Betölti a feladatokat fájlból, ha létezik, különben üres listát ad vissza."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        """Elmenti a feladatokat fájlba."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    def refresh_listbox(self):
        """Frissíti a feladatok listáját a Listbox-ban."""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            display_task = task['description']
            if task['done']:
                display_task += " [Done]"
            self.listbox.insert(tk.END, display_task)

    def add_task(self):
        """Új feladat hozzáadása."""
        task_description = self.entry.get().strip()
        if task_description != "":
            task = {"description": task_description, "done": False}
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_listbox()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task description!")

    def delete_task(self):
        """Feladat törlése."""
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.save_tasks()
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected to delete!")

    def mark_done(self):
        """Feladat befejezése."""
        try:
            selected_task_index = self.listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            if task["done"]:
                messagebox.showinfo("Info", "The task is already marked as done!")
            else:
                task["done"] = True
                self.save_tasks()
                self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected to mark as done!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
