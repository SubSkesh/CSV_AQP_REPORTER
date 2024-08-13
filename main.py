from load_data import *
from file_selector import *
from grouper import *
from unifier import *
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import threading

def show_loading_message():
    loading_window = tk.Toplevel()
    loading_window.title("Caricamento in corso...")
    loading_window.geometry("200x100")
    
    label = tk.Label(loading_window, text="Caricamento in corso, attendere prego...")
    label.pack(pady=20)
    
    try:
        # Se hai un'immagine di caricamento
        img = Image.open(r"C:\Users\Oscar Costanzelli\OneDrive - F.IMM S.R.L\Desktop\testingproject\images\waiting.png")
        img = img.resize((50, 50), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        label_img = tk.Label(loading_window, image=img)
        label_img.image = img
        label_img.pack(pady=10)
    except Exception as e:
        print(f"Errore nel caricamento dell'immagine: {e}")
    
    return loading_window
    


def convert_dates(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype('Int64').astype(str).str.zfill(8)
                df[col] = pd.to_datetime(df[col], format='%Y%m%d', errors='coerce')
                print(f"Converted column {col}:\n{df[col].head()}")
            except Exception as e:
                print(f"Errore nella conversione della colonna {col}: {e}")

def convert_times(df, time_columns):
    for col in time_columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype('Int64').astype(str).str.zfill(6)
                df[col] = pd.to_datetime(df[col], format='%H%M%S', errors='coerce').dt.time
                print(f"Converted column {col}:\n{df[col].head()}")
            except Exception as e:
                print(f"Errore nella conversione della colonna {col}: {e}")

def merge_dataframes(df1, df2, common_columns, columns_to_extract):
    merged_df = pd.merge(df1, df2, on=common_columns, suffixes=('_preavviso', '_appuntamento'))
    merged_df = merged_df[columns_to_extract]
    return merged_df

def save_to_csv(df, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df.to_csv(output_file, index=False, sep=';')
    print(f"File creato: {output_file}")

def ask_save_filepath():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    return file_path

def show_animation(images):
    root = tk.Tk()
    root.title("Benvenuto")
    
    # Dimensioni della finestra basate sulle dimensioni dell'immagine
    window_width, window_height = 200, 119
    frame = tk.Frame(root, width=window_width, height=window_height)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    
    label = tk.Label(frame)
    label.pack()

    def update_image(img_index):
        img = Image.open(images[img_index])
        img = img.resize((window_width, window_height), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        label.config(image=img)
        label.image = img
        img_index = (img_index + 1) % len(images)
        root.after(500, update_image, img_index)
    
    root.after(0, update_image, 0)
    
    root.after(2500, root.destroy)  # L'animazione dura 5 secondi
    root.mainloop()

def main():
    # Immagini per l'animazione
    animation_images = [
        "images/fimm logo.png"
    ]

    # Mostra l'animazione di benvenuto
    show_animation(animation_images)

    # Lancio il grouper
    preavvisi_path, appuntamenti_path = CSVGrouper()

    print(preavvisi_path, appuntamenti_path)

    check = 1
    # Guardo se i path sono stati inseriti
    if preavvisi_path is None or appuntamenti_path is None:
        check = 0

    file_preavvisi, file_portion = CSVUnifier(check, preavvisi_path, appuntamenti_path)
    print("ciao")

    # Mostra la finestra di caricamento in un thread separato
    
    #mostra una finestra di messaggio di avvertimento che dice di aspettare
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale

# Imposta la finestra principale come topmost (sempre in primo piano)
    root.attributes('-topmost', True)

# Mostra il messagebox in primo piano
    messagebox.showinfo("ATTENDERE", " ATTENDI IL CARICAMENTO DEI DATI!\nASPETTARE LA PROSSIMA FINESTRA!")

# Disabilita l'attributo topmost
    root.attributes('-topmost', False)


    # Carica i dati dai file CSV
    df_preavvisi = read_csv_file(file_preavvisi)
    df_appuntamenti = read_csv_file(file_portion)
    print("ciao")
    # Verifica il contenuto delle colonne DATA e ORA
    print("\nPrime righe del file preavvisi:")
    print(df_preavvisi[['DATA', 'ORA']].head())
    print("\nPrime righe del file appuntamenti:")
    print(df_appuntamenti[['DATA', 'ORA', 'LETTURA']].head())

    # Colonne comuni per il merge
    common_columns = ['ULM_IMPIANTO', 'PORTION']

    # Colonne da estrarre e rinominare
    columns_to_extract = common_columns + [
        'DATA_preavviso', 'ORA_preavviso',
        'DATA_appuntamento', 'ORA_appuntamento',
        'LETTURA'
    ]

    # Rinominazione delle colonne prima del merge
    df_preavvisi = df_preavvisi.rename(columns={'DATA': 'DATA_preavviso', 'ORA': 'ORA_preavviso'})
    df_appuntamenti = df_appuntamenti.rename(columns={'DATA': 'DATA_appuntamento', 'ORA': 'ORA_appuntamento'})

    # Verifica la rinominazione delle colonne
    print("\nPrime righe del file preavvisi dopo la rinominazione:")
    print(df_preavvisi[['DATA_preavviso', 'ORA_preavviso']].head())
    print("\nPrime righe del file appuntamenti dopo la rinominazione:")
    print(df_appuntamenti[['DATA_appuntamento', 'ORA_appuntamento', 'LETTURA']].head())

    # Esegui il merge
    merged_df = merge_dataframes(df_preavvisi, df_appuntamenti, common_columns, columns_to_extract)

    # Visualizza i primi dati del merge
    print("\nPrime righe del DataFrame unito:")
    print(merged_df.head())

    # Conversione delle colonne di data e ora
    convert_dates(merged_df, ['DATA_preavviso', 'DATA_appuntamento'])
    convert_times(merged_df, ['ORA_preavviso', 'ORA_appuntamento'])

    # Aggiorna la colonna LETTURA
    merged_df['LETTURA'] = merged_df['LETTURA'].apply(lambda x: 'SI' if x != 'NO' and pd.notna(x) else 'NO')

    # Aggiunge la colonna APPUNTAMENTO_ESEGUITO?
    merged_df['APPUNTAMENTO_ESEGUITO?'] = merged_df.apply(
        lambda row: 'SI' if pd.notna(row['DATA_appuntamento']) and pd.notna(row['ORA_appuntamento']) else 'NO',
        axis=1
    )

    # Unisce data e ora in un'unica colonna
    merged_df['DATA_PREAVVISO'] = merged_df.apply(
        lambda row: f"{row['DATA_preavviso'].strftime('%Y-%m-%d')} {row['ORA_preavviso']}" if pd.notna(row['DATA_preavviso']) and pd.notna(row['ORA_preavviso']) else "", axis=1
    )
    merged_df['DATA_APPUNTAMENTO'] = merged_df.apply(
        lambda row: f"{row['DATA_appuntamento'].strftime('%Y-%m-%d')} {row['ORA_appuntamento']}" if pd.notna(row['DATA_appuntamento']) and pd.notna(row['ORA_appuntamento']) else "", axis=1
    )

    # Rimuove le colonne separate di data e ora
    merged_df = merged_df.drop(columns=['DATA_preavviso', 'ORA_preavviso', 'DATA_appuntamento', 'ORA_appuntamento'])

    # Aggiunge la colonna ERRORE_CRONOLOGICO
    merged_df['ERRORE_CRONOLOGICO'] = merged_df.apply(
        lambda row: 'ERRORE' if pd.notna(row['DATA_APPUNTAMENTO']) and pd.notna(row['DATA_PREAVVISO']) and row['DATA_APPUNTAMENTO'] < row['DATA_PREAVVISO'] else 'REGOLARE',
        axis=1
    )

    # Aggiunge la colonna MONOPASSAGGIO
    merged_df['MONOPASSAGGIO'] = merged_df.apply(
        lambda row: 'SI' if row['DATA_PREAVVISO'] == "" or row['DATA_APPUNTAMENTO'] == "" else 'NO',
        axis=1
    )

    # Aggiunge la colonna CONFRONTO considerando l'errore cronologico
    def calcola_confronto(row):
        if pd.notna(row['DATA_PREAVVISO']) and pd.notna(row['DATA_APPUNTAMENTO']):
            diff_hours = abs((pd.to_datetime(row['DATA_APPUNTAMENTO']) - pd.to_datetime(row['DATA_PREAVVISO'])).total_seconds() / 3600)
            return '>48h' if diff_hours >= 48 else '<48h'
        return '<48h'

    merged_df['CONFRONTO'] = merged_df.apply(calcola_confronto, axis=1)

    # Aggiunge la colonna MULTA
    def calcola_multa(row):
        data_preavviso_empty = pd.isna(row['DATA_PREAVVISO']) or row['DATA_PREAVVISO'] == ""
        if row['LETTURA'] == 'NO' and data_preavviso_empty:
            return 90
        elif row['CONFRONTO'] == '<48h' and row['ERRORE_CRONOLOGICO'] == 'REGOLARE':
            diff_hours = abs((pd.to_datetime(row['DATA_APPUNTAMENTO']) - pd.to_datetime(row['DATA_PREAVVISO'])).total_seconds() / 3600)
            if 24 <= diff_hours < 48:
                return 30
            elif 16 <= diff_hours < 24:
                return 60
            elif diff_hours < 16:
                return 90
        return ""

    merged_df['MULTA'] = merged_df.apply(calcola_multa, axis=1)

    # Visualizza i dati dopo l'unione delle colonne e l'aggiunta di ERRORE_CRONOLOGICO, MONOPASSAGGIO, CONFRONTO, MULTA e APPUNTAMENTO_ESEGUITO?
    print("\nPrime righe del DataFrame dopo l'unione di date e ore e l'aggiunta di ERRORE_CRONOLOGICO, MONOPASSAGGIO, CONFRONTO, MULTA e APPUNTAMENTO_ESEGUITO?:")
    print(merged_df.head())

    # Chiede all'utente dove salvare il file di output
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale

# Imposta la finestra principale come topmost (sempre in primo piano)
    root.attributes('-topmost', True)

# Mostra il messagebox in primo piano
    messagebox.showinfo("OTTIMO", "DATI ELABORATI CON SUCCESSO!")

# Disabilita l'attributo topmost
    root.attributes('-topmost', False)
    output_file = ask_save_filepath()
    if output_file:
        save_to_csv(merged_df, output_file)
        print('Elaborazione completata')
        root = tk.Tk()
        root.withdraw()  # Nasconde la finestra principale

# Imposta la finestra principale come topmost (sempre in primo piano)
        root.attributes('-topmost', True)

# Mostra il messagebox in primo piano
        messagebox.showinfo("TERMINATO", "CSV CREATO CON SUCCESSO!")

# Disabilita l'attributo topmost
        root.attributes('-topmost', False)
    else:
        print('Salvataggio del file annullato')
        root = tk.Tk()
        root.withdraw()  # Nasconde la finestra principale

# Imposta la finestra principale come topmost (sempre in primo piano)
        root.attributes('-topmost', True)
        messagebox.showerror("Annullato", "Salvataggio del file annullato")
        root.attributes('-topmost', False)
    # Chiude la finestra di caricamento
    

if __name__ == "__main__":
    main()
