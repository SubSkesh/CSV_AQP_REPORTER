import pandas as pd

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, delimiter=';', low_memory=False)  # Imposta low_memory=False per evitare avvisi
        df.columns = df.columns.str.strip()  # Rimuove spazi extra dai nomi delle colonne
        return df
    except FileNotFoundError:
        print(f"File non trovato: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        print(f"Il file è vuoto: {file_path}")
        raise
    except Exception as e:
        print(f"Errore nella lettura del file: {e}")
        raise

if __name__ == "__main__":
    preavvisi_path = '../data/preavvisi.csv'
    appuntamenti_path = '../data/appuntamenti.csv'
    df_preavvisi = read_csv_file(preavvisi_path)
    df_appuntamenti = read_csv_file(appuntamenti_path)
    print(f'Dati caricati da {preavvisi_path} e {appuntamenti_path}')
