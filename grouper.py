import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

# Creato da Oscar Costanzelli

def wannaselect():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    # Chiede se l'utente vuole selezionare una cartella da suddividere
    risposta = messagebox.askyesno(
        title="RAGGRUPPARE IN SOTTOCARTELLE?",
        message="Vuoi selezionare una cartella da suddividere in sotto cartelle portion e preavvisi?"
    )
    return risposta


def select_folder():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    
    try:
        folder_selected = filedialog.askdirectory(title="Seleziona la cartella contenente i file CSV")
        if not folder_selected:
            raise Exception("Nessuna cartella selezionata.")
    except Exception as e:
        messagebox.showwarning("Attenzione", str(e))
        sys.exit(1)  # Termina il programma con un codice di uscita 1 (errore)
        
    return folder_selected


def get_csv_files(folder):
    # Restituisce i file CSV presenti in una cartella
    files = os.listdir(folder)
    csv_files = [file for file in files if file.endswith('.csv')]
    non_csv_files = [file for file in files if not file.endswith('.csv')]
    if non_csv_files:
        messagebox.showwarning("Attenzione", f"Ci sono file non CSV nella cartella: {non_csv_files}")
    return csv_files

def create_group_folders(base_folder, group_name, csv_files):
    # Crea le cartelle di gruppo e sposta i file
    group_folder = os.path.join(base_folder, group_name)
    os.makedirs(group_folder, exist_ok=True)

    for file in csv_files:
        source_file = os.path.join(base_folder, file)
        destination_file = os.path.join(group_folder, file)
        os.rename(source_file, destination_file)
        print(f"File spostato: {source_file} -> {destination_file}")

    messagebox.showinfo("Completato", f"Tutti i file del gruppo '{group_name}' sono stati spostati in {group_folder}")
    return group_folder  # Restituisce il percorso della cartella creata

def CSVGrouper():
    if wannaselect():
        messagebox.showinfo("OTTIMO", "Ottimo, scegli la cartella")
        folder_selected = select_folder()
    else:
        messagebox.showinfo("ATTENZIONE", "Operazione annullata.")
        return None,None

    csv_files = get_csv_files(folder_selected)
    if not csv_files:
        messagebox.showerror("Errore", "Non ci sono file CSV nella cartella selezionata.")
        return

    # Raggruppa i file CSV in base ai nomi
    preavvisi_files = [file for file in csv_files if "PREAV" in file]
    portion_files = [file for file in csv_files if "PORT" in file]

    preavvisi_folder = None
    portion_folder = None

    if preavvisi_files:
        preavvisi_folder = create_group_folders(folder_selected, "preavvisi", preavvisi_files)
    else:
        messagebox.showwarning("Attenzione", "Nessun file trovato per il gruppo 'preavvisi'")

    if portion_files:
        portion_folder = create_group_folders(folder_selected, "portion", portion_files)
    else:
        messagebox.showwarning("Attenzione", "Nessun file trovato per il gruppo 'portion'")
    
    return preavvisi_folder, portion_folder  # Restituisce i percorsi delle cartelle create

if __name__ == "__main__":
    preavvisi_folder, portion_folder = CSVGrouper()
    print(f"Cartella Preavvisi: {preavvisi_folder}")
    print(f"Cartella Portion: {portion_folder}")
