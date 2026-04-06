"""
Backend FastAPI per AI Prompt Explainer.
Analizza un prompt mostrando tokenizzazione, struttura, entità,
ragionamento semplificato e risposta finale da un modello AI.
"""

import json
import re
import os
from typing import Optional

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="AI Prompt Explainer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve app.html direttamente dal backend."""
    html_path = BASE_DIR / "app.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


class AnalyzeRequest(BaseModel):
    prompt: str
    provider: str  # "openai", "anthropic" o "demo"
    api_key: str = ""


class AnalyzeResponse(BaseModel):
    tokens: list[str]
    structure: dict
    entities: list[dict]
    reasoning_steps: list[str]
    final_output: str


# --- Tokenizzazione semplice via regex ---

def tokenize(text: str) -> list[str]:
    """Divide il testo in token (parole, punteggiatura, numeri)."""
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)


# --- Analisi struttura prompt ---

def analyze_structure(text: str) -> dict:
    """Rileva istruzioni, contesto, vincoli di stile nel prompt."""
    text_lower = text.lower()

    instruction_patterns = [
        r"(?:scrivi|genera|crea|elenca|spiega|traduci|riassumi|descrivi|calcola|trova|analizza|rispondi|dimmi|fammi|fornisci|prepara|elabora|componi)\b",
        r"(?:write|generate|create|list|explain|translate|summarize|describe|calculate|find|analyze|answer|tell me|make|provide|prepare|compose)\b",
    ]
    instructions = []
    for pattern in instruction_patterns:
        matches = re.findall(pattern, text_lower)
        instructions.extend(matches)
    instructions = list(set(instructions))

    context_keywords = []
    context_patterns = [
        (r"(?:come se fossi|agisci come|sei un|immagina di essere|nel ruolo di|in qualità di)", "ruolo/persona"),
        (r"(?:act as|you are|imagine you are|as a|in the role of)", "role/persona"),
        (r"(?:contesto|sfondo|background|situazione)", "contesto esplicito"),
        (r"(?:context|background|situation)", "explicit context"),
    ]
    for pattern, label in context_patterns:
        if re.search(pattern, text_lower):
            context_keywords.append(label)

    style_keywords = []
    style_patterns = [
        (r"(?:formale|informale|professionale|amichevole|tecnico|semplice|breve|dettagliato|conciso)", "stile"),
        (r"(?:formal|informal|professional|friendly|technical|simple|brief|detailed|concise)", "style"),
        (r"(?:in formato|come elenco|in tabella|in json|in markdown|punto per punto|bullet)", "formato output"),
        (r"(?:in format|as a list|as a table|in json|in markdown|step by step|bullet)", "output format"),
        (r"(?:massimo \d+ parole|almeno \d+ parole|in \d+ righe|max \d+ words)", "vincolo lunghezza"),
    ]
    for pattern, label in style_patterns:
        if re.search(pattern, text_lower):
            style_keywords.append(label)

    constraints = []
    constraint_patterns = [
        (r"(?:non|senza|evita|escludi|non usare|non includere)", "negazione/esclusione"),
        (r"(?:don't|do not|without|avoid|exclude|never)", "negation/exclusion"),
        (r"(?:solo|soltanto|esclusivamente|unicamente|only|just|exclusively)", "restrizione"),
    ]
    for pattern, label in constraint_patterns:
        if re.search(pattern, text_lower):
            constraints.append(label)

    return {
        "istruzioni_rilevate": instructions if instructions else ["nessuna istruzione esplicita rilevata"],
        "contesto": context_keywords if context_keywords else ["nessun contesto esplicito"],
        "stile_e_formato": style_keywords if style_keywords else ["nessun vincolo di stile esplicito"],
        "vincoli": constraints if constraints else ["nessun vincolo esplicito"],
    }


# --- Estrazione entità ---

def extract_entities(text: str) -> list[dict]:
    """Estrae entità base: email, date, numeri, nomi propri."""
    entities = []

    for m in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
        entities.append({"tipo": "email", "valore": m.group()})

    for m in re.finditer(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text):
        entities.append({"tipo": "data", "valore": m.group()})
    for m in re.finditer(r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b", text):
        entities.append({"tipo": "data", "valore": m.group()})

    for m in re.finditer(r"\b\d+(?:[.,]\d+)?(?:\s*(?:%|€|\$|USD|EUR|kg|km|m|cm|mm|gb|mb|tb))\b", text, re.IGNORECASE):
        entities.append({"tipo": "numero/misura", "valore": m.group()})

    for m in re.finditer(r"\b(?:[A-Z][a-zà-ü]+)(?:\s+[A-Z][a-zà-ü]+)+\b", text):
        val = m.group()
        if len(val) > 3:
            entities.append({"tipo": "nome proprio (possibile)", "valore": val})

    for m in re.finditer(r"(?:https?://|www\.)\S+", text):
        entities.append({"tipo": "URL", "valore": m.group()})

    seen = set()
    unique = []
    for e in entities:
        key = (e["tipo"], e["valore"])
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique


# --- Chiamata AI ---

SYSTEM_PROMPT = """Sei un assistente didattico che spiega come un modello AI elabora un prompt.

L'utente ti invierà un prompt. Tu devi:
1. Spiegare in 4-6 passaggi semplici come il modello "ragiona" per elaborare quel prompt.
   Ogni passaggio deve essere una frase chiara, in italiano, comprensibile da un utente non tecnico.
   Usa un tono divulgativo e amichevole.
2. Fornire la risposta finale che il modello genererebbe per quel prompt.

IMPORTANTE: Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza testo aggiuntivo, in questo formato:
{
  "reasoning_steps": [
    "Passaggio 1: ...",
    "Passaggio 2: ...",
    "Passaggio 3: ...",
    "Passaggio 4: ..."
  ],
  "final_output": "La risposta completa al prompt..."
}"""


async def call_openai(prompt: str, api_key: str) -> dict:
    """Chiama l'API OpenAI."""
    import httpx

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Analizza questo prompt:\n\n{prompt}"},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
            )
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail="Impossibile raggiungere l'API OpenAI. Verifica la connessione di rete.")
    except httpx.ProxyError as e:
        raise HTTPException(status_code=502, detail="Connessione bloccata dal proxy. Prova la modalità Demo oppure esegui l'app in locale.")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout nella chiamata a OpenAI. Riprova.")

    if response.status_code != 200:
        detail = response.text
        raise HTTPException(status_code=response.status_code, detail=f"Errore OpenAI: {detail}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return parse_ai_response(content)


async def call_anthropic(prompt: str, api_key: str) -> dict:
    """Chiama l'API Anthropic (Claude)."""
    import httpx

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 2000,
                    "system": SYSTEM_PROMPT,
                    "messages": [
                        {"role": "user", "content": f"Analizza questo prompt:\n\n{prompt}"},
                    ],
                },
            )
    except httpx.ConnectError as e:
        raise HTTPException(status_code=502, detail="Impossibile raggiungere l'API Anthropic. Verifica la connessione di rete.")
    except httpx.ProxyError as e:
        raise HTTPException(status_code=502, detail="Connessione bloccata dal proxy. Prova la modalità Demo oppure esegui l'app in locale.")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout nella chiamata ad Anthropic. Riprova.")

    if response.status_code != 200:
        detail = response.text
        raise HTTPException(status_code=response.status_code, detail=f"Errore Anthropic: {detail}")

    data = response.json()
    content = data["content"][0]["text"]
    return parse_ai_response(content)


