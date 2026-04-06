# AI Prompt Explainer

App didattica che mostra, passo dopo passo, come un modello di intelligenza artificiale analizza ed elabora un prompt.

## Funzionalità

1. **Tokenizzazione** — Il prompt viene suddiviso in token (parole, numeri, punteggiatura)
2. **Analisi struttura** — Vengono identificate istruzioni, contesto, stile e vincoli
3. **Estrazione entità** — Nomi, date, email, numeri e altri dati vengono evidenziati
4. **Ragionamento semplificato** — Il modello AI genera una spiegazione didattica dei passaggi logici
5. **Risposta finale** — L'output completo generato dal modello

## Requisiti

- Python 3.10+
- Una API key OpenAI oppure Anthropic

## Installazione

```bash
pip install fastapi uvicorn httpx
```

## Configurazione API Key

La API key viene inserita direttamente nell'interfaccia web. In alternativa, puoi creare un file `.env` per riferimento:

```env
# .env (esempio)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-api03-...
```

> **Nota:** il backend non legge il file `.env` automaticamente — la chiave viene passata dal frontend ad ogni richiesta. Il file `.env` serve solo come promemoria personale.

## Avvio

### 1. Avvia il backend

```bash
python backend.py
```

Oppure con uvicorn direttamente:

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

Il server sarà disponibile su `http://localhost:8000`.

### 2. Apri il frontend

Apri il file `app.html` direttamente nel browser:

- Doppio clic sul file, oppure
- Da terminale: `open app.html` (macOS) / `xdg-open app.html` (Linux) / `start app.html` (Windows)

Il frontend si collega automaticamente al backend su `http://localhost:8000`.

## Utilizzo

1. Scrivi un prompt nella textarea
2. Seleziona il provider (OpenAI o Anthropic)
3. Inserisci la tua API key
4. Clicca **Analizza il prompt**
5. Esplora i 5 passaggi dell'analisi

Premi **Ctrl+Invio** nella textarea per avviare l'analisi rapidamente.

## Nota sulle API Key

- Le chiavi API vengono inviate al backend solo per effettuare la chiamata al modello
- Non vengono memorizzate né salvate su disco
- In ambiente di produzione, valuta l'uso di variabili d'ambiente lato server

## Disclaimer

Questo strumento ha finalità esclusivamente **didattiche**. I passaggi mostrati (tokenizzazione, ragionamento, ecc.) sono una ricostruzione semplificata a scopo divulgativo e non rappresentano il funzionamento tecnico interno reale del modello AI.
