import os
import sys
import json
import pandas as pd
import tkinter as tk
from tkinter import Label, Entry, Button, BooleanVar, filedialog
import ttkbootstrap as ttk


# Constants for file paths and initial settings
SCRIPT_DIRECTORY = getattr(sys, '_MEIPASS', os.path.dirname(os.path.realpath(__file__)))
CATEGORY_FILE = os.path.join(SCRIPT_DIRECTORY, "labels.json")
INITIAL_FONT_SIZE = 12

def load_json_file(file_path, default={}):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return default

categories = load_json_file(CATEGORY_FILE)

class ManualCodingApp:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.load_data()
        self.display_column = "sentence_text" # Setting sentence_text as default
        self.create_menu()
        self.display_row()

    def setup_gui(self):
        self.root.title("Manual Coding Helper for SCEUS")
        self.root.geometry("1000x1200")
        self.root.config(bg='#333333')

        self.index = tk.IntVar(value=0)
        self.font_size = tk.IntVar(value=INITIAL_FONT_SIZE)
        self.dark_mode = BooleanVar(value=False)

        self.create_widgets()
        self.layout_widgets()
        self.bind_events()


    def create_widgets(self):
        self.mip_label = ttk.Label(self.root, font=("Helvetica", self.font_size.get(), "bold"), wraplength=2000, bootstyle="inverse-primary")
        self.kodierung_label = Label(self.root, font=("Helvetica", self.font_size.get()))
        self.row_label = Label(self.root, font=("Helvetica", self.font_size.get()))
#        self.correct_label = Label(self.root, font=("Helvetica", self.font_size.get()))
        self.category_info_label = Label(self.root, font=("Helvetica", self.font_size.get()))
        self.kommentar_label = Label(self.root, font=("Helvetica", self.font_size.get()))
        self.percentage_label = Label(self.root, font=("Helvetica", self.font_size.get()))
        self.descriptive_sentence_text = ttk.Text(self.root, wrap=tk.WORD, font=("Helvetica", self.font_size.get()), height=2)
        self.kommentar_entry = Entry(self.root, font=("Helvetica", self.font_size.get()))
        self.entry = Entry(self.root, font=("Helvetica", self.font_size.get()))
        self.entry.config(state=tk.NORMAL)  # Set the state to NORMAL to enable input
        self.entry_label = Label(self.root, text="Enter new label value:")
        self.update_button = Button(self.root, text="Update Label (Enter)", command=self.update_kodierung, font=("Helvetica", self.font_size.get()))
        self.next_button = Button(self.root, text="Next Row (Right)", command=self.next_row, font=("Helvetica", self.font_size.get()))
        self.previous_button = Button(self.root, text="Previous Row (Left)", command=self.previous_row, font=("Helvetica", self.font_size.get()))
#        self.correct_button = Button(self.root, text="Correct (C)", command=lambda: self.toggle_correct_status(True), font=("Helvetica", self.font_size.get()))
#        self.incorrect_button = Button(self.root, text="Incorrect (X)", command=lambda: self.toggle_correct_status(False), font=("Helvetica", self.font_size.get()))
        self.update_kommentar_button = Button(self.root, text="Update Comment", command=self.update_kommentar, font=("Helvetica", self.font_size.get()))
        self.go_to_empty_button = Button(self.root, text="Go to Empty Row", command=self.go_to_empty_row, font=("Helvetica", self.font_size.get()))

    def layout_widgets(self):
        # Layout all widgets in the GUI
        self.mip_label.pack(pady=5)
        self.kodierung_label.pack(pady=5)
        self.category_info_label.pack(pady=5)
        self.descriptive_sentence_text.pack(pady=5, fill="both", expand=True)

        self.row_label.pack(pady=5)
#        self.correct_label.pack(pady=5)
        self.kommentar_label.pack(pady=5)
        self.percentage_label.pack(pady=5)
        self.go_to_empty_button.pack(pady=5)
#        self.correct_button.pack(pady=5)
#        self.incorrect_button.pack(pady=5)
        self.entry_label.pack(pady=5)
        self.entry.pack(pady=5)
        self.update_button.pack(pady=5)
        self.kommentar_entry.pack(pady=5)
        self.update_kommentar_button.pack(pady=5)
        self.previous_button.pack(pady=5)
        self.next_button.pack(pady=5)

    def bind_events(self):
        self.root.bind('<Left>', lambda event: self.previous_row())
        self.root.bind('<Right>', lambda event: self.next_row())
