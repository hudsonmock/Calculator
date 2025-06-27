import math
import re

class SimpleCalculator:
    def __init__(self):
        self.history = []
    
    def evaluate_expression(self, expression):
        """Safely evaluate a mathematical expression"""
        try:
            # Remove spaces and convert to lowercase
            expression = expression.replace(' ', '').lower()
            
            # Replace common mathematical functions and constants
            replacements = {
                'π': str(math.pi),
                'pi': str(math.pi),
                'e': str(math.e),
                'sin(': 'math.sin(',
                'cos(': 'math.cos(',
                'tan(': 'math.tan(',
                'sqrt(': 'math.sqrt(',
                'log(': 'math.log(',
                'ln(': 'math.log(',
                'abs(': 'abs(',
                '^': '**',
                '×': '*',
                '÷': '/',
            }
            
            for old, new in replacements.items():
                expression = expression.replace(old, new)
            
            # Validate the expression (only allow safe characters)
            if not re.match(r'^[0-9+\-*/().mathsincotan_abslgrqtpe\s]+$', expression):
                return "Error: Invalid characters in expression"
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            return result
            
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception:
            return "Error: Invalid expression"
    
    def add_to_history(self, expression, result):
        """Add calculation to history"""
        self.history.append(f"{expression} = {result}")
        # Keep only last 10 calculations
        if len(self.history) > 10:
            self.history.pop(0)
    
    def show_history(self):
        """Display calculation history"""
        if not self.history:
            print("No calculations in history.")
            return
        
        print("\n--- Calculation History ---")
        for i, calc in enumerate(self.history, 1):
            print(f"{i}. {calc}")
        print()
    
    def show_help(self):
        """Display help information"""
        help_text = """
=== Calculator Help ===

Basic Operations:
  +, -, *, /     Basic arithmetic
  ** or ^        Exponentiation (2^3 or 2**3)
  ()             Parentheses for grouping

Mathematical Functions:
  sqrt(x)        Square root
  sin(x)         Sine (x in radians)
  cos(x)         Cosine (x in radians)
  tan(x)         Tangent (x in radians)
  log(x)         Natural logarithm
  abs(x)         Absolute value

Constants:
  pi or π        Pi (3.14159...)
  e              Euler's number (2.71828...)

Commands:
  history        Show calculation history
  clear          Clear history
  help           Show this help
  quit or exit   Exit calculator

Examples:
  2 + 3 * 4
  sqrt(16)
  sin(pi/2)
  2^3 + sqrt(9)
  (5 + 3) * 2
        """
        print(help_text)
    
    def run(self):
        """Main calculator loop"""
        print("=== Advanced Calculator ===")
        print("Type 'help' for instructions, 'quit' to exit")
        print()
        
        while True:
            try:
                user_input = input("Calculator> ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("Thank you for using the calculator!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.history.clear()
                    print("History cleared.")
                    continue
                
                # Evaluate the expression
                result = self.evaluate_expression(user_input)
                
                if str(result).startswith("Error"):
                    print(result)
                else:
                    print(f"= {result}")
                    self.add_to_history(user_input, result)
                
            except KeyboardInterrupt:
                print("\nCalculator interrupted. Type 'quit' to exit.")
            except EOFError:
                print("\nGoodbye!")
                break

def main():
    calculator = SimpleCalculator()
    calculator.run()

if __name__ == "__main__":
    main()
