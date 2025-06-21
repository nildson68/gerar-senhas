import tkinter as tk
from tkinter import font

class ProfessionalCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora Profissional")
        self.geometry("360x520")
        self.resizable(False, False)
        self.configure(bg="#ffffff")

        # Fonts
        self.display_font = font.Font(family="Inter", size=30, weight="bold")
        self.button_font = font.Font(family="Inter", size=18, weight="bold")

        # Current expression
        self.expression = ""

        # Setup UI components
        self.create_display()
        self.create_buttons()

    def create_display(self):
        self.display_var = tk.StringVar()
        self.display_var.set("0")

        display_frame = tk.Frame(self, bg="#ffffff", bd=0, relief="ridge")
        display_frame.pack(pady=(20, 10), padx=20, fill="x")

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg="#f9fafb",
            fg="#111827",
            font=self.display_font,
            padx=15,
            pady=15,
            relief="flat",
            borderwidth=0,
        )
        self.display_label.pack(fill="x", ipady=10)
        self.display_label.configure(relief="sunken", bd=2)
        self.round_corners(self.display_label)

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

        # Buttons layout
        buttons = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char == "0":
                    btn = self.create_button(button_frame, char, r, c, colspan=2)
                else:
                    btn = self.create_button(button_frame, char, r, c)

        # Adjust grid weights for scaling
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)

    def create_button(self, parent, char, row, col, colspan=1):
        # Color scheme
        operators = {"÷", "×", "−", "+", "=", "%", "±"}
        bg_color = "#f3f4f6"
        fg_color = "#111827"
        active_bg = "#e0e7ff"

        if char in operators:
            bg_color = "#2563eb"
            fg_color = "#ffffff"
            active_bg = "#1e40af"
        elif char == "C":
            bg_color = "#ef4444"
            fg_color = "#ffffff"
            active_bg = "#991b1b"

        btn = tk.Label(
            parent,
            text=char,
            bg=bg_color,
            fg=fg_color,
            font=self.button_font,
            relief="raised",
            borderwidth=2,
            padx=10,
            pady=12,
            cursor="hand2",
        )
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=6, pady=6)
        self.round_corners(btn)

        # Bind click event
        btn.bind("<Button-1>", lambda e, ch=char: self.on_button_click(ch))
        # Bind hover events for interactive effect
        btn.bind("<Enter>", lambda e, b=btn, c=active_bg: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))

        return btn

    def round_corners(self, widget):
        # Tkinter does not support true rounded corners natively.
        # This is a placeholder if future work to use images is desired.
        # For now, do nothing but keeps code ready for enhancements.
        pass

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "=":
            self.calculate_result()
        elif char == "±":
            self.toggle_sign()
        elif char == "%":
            self.percentage()
        else:
            self.append_expression(char)

    def append_expression(self, char):
        # Replace symbols with Python operators
        replacements = {"÷": "/", "×": "*", "−": "-", "+": "+"}
        if char in replacements:
            to_append = replacements[char]
        else:
            to_append = char

        if self.expression == "" and to_append in {"/", "*", "-", "+"}:
            # Prevent starting expression with operator except minus for negative number
            if to_append != "-":
                return

        # Prevent multiple dots in the current number segment
        if to_append == ".":
            # Split expression by operators to check current number
            import re
            number_parts = re.split(r"[\+\-\*/]", self.expression)
            if "." in number_parts[-1]:
                return

        self.expression += to_append
        self.display_var.set(self.expression)

    def calculate_result(self):
        try:
            # Evaluate expression safely
            result = eval(self.expression, {"__builtins__": None}, {})
            # Format float with max 10 decimals, strip trailing zeros
            if isinstance(result, float):
                result = round(result, 10)
                result = int(result) if result.is_integer() else result
            self.expression = str(result)
            self.display_var.set(self.expression)
        except Exception:
            self.display_var.set("Erro")
            self.expression = ""

    def toggle_sign(self):
        if not self.expression:
            return
        # Try to toggle sign of the last number in expression
        import re
        tokens = re.split(r"([+\-*/])", self.expression)
        if tokens[-1] == "":
            # Expression ends with operator, do nothing
            return
        last_number = tokens[-1]
        if last_number.startswith("-"):
            tokens[-1] = last_number[1:]
        else:
            tokens[-1] = "-" + last_number
        self.expression = "".join(tokens)
        self.display_var.set(self.expression)

    def percentage(self):
        if not self.expression:
            return
        try:
            # Evaluate current expression then divide by 100
            value = eval(self.expression, {"__builtins__": None}, {})
            value /= 100
            self.expression = str(value)
            self.display_var.set(self.expression)
        except Exception:
            self.display_var.set("Erro")
            self.expression = ""

if __name__ == "__main__":
    app = ProfessionalCalculator()
    app.mainloop()