#        self.root.bind('<c>', lambda event: self.toggle_correct_status(True))
#        self.root.bind('<x>', lambda event: self.toggle_correct_status(False))
        self.root.bind('<Control-plus>', lambda event: self.increase_font_size())
        self.root.bind('<Control-minus>', lambda event: self.decrease_font_size())
        self.root.bind('<Return>', lambda event: self.update_kodierung())
        self.root.bind('<Configure>', lambda event: self.update_wraplength())
        

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select Dataset_Manual file (xlsx or csv)")
        if not file_path:
            sys.exit("File selection cancelled.")

        if file_path.endswith('.xlsx'):
            self.df = pd.read_excel(file_path, sheet_name="Coding")
        elif file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)
        else:
            sys.exit("Unsupported file type")

        self.file_path = file_path  # Store the file path
        self.ensure_columns()

        # After loading data, set focus back to the main application window
        self.root.focus_force()  # Ensure window has focus after loading data

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        settings_menu.add_command(label="Select column to display", command=self.select_column)
        settings_menu.add_cascade(label="Font Size", menu=self.font_size_submenu())
        settings_menu.add_command(label="Edit Labels", command=self.edit_labels)

    def edit_labels(self):
        window = tk.Toplevel(self.root)
        window.title("Edit Labels")

        tree = ttk.Treeview(window, columns=('Label', 'Description'))
        tree.heading('#0', text='ID')
        tree.heading('#1', text='Label')
        tree.heading('#2', text='Description')
        tree.pack(fill='both', expand=True)  # Use fill and expand to take up full space

        for id, label in categories.items():
            tree.insert('', 'end', text=id, values=(label['label'], label['description']))

        def edit_item():
            selected_item = tree.selection()[0]
            id = tree.item(selected_item, 'text')
            label = tree.item(selected_item, 'values')[0]
            description = tree.item(selected_item, 'values')[1]

            top = tk.Toplevel(window)
            tk.Label(top, text='Label:').pack()
            label_entry = tk.Entry(top)
            label_entry.insert(0, label)
            label_entry.pack()
            tk.Label(top, text='Description:').pack()
            description_entry = tk.Entry(top)
            description_entry.insert(0, description)
            description_entry.pack()

            def save_changes():
                categories[id]['label'] = label_entry.get()
                categories[id]['description'] = description_entry.get()
                with open(CATEGORY_FILE, 'w') as f:
                    json.dump(categories, f)
                top.destroy()
                refresh_treeview(tree)  # Call the refresh function

            tk.Button(top, text='Save', command=save_changes).pack()

        def refresh_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            for id, label in categories.items():
                tree.insert('', 'end', text=id, values=(label['label'], label['description']))

        tk.Button(window, text='Edit', command=edit_item).pack()


    def font_size_submenu(self):
        submenu = tk.Menu(self.root, tearoff=0)
        submenu.add_command(label="Increase Font Size (Strg +)", command=self.increase_font_size)
        submenu.add_command(label="Decrease Font Size (Strg -)", command=self.decrease_font_size)
        return submenu


    def select_column(self):
        column_names = self.df.columns.tolist()
        column_names.sort()

        column_var = tk.StringVar()
        if self.display_column is None:
            self.display_column = 'sentence_text' if 'sentence_text' in column_names else column_names[0]
        column_var.set(self.display_column)  # default value

        window = tk.Toplevel(self.root)
        window.title("Select column to display")

        label = tk.Label(window, text="Select column to display:")
        label.pack(pady=5)

        option_menu = tk.OptionMenu(window, column_var, *column_names)
        option_menu.pack(pady=5)

        def save_column():
            self.display_column = column_var.get()
            window.destroy()

        button = tk.Button(window, text="Save", command=save_column)
        button.pack(pady=5)

        window.grab_set()
        self.root.wait_window(window)


    def ensure_columns(self):
        for column in ['Kodierung', 'Kommentar', 'Manually Checked']:
            if column not in self.df.columns:
                self.df[column] = None

    def display_row(self):
        index = self.index.get()
        row_data = self.df.iloc[index]
        self.mip_label.config(text=row_data.get(self.display_column, ''))
        self.kodierung_label.config(text=f"Label: {row_data.get('Kodierung', '')}")
        self.row_label.config(text=f"Row: {index + 1}/{len(self.df)}")
        self.kommentar_label.config(text=f"Comment: {row_data.get('Kommentar', '')}")
        self.update_category_info()

    def update_category_info(self):
        kodierung = str(self.df.at[self.index.get(), 'Kodierung'])
        kodierung = kodierung.replace(".0", "")
        self.kodierung_label.config(text=f"Label: {kodierung}")
        category_info = categories.get(str(kodierung), {}).get("label", "No information available")
        self.category_info_label.config(text=f"Category Information: {category_info}")
        descriptive_sentence = categories.get(str(kodierung), {}).get("description", "No descriptive sentence available")
        self.descriptive_sentence_text.delete('1.0', tk.END)
        self.descriptive_sentence_text.insert(tk.END, descriptive_sentence)


    def next_row(self):
        new_index = min(self.index.get() + 1, len(self.df) - 1)
        self.index.set(new_index)
        self.display_row()

    def previous_row(self):
        new_index = max(self.index.get() - 1, 0)
        self.index.set(new_index)
        self.display_row()

    def update_kodierung(self):
        new_kodierung = self.entry.get()
        self.df.at[self.index.get(), 'Kodierung'] = new_kodierung
        self.display_row()
        self.save_changes()


    def update_kommentar(self):
        new_kommentar = self.kommentar_entry.get()
        self.df.at[self.index.get(), 'Kommentar'] = new_kommentar
        self.kommentar_label.config(text=f"Comment: {new_kommentar}")
        self.kommentar_entry.delete(0, 'end')
        self.save_changes()


    def update_wraplength(self):
        window_width = self.root.winfo_width()
        padding = 20
        new_width = max(1, (window_width - 2 * padding) // 7)
        self.descriptive_sentence_text.config(width=new_width)
        widgets_with_wraplength = [
            self.mip_label, self.kodierung_label, self.row_label,
            self.category_info_label, self.kommentar_label, self.percentage_label
        ] # self.correct_label
        new_wraplength = window_width - 2 * padding
        for widget in widgets_with_wraplength:
            widget.config(wraplength=new_wraplength)


    def toggle_dark_mode(self):
        is_dark = self.dark_mode.get()
        self.root.configure(bg='#333333' if is_dark else 'white')
        text_color = 'white' if is_dark else 'black'
        bg_color = '#333333' if is_dark else 'white'
        widgets = [self.mip_label, self.kodierung_label, self.row_label,
                   self.category_info_label, self.kommentar_label, self.percentage_label] # self.correct_label
        for widget in widgets:
            widget.config(fg=text_color, bg=bg_color)
        self.entry.config(bg='lightgrey' if not is_dark else 'white', fg=text_color)
        self.kommentar_entry.config(bg='lightgrey' if not is_dark else 'white', fg=text_color)

    def increase_font_size(self):
        new_size = self.font_size.get() + 1
        self.font_size.set(new_size)
        self.update_font_size()

    def decrease_font_size(self):
        new_size = max(1, self.font_size.get() - 1)
        self.font_size.set(new_size)
        self.update_font_size()

    def update_font_size(self):
        font_spec = ("Helvetica", self.font_size.get())
        widgets = [self.mip_label, self.kodierung_label, self.row_label,
                   self.category_info_label, self.kommentar_label, self.percentage_label,
                   self.entry, self.kommentar_entry, self.descriptive_sentence_text] # self.correct_label
        for widget in widgets:
            widget.config(font=font_spec)

#    def toggle_correct_status(self, is_correct):
#        self.df.at[self.index.get(), 'Manually Checked'] = is_correct
#        self.update_correct_status()
#
#    def update_correct_status(self):
#        is_correct = self.df.at[self.index.get(), 'Manually Checked']
#        if is_correct is True:
#            self.correct_label.config(text="Correct: ✔", fg='green')
#        elif is_correct is False:
#            self.correct_label.config(text="Correct: ✘", fg='red')
#        else:
#            self.correct_label.config(text="Correct: ?", fg='yellow')

    def save_changes(self):
        if self.file_path.endswith('.xlsx'):
            self.df.to_excel(self.file_path, index=False)
        elif self.file_path.endswith('.csv'):
            self.df.to_csv(self.file_path, index=False)
        else:
            print("Unsupported file type")


    def go_to_empty_row(self):
        empty_indices = self.df[(self.df['Kodierung'] == 0) | (self.df['Kodierung'].isna()) | (self.df['Kodierung'] == 'NA')].index
        if not empty_indices.empty:
            self.index.set(empty_indices[0])
            self.display_row()
        else:
            print("No empty rows found.")


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    root.focus_set()  # Set the focus to the main window
    app = ManualCodingApp(root)
    root.mainloop()