def generate_demo_response(prompt: str) -> dict:
    """Genera una risposta demo senza chiamare API esterne."""
    text_lower = prompt.lower()

    # Genera reasoning steps contestuali
    steps = [
        f"Passaggio 1: Il modello riceve il prompt composto da {len(prompt.split())} parole e lo analizza per capire cosa viene chiesto.",
    ]

    if any(w in text_lower for w in ["scrivi", "genera", "crea", "write", "create", "generate"]):
        steps.append("Passaggio 2: Viene riconosciuta una richiesta di creazione/scrittura. Il modello prepara una struttura per il contenuto.")
    elif any(w in text_lower for w in ["spiega", "explain", "descrivi", "describe"]):
        steps.append("Passaggio 2: Viene riconosciuta una richiesta di spiegazione. Il modello organizza le informazioni in modo chiaro.")
    elif any(w in text_lower for w in ["traduci", "translate"]):
        steps.append("Passaggio 2: Viene riconosciuta una richiesta di traduzione. Il modello identifica la lingua di partenza e di arrivo.")
    else:
        steps.append("Passaggio 2: Il modello analizza il tipo di richiesta e cerca di capire l'intento dell'utente.")

    steps.append("Passaggio 3: Vengono identificati i dettagli chiave: persone, date, numeri, contesto e qualsiasi vincolo specificato.")
    steps.append("Passaggio 4: Il modello attinge alle sue conoscenze per elaborare una risposta pertinente e completa.")
    steps.append("Passaggio 5: La risposta viene formulata nel tono e nel formato più appropriati alla richiesta.")

    return {
        "reasoning_steps": steps,
        "final_output": f"[Modalità Demo] Questa è una risposta dimostrativa. In modalità reale (con API key OpenAI o Anthropic), qui apparirà la risposta effettiva del modello AI al prompt:\n\n\"{prompt}\"\n\nPer ottenere risposte reali, seleziona OpenAI o Anthropic e inserisci una API key valida.",
    }


def parse_ai_response(content: str) -> dict:
    """Estrae JSON dalla risposta AI con fallback robusto."""
    # Prova parsing diretto
    try:
        parsed = json.loads(content)
        if "reasoning_steps" in parsed and "final_output" in parsed:
            return parsed
    except json.JSONDecodeError:
        pass

    # Cerca blocco JSON nel testo
    json_match = re.search(r"\{[\s\S]*\}", content)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            if "reasoning_steps" in parsed and "final_output" in parsed:
                return parsed
        except json.JSONDecodeError:
            pass

    # Fallback: usa il contenuto grezzo
    return {
        "reasoning_steps": [
            "Il modello ha ricevuto il prompt e lo ha analizzato.",
            "Ha identificato il tipo di richiesta e il contesto.",
            "Ha elaborato una risposta basata sulle sue conoscenze.",
            "Ha formulato la risposta nel formato più appropriato.",
        ],
        "final_output": content,
    }


# --- Endpoint principale ---

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Il prompt non può essere vuoto.")
    if req.provider not in ("openai", "anthropic", "demo"):
        raise HTTPException(status_code=400, detail="Provider non supportato. Usa 'openai', 'anthropic' o 'demo'.")
    if req.provider != "demo" and not req.api_key.strip():
        raise HTTPException(status_code=400, detail="La API key è obbligatoria per il provider selezionato.")

    tokens = tokenize(req.prompt)
    structure = analyze_structure(req.prompt)
    entities = extract_entities(req.prompt)

    if req.provider == "demo":
        ai_result = generate_demo_response(req.prompt)
    elif req.provider == "openai":
        ai_result = await call_openai(req.prompt, req.api_key)
    else:
        ai_result = await call_anthropic(req.prompt, req.api_key)

    return AnalyzeResponse(
        tokens=tokens,
        structure=structure,
        entities=entities,
        reasoning_steps=ai_result["reasoning_steps"],
        final_output=ai_result["final_output"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
