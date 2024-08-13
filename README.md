
# CSV Merger & Analyzer

Questo progetto è un'applicazione Python progettata per unire, analizzare e elaborare file CSV contenenti dati di preavvisi e appuntamenti. L'applicazione permette di combinare dati da diverse sorgenti, effettuare calcoli specifici e salvare i risultati in un nuovo file CSV.

## Funzionalità

- **Unione di File CSV**: Unisce i dati di preavvisi e appuntamenti basandosi su colonne comuni.
- **Conversione di Date e Ore**: Converte i formati di data e ora in modo coerente per l'elaborazione.
- **Calcolo di Confronti Temporali**: Calcola differenze di tempo tra date e ore e valuta se gli appuntamenti sono stati eseguiti correttamente.
- **Gestione delle Sanzioni**: Assegna sanzioni basate su condizioni predefinite legate al tempo di preavviso e all'esecuzione dell'appuntamento.
- **Animazione di Benvenuto**: Mostra un'animazione all'avvio del programma per migliorare l'esperienza utente.

## Requisiti

- Python 3.x
- Librerie Python: `pandas`, `tkinter`, `Pillow`

## Installazione

1. **Clona il repository**:

   ```bash
   git clone https://github.com/tuo-username/csv-merger-analyzer.git
   cd csv-merger-analyzer
   ```

2. **Installa le dipendenze**:

   Assicurati di avere `pip` installato, poi esegui:

   ```bash
   pip install pandas Pillow
   ```

## Utilizzo

1. **Avviare l'applicazione**:

   Esegui il file `main.py`:

   ```bash
   python main.py
   ```

2. **Selezione dei file**:

   Durante l'esecuzione, l'applicazione ti chiederà di selezionare i file CSV contenenti i dati di preavvisi e appuntamenti. Se i file non sono pre-selezionati, verrà aperta una finestra per scegliere manualmente i file.

3. **Elaborazione dei dati**:

   L'applicazione unirà i dati, eseguirà calcoli sulle date e ore, e ti permetterà di visualizzare i risultati direttamente nel terminale.

4. **Salvataggio dei risultati**:

   Alla fine dell'elaborazione, ti verrà chiesto di scegliere dove salvare il file CSV risultante.

## Contribuire

Se desideri contribuire al progetto, sentiti libero di fare un fork del repository, creare un branch per le tue modifiche, e inviare una pull request.

```bash
git checkout -b nuova-funzionalità
git commit -m "Aggiunge una nuova funzionalità"
git push origin nuova-funzionalità
```

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Consulta il file [LICENSE](LICENSE) per maggiori dettagli.
