#!/usr/bin/env python3
"""
Stock Price Tracker using Yahoo Finance API
============================================

A comprehensive application to track stock prices with:
- Real-time stock data fetching
- Price history visualization
- Multiple stock tracking
- Market cap and financial metrics
- Beautiful GUI interface

Author: Assistant
Date: June 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import threading
import time

class StockTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Stock Price Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ecf0f1")
        
        # Store tracked stocks
        self.tracked_stocks = {}
        self.auto_refresh = False
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#ecf0f1')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="📈 Stock Price Tracker",
            font=('Arial', 24, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack()
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#ecf0f1')
        input_frame.pack(pady=10)
        
        tk.Label(
            input_frame,
            text="Stock Symbol:",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(side=tk.LEFT, padx=5)
        
        self.symbol_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=15,
            bg='white',
            fg='#2c3e50',
            insertbackground='#2c3e50',
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.symbol_entry.pack(side=tk.LEFT, padx=5)
        self.symbol_entry.bind('<Return>', lambda e: self.add_stock())
        
        tk.Button(
            input_frame,
            text="Add Stock",
            command=self.add_stock,
            bg='#ecf0f1',
            fg='black',
            font=('Arial', 11, 'bold'),
            padx=15,
            activebackground='#ecf0f1',
            activeforeground='black',
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor='#3498db',
            highlightbackground="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame,
            text="Get Info",
            command=self.get_stock_info,
            bg='#ecf0f1',
            fg='black',
            font=('Arial', 11, 'bold'),
            padx=15,
            activebackground='#ecf0f1',
            activeforeground='black',
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor='#27ae60',
            highlightbackground='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame,
            text="Show Chart",
            command=self.show_chart,
            bg='#ecf0f1',
            fg='black',
            font=('Arial', 11, 'bold'),
            padx=15,
            activebackground='#ecf0f1',
            activeforeground='black',
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor='#e74c3c',
            highlightbackground='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame,
            text="Remove Stock",
            command=self.remove_selected_stock,
            bg='#ecf0f1',
            fg='black',
            font=('Arial', 11, 'bold'),
            padx=15,
            activebackground='#ecf0f1',
            activeforeground='black',
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightcolor='#f39c12',
            highlightbackground='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)
        
        # Auto-refresh frame
        refresh_frame = tk.Frame(self.root, bg='#ecf0f1')
        refresh_frame.pack(pady=5)
        
        self.auto_refresh_var = tk.BooleanVar()
        tk.Checkbutton(
            refresh_frame,
            text="Auto-refresh every 30 seconds",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh,
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 10),
            activebackground='#ecf0f1',
            activeforeground='#2c3e50',
            selectcolor='#3498db'
        ).pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Stock list
        left_frame = tk.Frame(content_frame, bg='#f8f9fa', relief=tk.FLAT, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_frame,
            text="📊 Tracked Stocks",
            font=('Arial', 14, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(pady=10)
        
        # Treeview for stocks
        columns = ('Symbol', 'Price', 'Change', 'Change %', 'Volume')
        self.stock_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        
        # Configure treeview style
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#ffffff", 
                       foreground="#2c3e50", 
                       fieldbackground="#ffffff",
                       relief="flat",
                       borderwidth=0)
        style.configure("Treeview.Heading", 
                       background="#34495e", 
                       foreground="white", 
                       font=('Arial', 10, 'bold'),
                       relief="flat")
        
        # Configure selection colors
        style.map("Treeview",
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=100, anchor='center')
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Right panel - Stock details
        right_frame = tk.Frame(content_frame, bg='#f8f9fa', relief=tk.FLAT, bd=0)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            right_frame,
            text="📋 Stock Details",
            font=('Arial', 14, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        ).pack(pady=10)
        
        self.details_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=('Arial', 10),
            bg='#ffffff',
            fg='#2c3e50',
            insertbackground='#2c3e50',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor='#3498db',
            highlightbackground='#bdc3c7'
        )
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#ecf0f1',
            fg='#2c3e50',
            font=('Arial', 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click on treeview
        self.stock_tree.bind('<Double-1>', self.on_stock_select)
        
    def remove_selected_stock(self):
        """Remove selected stock from tracking list"""
        selection = self.stock_tree.selection()
        if not selection:
            # If no selection, try to remove the symbol from entry
            symbol = self.symbol_entry.get().strip().upper()
            if not symbol:
                messagebox.showwarning("Warning", "Please select a stock from the list or enter a symbol to remove")
                return
        else:
            # Get symbol from selected item
            item = self.stock_tree.item(selection[0])
            symbol = item['values'][0]
        
        if symbol in self.tracked_stocks:
            # Remove from data
            del self.tracked_stocks[symbol]
            
            # Remove from treeview
            if selection:
                self.stock_tree.delete(selection[0])
            else:
                # Find and remove the item
                for item in self.stock_tree.get_children():
                    if self.stock_tree.item(item)['values'][0] == symbol:
                        self.stock_tree.delete(item)
                        break
            
            self.status_var.set(f"Removed {symbol} successfully")
            self.symbol_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Info", f"{symbol} is not in the tracking list")
    
    def add_stock(self):
        """Add a stock to the tracking list"""
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return
        
        if symbol in self.tracked_stocks:
            messagebox.showinfo("Info", f"{symbol} is already being tracked")
            return
        
        self.status_var.set(f"Fetching data for {symbol}...")
        self.root.update()
        
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get current data
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                raise ValueError("No data found for this symbol")
            
            # Store stock data
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
            
            self.tracked_stocks[symbol] = {
                'ticker': ticker,
                'price': current_price,
                'change': change,
                'change_percent': change_percent,
                'volume': volume,
                'info': info
            }
            
            # Add to treeview
            self.update_stock_display(symbol)
            
            # Clear entry
            self.symbol_entry.delete(0, tk.END)
            
            self.status_var.set(f"Added {symbol} successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data for {symbol}: {str(e)}")
            self.status_var.set("Ready")
    
    def update_stock_display(self, symbol):
        """Update the display for a specific stock"""
        if symbol not in self.tracked_stocks:
            return
        
        stock_data = self.tracked_stocks[symbol]
        
        # Format values
        price = f"${stock_data['price']:.2f}"
        change = f"{stock_data['change']:+.2f}"
        change_percent = f"{stock_data['change_percent']:+.2f}%"
        volume = f"{stock_data['volume']:,.0f}"
        
        # Determine color based on change
        tag = "positive" if stock_data['change'] >= 0 else "negative"
        
        # Configure tags
        self.stock_tree.tag_configure("positive", foreground="green")
        self.stock_tree.tag_configure("negative", foreground="red")
        
        # Check if item already exists
        existing_items = self.stock_tree.get_children()
        for item in existing_items:
            if self.stock_tree.item(item)['values'][0] == symbol:
                self.stock_tree.item(item, values=(symbol, price, change, change_percent, volume), tags=(tag,))
                return
        
        # Insert new item
        self.stock_tree.insert('', 'end', values=(symbol, price, change, change_percent, volume), tags=(tag,))
    
    def get_stock_info(self):
        """Get detailed information about a stock"""
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return
        
        self.status_var.set(f"Fetching detailed info for {symbol}...")
        self.root.update()
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Format the information
            details = f"📊 STOCK INFORMATION FOR {symbol}\n"
            details += "=" * 50 + "\n\n"
            
            # Basic info
            details += f"Company Name: {info.get('longName', 'N/A')}\n"
            details += f"Sector: {info.get('sector', 'N/A')}\n"
            details += f"Industry: {info.get('industry', 'N/A')}\n"
            details += f"Country: {info.get('country', 'N/A')}\n\n"
            
            # Price info
            details += "💰 PRICE INFORMATION\n"
            details += "-" * 30 + "\n"
            details += f"Current Price: ${info.get('currentPrice', 'N/A')}\n"
            details += f"Previous Close: ${info.get('previousClose', 'N/A')}\n"
            details += f"Open: ${info.get('open', 'N/A')}\n"
            details += f"Day High: ${info.get('dayHigh', 'N/A')}\n"
            details += f"Day Low: ${info.get('dayLow', 'N/A')}\n"
            details += f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
            details += f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}\n\n"
            
            # Market info
            details += "📈 MARKET INFORMATION\n"
            details += "-" * 30 + "\n"
            details += f"Market Cap: ${info.get('marketCap', 'N/A'):,}\n"
            details += f"Volume: {info.get('volume', 'N/A'):,}\n"
            details += f"Average Volume: {info.get('averageVolume', 'N/A'):,}\n"
            details += f"PE Ratio: {info.get('trailingPE', 'N/A')}\n"
            details += f"Dividend Yield: {info.get('dividendYield', 'N/A')}\n"
            details += f"Beta: {info.get('beta', 'N/A')}\n\n"
            
            # Additional info
            details += "ℹ️  ADDITIONAL INFORMATION\n"
            details += "-" * 30 + "\n"
            details += f"Business Summary:\n{info.get('longBusinessSummary', 'N/A')[:500]}...\n\n"
            
            # Display in text widget
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            
            self.status_var.set(f"Info loaded for {symbol}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch info for {symbol}: {str(e)}")
            self.status_var.set("Ready")
    
    def show_chart(self):
        """Show price chart for a stock"""
        symbol = self.symbol_entry.get().strip().upper()
        if not symbol:
            messagebox.showwarning("Warning", "Please enter a stock symbol")
            return
        
        self.status_var.set(f"Generating chart for {symbol}...")
        self.root.update()
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data for different periods
            periods = ['1mo', '3mo', '6mo', '1y']
            
            # Create chart window
            chart_window = tk.Toplevel(self.root)
            chart_window.title(f"📈 {symbol} Price Chart")
            chart_window.geometry("1000x700")
            
            # Create notebook for different time periods
            notebook = ttk.Notebook(chart_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            for period in periods:
                # Get data
                hist = ticker.history(period=period)
                
                if hist.empty:
                    continue
                
                # Create frame for this period
                frame = ttk.Frame(notebook)
                notebook.add(frame, text=period.upper())
                
                # Create matplotlib figure
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                              gridspec_kw={'height_ratios': [3, 1]})
                
                # Price chart
                ax1.plot(hist.index, hist['Close'], linewidth=2, color='#3498db')
                ax1.fill_between(hist.index, hist['Close'], alpha=0.3, color='#3498db')
                ax1.set_title(f'{symbol} - {period.upper()} Price Chart', fontsize=16, fontweight='bold')
                ax1.set_ylabel('Price ($)', fontsize=12)
                ax1.grid(True, alpha=0.3)
                
                # Volume chart
                ax2.bar(hist.index, hist['Volume'], alpha=0.7, color='#e74c3c')
                ax2.set_title('Volume', fontsize=12)
                ax2.set_ylabel('Volume', fontsize=10)
                ax2.set_xlabel('Date', fontsize=10)
                
                plt.tight_layout()
                
                # Embed in tkinter
                canvas = FigureCanvasTkAgg(fig, frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set(f"Chart generated for {symbol}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart for {symbol}: {str(e)}")
            self.status_var.set("Ready")
    
    def on_stock_select(self, event):
        """Handle double-click on stock in treeview"""
        selection = self.stock_tree.selection()
        if selection:
            item = self.stock_tree.item(selection[0])
            symbol = item['values'][0]
            self.symbol_entry.delete(0, tk.END)
            self.symbol_entry.insert(0, symbol)
            self.get_stock_info()
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        if self.auto_refresh_var.get():
            self.auto_refresh = True
            self.start_auto_refresh()
        else:
            self.auto_refresh = False
    
    def start_auto_refresh(self):
        """Start auto-refresh in a separate thread"""
        def refresh_loop():
            while self.auto_refresh:
                time.sleep(30)  # Wait 30 seconds
                if self.auto_refresh:  # Check again in case it was turned off
                    self.refresh_all_stocks()
        
        thread = threading.Thread(target=refresh_loop, daemon=True)
        thread.start()
    
    def refresh_all_stocks(self):
        """Refresh data for all tracked stocks"""
        if not self.tracked_stocks:
            return
        
        self.status_var.set("Refreshing all stocks...")
        
        for symbol in list(self.tracked_stocks.keys()):
            try:
                ticker = self.tracked_stocks[symbol]['ticker']
                hist = ticker.history(period="1d")
                info = ticker.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = info.get('previousClose', current_price)
                    change = current_price - prev_close
                    change_percent = (change / prev_close) * 100
                    volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                    
                    self.tracked_stocks[symbol].update({
                        'price': current_price,
                        'change': change,
                        'change_percent': change_percent,
                        'volume': volume,
                        'info': info
                    })
                    
                    self.update_stock_display(symbol)
                    
            except Exception as e:
                print(f"Error refreshing {symbol}: {e}")
        
        self.status_var.set(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StockTracker(root)
    
    # Add some example stocks
    example_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    
    def add_examples():
        for symbol in example_stocks:
            app.symbol_entry.delete(0, tk.END)
            app.symbol_entry.insert(0, symbol)
            app.add_stock()
            time.sleep(0.5)  # Small delay to avoid rate limiting
    
    # Ask user if they want to load example stocks
    if messagebox.askyesno("Example Stocks", "Would you like to load some example stocks (AAPL, GOOGL, MSFT, TSLA)?"):
        thread = threading.Thread(target=add_examples, daemon=True)
        thread.start()
    
    root.mainloop()


if __name__ == "__main__":
    main()