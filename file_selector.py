import tkinter as tk
from tkinter import filedialog

def select_files():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale

    # Seleziona il file CSV di preavvisi
    preavvisi_path = filedialog.askopenfilename(
        title="Seleziona il file di preavvisi CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    # Seleziona il file CSV di appuntamenti
    appuntamenti_path = filedialog.askopenfilename(
        title="Seleziona il file di appuntamenti CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    return preavvisi_path, appuntamenti_path

if __name__ == "__main__":
    preavvisi, appuntamenti = select_files()
    print(f"File di preavvisi selezionato: {preavvisi}")
    print(f"File di appuntamenti selezionato: {appuntamenti}")
