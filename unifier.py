import os
import pandas as pd
from tkinter import Tk, filedialog, messagebox

def select_folder(title="Seleziona la cartella contenente i file CSV"):
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    return folder_path

def select_save_location(default_name="output.csv"):
    root = Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Salva il file unito come"
    )
    return save_path

def merge_csv_files(input_folder, output_file):
    all_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    df_list = []
    
    for file in all_files:
        df = pd.read_csv(file, delimiter=';')
        
        # Controlla la presenza delle colonne necessarie e gestisci l'assenza
        if 'ULM_IMPIANTO' in df.columns:
            df['ULM_IMPIANTO'] = df['ULM_IMPIANTO'].astype(float).fillna(0).astype(int).astype(str)
        else:
            print(f"Colonna 'ULM_IMPIANTO' non trovata nel file {file}")
            continue  # Salta questo file o gestiscilo in modo appropriato

        if 'DATA' in df.columns:
            df['DATA'] = df['DATA'].astype(float).fillna(0).astype(int).astype(str)
        else:
            print(f"Colonna 'DATA' non trovata nel file {file}")
            continue

        if 'ORA' in df.columns:
            df['ORA'] = df['ORA'].astype(float).fillna(0).astype(int).astype(str)
        else:
            print(f"Colonna 'ORA' non trovata nel file {file}")
            continue

        df_list.append(df)
    
    if df_list:
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df.to_csv(output_file, index=False, sep=';')
        print(f"I file CSV sono stati uniti e salvati in {output_file}")
    else:
        print("Nessun file valido trovato per l'unione.")

def CSVUnifier(check, path_preavvisi=None, path_portion=None):
    preavvisi_output = None
    portion_output = None
    
    if check == 0:
        # Chiede all'utente di selezionare le cartelle se check è 0
        preavvisi_folder = select_folder("Seleziona la cartella contenente i file preavvisi")
        if not preavvisi_folder:
            print("Selezione della cartella 'preavvisi' annullata.")
            return None, None

        portion_folder = select_folder("Seleziona la cartella contenente i file portion")
        if not portion_folder:
            print("Selezione della cartella 'portion' annullata.")
            return None, None

    elif check == 1:
        # Usa i percorsi passati come argomenti se check è 1
        preavvisi_folder = path_preavvisi
        portion_folder = path_portion

    else:
        #stampa errore su una finestra

        messagebox.showerror("Errore", "Valore di check non valido. Usa 0 per selezionare le cartelle o 1 per usare i percorsi passati.")
        #esci dal programma 
        exit()

    # Unisce i file CSV nella cartella preavvisi
    if preavvisi_folder:
        preavvisi_output = select_save_location("preavvisi_output.csv")
        if preavvisi_output:
            merge_csv_files(preavvisi_folder, preavvisi_output)
        else:
            print("Salvataggio del file 'preavvisi' annullato.")

    # Unisce i file CSV nella cartella portion
    if portion_folder:
        portion_output = select_save_location("portion_output.csv")
        if portion_output:
            merge_csv_files(portion_folder, portion_output)
        else:
            print("Salvataggio del file 'portion' annullato.")

    return preavvisi_output, portion_output

if __name__ == "__main__":
    preavvisi_path, portion_path = CSVUnifier(0)
    print(f"Preavvisi Output: {preavvisi_path}")
    print(f"Portion Output: {portion_path}")
