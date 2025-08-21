import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Python Scientific Calculator (fx-991EX Style)")
        master.geometry("500x700")

        # --- State Variables ---
        self.expression = ""
        self.last_answer = ""
        self.angle_mode = tk.StringVar(value="DEG")  # DEG, RAD, GRAD
        self.is_shift_active = False

        # --- Theming and Styling ---
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=('Arial', 12))
        self.style.configure("Display.TEntry", padding=10)
        self.style.configure("Status.TLabel", font=('Arial', 10), padding=5)
        self.style.configure("Shift.TButton", foreground="red")


        # --- GUI Layout ---
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Display Screen ---
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill=tk.X, pady=5)
        
        # Status Bar (for DEG/RAD/GRAD and SHIFT)
        self.status_label = ttk.Label(display_frame, textvariable=self.angle_mode, style="Status.TLabel")
        self.status_label.pack(anchor='w')
        
        self.display_var = tk.StringVar()
        display_entry = ttk.Entry(display_frame, textvariable=self.display_var, font=("Arial", 30),
                                  justify="right", state="readonly", style="Display.TEntry")
        display_entry.pack(fill=tk.X, expand=True)

        # --- Button Grid ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Button definitions: (text, shift_text, row, col, columnspan, function)
        buttons = [
            ('SHIFT', '', 0, 0, 1, self.toggle_shift), ('MODE', 'SETUP', 0, 1, 1, self.change_angle_mode),
            ('x²', '√', 1, 0, 1, 'func'), ('x³', '∛', 1, 1, 1, 'func'), ('x^y', 'y√x', 1, 2, 1, 'op'),
            ('sin', 'sin⁻¹', 2, 0, 1, 'func'), ('cos', 'cos⁻¹', 2, 1, 1, 'func'), ('tan', 'tan⁻¹', 2, 2, 1, 'func'),
            ('log', '10^x', 3, 0, 1, 'func'), ('ln', 'e^x', 3, 1, 1, 'func'), ('(-)', 'ABS', 3, 2, 1, 'op'),
            ('(', '', 4, 0, 1, 'op'), (')', '', 4, 1, 1, 'op'), ('π', 'e', 4, 2, 1, 'const'),

            ('7', '', 1, 3, 1, 'num'), ('8', '', 1, 4, 1, 'num'), ('9', '', 1, 5, 1, 'num'),
            ('4', '', 2, 3, 1, 'num'), ('5', '', 2, 4, 1, 'num'), ('6', '', 2, 5, 1, 'num'),
            ('1', '', 3, 3, 1, 'num'), ('2', '', 3, 4, 1, 'num'), ('3', '', 3, 5, 1, 'num'),
            ('0', '', 4, 3, 1, 'num'), ('.', '', 4, 4, 1, 'num'), ('Ans', '', 4, 5, 1, 'ans'),

            ('DEL', 'AC', 1, 6, 1, 'clear'),
            ('/', '', 2, 6, 1, 'op'),
            ('*', '', 3, 6, 1, 'op'),
            ('-', '', 4, 6, 1, 'op'),
            ('+', '', 5, 6, 1, 'op'),
            ('=', '', 5, 5, 1, 'eval')
        ]
        
        self.shift_button = None # To change its style later
        
        for i in range(6): button_frame.grid_rowconfigure(i, weight=1)
        for i in range(7): button_frame.grid_columnconfigure(i, weight=1)

        for (text, shift_text, row, col, span, func_type) in buttons:
            button_text = f"{shift_text}\n{text}" if shift_text else text
            action = lambda t=text, st=shift_text, ft=func_type: self.on_button_click(t, st, ft)
            
            # Special case for the SHIFT button itself
            if func_type == self.toggle_shift:
                action = func_type
                
            btn = ttk.Button(button_frame, text=button_text, command=action)
            btn.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)
            
            if text == 'SHIFT':
                self.shift_button = btn


    def on_button_click(self, text, shift_text, func_type):
        char = shift_text if self.is_shift_active else text
        
        if func_type == 'num' or (func_type == 'op' and char not in 'x^y'):
            self.expression += char
        elif func_type == 'const':
            self.expression += {'π': 'pi', 'e': 'e'}[char]
        elif func_type == 'op' and char == 'x^y':
            self.expression += '^'
        elif func_type == 'func':
            func_map = {'√':'sqrt', '∛':'cbrt', 'sin⁻¹':'asin', 'cos⁻¹':'acos', 'tan⁻¹':'atan', '10^x':'10**', 'e^x':'exp'}
            self.expression += func_map.get(char, char) + '('
        elif func_type == 'ans':
            self.expression += self.last_answer
        elif func_type == 'clear':
            if self.is_shift_active: # AC
                self.expression = ""
            else: # DEL
                self.expression = self.expression[:-1]
        elif func_type == 'eval':
            self.calculate()
            
        self.display_var.set(self.expression)
        if self.is_shift_active and func_type != self.toggle_shift:
            self.toggle_shift() # Auto-disable shift after one use

    def toggle_shift(self):
        self.is_shift_active = not self.is_shift_active
        if self.is_shift_active:
            self.shift_button.configure(style="Shift.TButton")
            self.status_label.config(text=f"SHIFT | {self.angle_mode.get()}")
        else:
            self.shift_button.configure(style="TButton")
            self.status_label.config(text=self.angle_mode.get())
            
    def change_angle_mode(self):
        modes = ["DEG", "RAD", "GRAD"]
        current_index = modes.index(self.angle_mode.get())
        next_index = (current_index + 1) % len(modes)
        self.angle_mode.set(modes[next_index])
        self.toggle_shift() if self.is_shift_active else None # Disable shift if active

    def calculate(self):
        try:
            expr = self._prepare_expression(self.expression)
            
            # Use a safe eval context
            allowed_globals = {"math": self.get_math_with_angle_mode()}
            result = eval(expr, allowed_globals)

            self.last_answer = str(result)
            self.display_var.set(self.last_answer)
            self.expression = "" # Reset for next calculation, Casio-style
        except Exception as e:
            self.display_var.set("Syntax Error")
            self.expression = ""

    def _prepare_expression(self, expr):
        # Replace user-friendly names with Python's math module names
        replacements = {
            'π': 'math.pi',
            'e': 'math.e',
            '^': '**',
            '√': 'math.sqrt',
            '∛': 'cbrt',
            'sin⁻¹': 'math.asin',
            'cos⁻¹': 'math.acos',
            'tan⁻¹': 'math.atan',
            'log': 'math.log10',
            'ln': 'math.log',
            'ABS': 'abs',
            # standard functions are handled by the custom math object
        }
        for old, new in replacements.items():
            expr = expr.replace(old, new)
        return expr

    def get_math_with_angle_mode(self):
        # Create a custom object that mimics the math module but respects angle modes
        class MathWithAngles:
            def __init__(self, mode):
                self.mode = mode
                # Map all standard math functions
                for name in dir(math):
                    if not name.startswith('__'):
                        setattr(self, name, getattr(math, name))
            
            def _to_radians(self, angle):
                if self.mode == 'DEG': return math.radians(angle)
                if self.mode == 'GRAD': return angle * math.pi / 200
                return angle # RAD
            
            def _from_radians(self, angle):
                if self.mode == 'DEG': return math.degrees(angle)
                if self.mode == 'GRAD': return angle * 200 / math.pi
                return angle # RAD

            # Override trig functions
            def sin(self, x): return math.sin(self._to_radians(x))
            def cos(self, x): return math.cos(self._to_radians(x))
            def tan(self, x): return math.tan(self._to_radians(x))

            # Override inverse trig functions
            def asin(self, x): return self._from_radians(math.asin(x))
            def acos(self, x): return self._from_radians(math.acos(x))
            def atan(self, x): return self._from_radians(math.atan(x))

            # Custom functions like cube root
            def cbrt(self, x): return x**(1/3)
        
        return MathWithAngles(self.angle_mode.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()