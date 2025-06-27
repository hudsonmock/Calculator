import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.expression = ""
        self.last_operation = ""
        
        # Create the UI
        self.create_display()
        self.create_buttons()
        
        # Bind keyboard events
        self.root.bind('<Key>', self.key_press)
        self.root.focus_set()
    
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg='#2C2C2C', padx=10, pady=10)
        display_frame.pack(fill=tk.X)
        
        # Expression display (shows the full expression)
        self.expression_label = tk.Label(
            display_frame, 
            text="", 
            font=('Arial', 12), 
            bg='#2C2C2C', 
            fg='#888888',
            anchor='e',
            height=1
        )
        self.expression_label.pack(fill=tk.X, pady=(0, 5))
        
        # Result display
        self.result_display = tk.Label(
            display_frame, 
            textvariable=self.result_var, 
            font=('Arial', 24, 'bold'), 
            bg='#2C2C2C', 
            fg='white',
            anchor='e',
            height=2
        )
        self.result_display.pack(fill=tk.X)
    
    def create_buttons(self):
        # Button frame
        button_frame = tk.Frame(self.root, bg='#1E1E1E')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button styling
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'relief': 'flat',
            'borderwidth': 1,
            'cursor': 'hand2'
        }
        
        # Button colors
        number_color = {'bg': '#4A4A4A', 'fg': 'white', 'activebackground': '#5A5A5A'}
        operator_color = {'bg': '#FF9500', 'fg': 'white', 'activebackground': '#FFB84D'}
        function_color = {'bg': '#A6A6A6', 'fg': 'black', 'activebackground': "#000000"}
        
        # Button layout
        buttons = [
            # Row 1
            [('C', function_color, self.clear), ('±', function_color, self.toggle_sign), 
             ('%', function_color, self.percentage), ('÷', operator_color, lambda: self.operation('÷'))],
            
            # Row 2
            [('√', function_color, self.square_root), ('x²', function_color, self.square), 
             ('1/x', function_color, self.reciprocal), ('×', operator_color, lambda: self.operation('×'))],
            
            # Row 3
            [('7', number_color, lambda: self.number('7')), ('8', number_color, lambda: self.number('8')), 
             ('9', number_color, lambda: self.number('9')), ('-', operator_color, lambda: self.operation('-'))],
            
            # Row 4
            [('4', number_color, lambda: self.number('4')), ('5', number_color, lambda: self.number('5')), 
             ('6', number_color, lambda: self.number('6')), ('+', operator_color, lambda: self.operation('+'))],
            
            # Row 5
            [('1', number_color, lambda: self.number('1')), ('2', number_color, lambda: self.number('2')), 
             ('3', number_color, lambda: self.number('3')), ('=', operator_color, self.equals)],
            
            # Row 6
            [('0', number_color, lambda: self.number('0'), 2), ('.', number_color, self.decimal), 
             ('⌫', function_color, self.backspace)]
        ]
        
        # Create buttons
        for row_idx, row in enumerate(buttons):
            for col_idx, item in enumerate(row):
                if len(item) == 4:  # Button spans multiple columns
                    text, colors, command, colspan = item
                else:
                    text, colors, command = item
                    colspan = 1
                
                btn = tk.Button(
                    button_frame,
                    text=text,
                    command=command,
                    **button_style,
                    **colors
                )
                
                btn.grid(
                    row=row_idx, 
                    column=col_idx, 
                    columnspan=colspan,
                    sticky='nsew', 
                    padx=2, 
                    pady=2
                )
        
        # Configure grid weights
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
    
    def number(self, num):
        if self.result_var.get() == "0" or self.last_operation == "equals":
            self.result_var.set(num)
            if self.last_operation == "equals":
                self.expression = ""
                self.expression_label.config(text="")
        else:
            current = self.result_var.get()
            self.result_var.set(current + num)
        self.last_operation = "number"
    
    def decimal(self):
        current = self.result_var.get()
        if '.' not in current:
            if self.last_operation == "equals":
                self.result_var.set("0.")
                self.expression = ""
                self.expression_label.config(text="")
            else:
                self.result_var.set(current + '.')
        self.last_operation = "decimal"
    
    def operation(self, op):
        current = self.result_var.get()
        
        if self.expression and self.last_operation == "operation":
            # Replace the last operator
            self.expression = self.expression.rsplit(' ', 2)[0] + f" {op} "
        else:
            if self.expression and self.last_operation != "equals":
                # Calculate intermediate result
                self.calculate()
                current = self.result_var.get()
            
            self.expression = f"{current} {op} "
        
        self.expression_label.config(text=self.expression)
        self.last_operation = "operation"
    
    def equals(self):
        if self.expression and self.last_operation != "equals":
            self.expression += self.result_var.get()
            self.expression_label.config(text=self.expression)
            self.calculate()
            self.last_operation = "equals"
    
    def calculate(self):
        try:
            # Replace display symbols with calculation symbols
            expression = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            
            # Format result
            if result == int(result):
                self.result_var.set(str(int(result)))
            else:
                self.result_var.set(f"{result:.10g}")
                
        except:
            self.result_var.set("Error")
            self.expression = ""
    
    def clear(self):
        self.result_var.set("0")
        self.expression = ""
        self.expression_label.config(text="")
        self.last_operation = ""
    
    def backspace(self):
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
        self.last_operation = "backspace"
    
    def toggle_sign(self):
        current = self.result_var.get()
        if current != "0":
            if current.startswith('-'):
                self.result_var.set(current[1:])
            else:
                self.result_var.set('-' + current)
    
    def percentage(self):
        try:
            current = float(self.result_var.get())
            result = current / 100
            if result == int(result):
                self.result_var.set(str(int(result)))
            else:
                self.result_var.set(f"{result:.10g}")
        except:
            self.result_var.set("Error")
    
    def square_root(self):
        try:
            current = float(self.result_var.get())
            if current >= 0:
                result = math.sqrt(current)
                if result == int(result):
                    self.result_var.set(str(int(result)))
                else:
                    self.result_var.set(f"{result:.10g}")
            else:
                self.result_var.set("Error")
        except:
            self.result_var.set("Error")
    
    def square(self):
        try:
            current = float(self.result_var.get())
            result = current ** 2
            if result == int(result):
                self.result_var.set(str(int(result)))
            else:
                self.result_var.set(f"{result:.10g}")
        except:
            self.result_var.set("Error")
    
    def reciprocal(self):
        try:
            current = float(self.result_var.get())
            if current != 0:
                result = 1 / current
                if result == int(result):
                    self.result_var.set(str(int(result)))
                else:
                    self.result_var.set(f"{result:.10g}")
            else:
                self.result_var.set("Error")
        except:
            self.result_var.set("Error")
    
    def key_press(self, event):
        key = event.char
        
        # Numbers
        if key in '0123456789':
            self.number(key)
        
        # Operations
        elif key == '+':
            self.operation('+')
        elif key == '-':
            self.operation('-')
        elif key in '*x':
            self.operation('×')
        elif key in '/':
            self.operation('÷')
        
        # Other functions
        elif key == '.':
            self.decimal()
        elif key in '\r\n=':
            self.equals()
        elif key == 'c' or key == 'C':
            self.clear()
        elif event.keysym == 'BackSpace':
            self.backspace()

def main():
    root = tk.Tk()
    
    # Set window icon and properties
    root.configure(bg='#1E1E1E')
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"400x600+{x}+{y}")
    
    calculator = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

