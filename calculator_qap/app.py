import tkinter as tk
from tkinter import ttk
import math

class AdvancedCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Python Advanced Calculator")
        master.geometry("400x600")

        self.expression = ""
        self.history = []
        self.memory = 0

        self.style = ttk.Style()
        self.themes = ["light", "dark"]
        self.current_theme = tk.StringVar(value="light")
        self.apply_theme()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Display ---
        self.display_var = tk.StringVar()
        display_entry = ttk.Entry(main_frame, textvariable=self.display_var, font=("Arial", 24), justify="right", state="readonly")
        display_entry.grid(row=0, column=0, columnspan=5, sticky="nsew", ipady=10)

        # --- Button Layout ---
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 1, 4), ('CE', 2, 4), ('sqrt', 3, 4), ('^', 4, 4),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log10', 5, 3),
            ('M+', 5, 4), ('MR', 6, 4), ('MC', 6, 3), ('Theme', 6, 0)
        ]

        for (text, row, col) in buttons:
            button = ttk.Button(main_frame, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            main_frame.grid_columnconfigure(col, weight=1)
            main_frame.grid_rowconfigure(row, weight=1)

        # --- History Panel ---
        history_frame = ttk.LabelFrame(main_frame, text="History", padding="10")
        history_frame.grid(row=7, column=0, columnspan=5, sticky="nsew", pady=10)

        self.history_text = tk.Text(history_frame, height=5, state="disabled", wrap="word")
        self.history_text.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(7, weight=2)

    def on_button_click(self, char):
        if char in "0123456789.":
            self.expression += str(char)
            self.display_var.set(self.expression)
        elif char in "+-*/^":
            if self.expression and self.expression[-1] not in "+-*/^":
                self.expression += str(char)
                self.display_var.set(self.expression)
        elif char == '=':
            self.calculate()
        elif char == 'C':
            self.expression = ""
            self.display_var.set("")
        elif char == 'CE':
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
        elif char == 'sqrt':
            try:
                result = str(math.sqrt(float(self.expression)))
                self.add_to_history(f"sqrt({self.expression}) = {result}")
                self.expression = result
                self.display_var.set(result)
            except ValueError:
                self.display_var.set("Error")
                self.expression = ""
        elif char in ('sin', 'cos', 'tan', 'log10'):
            try:
                value = float(self.expression)
                if char == 'sin':
                    result = str(math.sin(math.radians(value)))
                elif char == 'cos':
                    result = str(math.cos(math.radians(value)))
                elif char == 'tan':
                    result = str(math.tan(math.radians(value)))
                elif char == 'log10':
                    result = str(math.log10(value))
                self.add_to_history(f"{char}({self.expression}) = {result}")
                self.expression = result
                self.display_var.set(result)
            except (ValueError, ZeroDivisionError):
                self.display_var.set("Error")
                self.expression = ""
        elif char == 'M+':
            try:
                self.memory += float(self.expression)
            except ValueError:
                pass
        elif char == 'MR':
            self.expression += str(self.memory)
            self.display_var.set(self.expression)
        elif char == 'MC':
            self.memory = 0
        elif char == 'Theme':
            current_index = self.themes.index(self.current_theme.get())
            next_index = (current_index + 1) % len(self.themes)
            self.current_theme.set(self.themes[next_index])
            self.apply_theme()

    def calculate(self):
        try:
            # Replace ^ with ** for Python's power operator
            calculation = self.expression.replace('^', '**')
            result = str(eval(calculation))
            self.add_to_history(f"{self.expression} = {result}")
            self.expression = result
            self.display_var.set(result)
        except Exception as e:
            self.display_var.set("Error")
            self.expression = ""

    def add_to_history(self, entry):
        self.history.insert(0, entry)
        self.update_history_display()

    def update_history_display(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")

    def apply_theme(self):
        theme = self.current_theme.get()
        if theme == "dark":
            self.master.tk_setPalette(background='#2e2e2e', foreground='white')
            self.style.configure("TButton", foreground="white", background="#555555")
            self.style.configure("TEntry", fieldbackground="#555555", foreground="white")
            self.style.configure("TLabelFrame", foreground="white")
            self.style.map("TButton", background=[("active", "#666666")])
        else: # light theme
            self.master.tk_setPalette(background='#f0f0f0', foreground='black')
            self.style.configure("TButton", foreground="black", background="#d9d9d9")
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("TLabelFrame", foreground="black")
            self.style.map("TButton", background=[("active", "#e6e6e6")])

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()