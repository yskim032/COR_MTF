import os
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import fileinput
from datetime import datetime

# 

def check_expiration():
    expiration_date = datetime(2026, 4, 1)  # 2026-04-01 만료
    current_date = datetime.now()
    
    if current_date > expiration_date:
        messagebox.showerror("Error", "This program has expired. Please contact the administrator.")
        root.quit()
        return False
    return True

def select_file():
    files = filedialog.askopenfilenames(
        title="Select DTX files",
        filetypes=(("DTX Files", "*.GVA;*.txt;*.xls;*.csv"), ("All Files", "*.*"))
    )
    
    if not files:
        return

    listbox.delete(0, END)
    for file_path in files:
        listbox.insert(END, file_path)
    
    count_label.config(text=f"{len(files)} files selected")

def convert_files():
    files = listbox.get(0, END)
    if not files:
        messagebox.showwarning("Warning", "Please select files first.")
        return

    total_files = len(files)
    
    try:
        for file_path in files:
            with fileinput.input(file_path, inplace=True, encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if f.isfirstline():
                        print('HDR              55MFT                               096N', end='\n')
                    else:
                        print(line, end='')
        
        result_label.config(text=f"Successfully converted {total_files} files!", foreground="#00e676")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        result_label.config(text="Conversion failed.", foreground="#cf6679")

# --- UI Setup ---
root = Tk()
root.title("DTX Converter")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#2b2b2b")

# Check expiration on start
if not check_expiration():
    exit()

# Stylization
style = ttk.Style()
style.theme_use('clam')

# Colors
BG_COLOR = "#2b2b2b"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#3a7bd5"
BUTTON_BG = "#3a7bd5"
BUTTON_FG = "#ffffff"
LISTBOX_BG = "#383838"
LISTBOX_FG = "#ffffff"

style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
style.configure("TButton", 
                font=("Segoe UI", 10, "bold"), 
                background=BUTTON_BG, 
                foreground=BUTTON_FG, 
                borderwidth=0, 
                padding=10)
style.map("TButton", 
          background=[('active', '#2c5aa0'), ('pressed', '#1a3b6e')],
          relief=[('pressed', 'sunken')])

# Main container
main_frame = ttk.Frame(root, style="TFrame")
main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Header
header_label = ttk.Label(main_frame, text="DTX Converter", style="Header.TLabel")
header_label.pack(pady=(0, 20), anchor="center")

# File Selection Area
top_frame = ttk.Frame(main_frame)
top_frame.pack(fill=X, pady=(0, 10))

select_btn = ttk.Button(top_frame, text="Select Files", command=select_file)
select_btn.pack(side=LEFT)

count_label = ttk.Label(top_frame, text="0 files selected", font=("Segoe UI", 10, "italic"))
count_label.pack(side=RIGHT, padx=10)

# Listbox Area
list_frame = Frame(main_frame, bg=BG_COLOR)
list_frame.pack(fill=BOTH, expand=True, pady=10)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(
    list_frame, 
    selectmode="extended", 
    height=15, 
    width=80, 
    bg=LISTBOX_BG, 
    fg=LISTBOX_FG,
    bd=0,
    highlightthickness=1,
    highlightbackground="#555555",
    font=("Consolas", 9),
    yscrollcommand=scrollbar.set
)
listbox.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=listbox.yview)

# Action Area
bottom_frame = ttk.Frame(main_frame)
bottom_frame.pack(fill=X, pady=20)

convert_btn = ttk.Button(bottom_frame, text="Convert Files", command=convert_files)
convert_btn.pack(fill=X)

# Status Area
result_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10, "bold"))
result_label.pack(pady=5)

root.mainloop()
