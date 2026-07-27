# Analisi — App di Yoga ispirata a "Down Dog" (Yoga Buddhi Co.)

> Documento di ricerca e pianificazione. Nessuna riga di codice è stata ancora scritta:
> questo file raccoglie tutte le caratteristiche reperite in rete sull'app di riferimento
> e le domande aperte da chiarire prima di realizzare l'applicazione.

## 1. Identificazione dell'app di riferimento

Lo screenshot fornito è la scheda App Store di **Yoga | Down Dog**, sviluppata da
**Yoga Buddhi Co.** — valutazione ~4,9/5 con oltre 43.000 recensioni (Italia),
oltre 300.000 recensioni a 5 stelle a livello globale. Categoria: Salute e benessere.

Sito ufficiale: https://www.downdogapp.com

## 2. Concetto chiave dell'app

Down Dog **non usa video preregistrati**: è un **motore generativo di sequenze**.
Ad ogni avvio combina un'ampia libreria di pose (video clip + audio del docente +
musica) e produce una pratica **sempre diversa**, coerente con i parametri scelti
dall'utente ("Non fare mai la stessa pratica due volte" — oltre **60.000
configurazioni** possibili).

## 3. Elenco completo delle caratteristiche reperite in rete

### 3.1 Tipi di pratica (stili)
- Vinyasa (default)
- Hatha
- Gentle
- Restorative
- Yin
- Ashtanga
- Chair Yoga (yoga sulla sedia)
- Yoga Nidra
- Hot 26 (sequenza stile Bikram)
- Sun Salutation (saluti al sole)
- Cardio Flow
- Wake-Up Yoga (pratica breve del risveglio)

### 3.2 Livelli di difficoltà (5)
1. Principiante 1
2. Principiante 2
3. Intermedio 1
4. Intermedio 2
5. Avanzato

### 3.3 Personalizzazione della pratica
- **Durata** libera (da pochi minuti a oltre un'ora, con timer circolare)
- **Boost**: focus primario e secondario su **19 aree del corpo** (schiena bassa,
  core, apertura anche, spalle, hamstring, backbend, ecc.)
- **Ritmo/pace** regolabile (più lento ↔ più veloce)
- **Durata della savasana** regolabile
- **Like/Dislike delle pose**: le pose "piaciute" appaiono più spesso, quelle
  "non piaciute" non appaiono mai più (schermata "Pose nella tua pratica" con
  filtri Tutte / Piaciute / Non piaciute)
- Ricerca nella libreria delle pose

### 3.4 Audio e voce
- **6 voci di insegnanti** in inglese tra cui scegliere
- Pratiche disponibili in **13 lingue**: inglese, spagnolo, portoghese, francese,
  tedesco, **italiano**, russo, mandarino, giapponese, coreano, turco, polacco, ucraino
- **Musica adattiva** che sale e scende col respiro; generi: ambient, acustica,
  onde cerebrali (brain waves), suoni della natura, spirituale; volume di voce e
  musica regolabili separatamente

### 3.5 Monitoraggio e motivazione
- Tab **Journey/Progressi**: streak giornaliero, obiettivi giornalieri/settimanali/mensili
- Statistiche configurabili (tempo totale di pratica, pratiche al mese, streak corrente)
- **Cronologia** delle pratiche completate, con indicatore "Oggi hai completato la tua pratica!"
- **Preferiti**: salvataggio di una pratica per rifarla identica
- **Promemoria** di pratica configurabili

### 3.6 Piattaforme e distribuzione
- iOS / iPadOS, Android, **versione Web** (browser)
- **Chromecast** per lo streaming su TV (da iOS, Android e Web); AirPlay su iOS
- **Download offline** delle pratiche
- Un unico account/abbonamento valido su tutte le piattaforme

### 3.7 Famiglia di app collegate (stesso abbonamento)
- Yoga | Down Dog
- Meditation | Down Dog
- Pilates | Down Dog
- HIIT | Down Dog
- Barre | Down Dog
- Prenatal Yoga | Down Dog
- 7 Minute Workout | Down Dog

(Nello screenshot: onboarding con scelta tra Yoga, Meditazione, Pilates, HIIT.)

### 3.8 Integrazioni
- **Apple Health** (registrazione minuti di allenamento) — il supporto a Google Fit
  è stato dismesso

### 3.9 Modello di business
- Freemium con **prova gratuita** (storicamente fino a 22 giorni; varia nel tempo)
- Abbonamento: ~7,99–9,99 $/mese oppure ~39,99–59,99 $/anno (varia per regione
  e piattaforma); acquisti in-app su App Store / Play Store
- Sconti storici per studenti/insegnanti e operatori sanitari

### 3.10 Nota su "skill e plugin"
Down Dog **non ha un sistema pubblico di plugin o estensioni di terze parti**:
è un'app proprietaria monolitica. Ciò che nella richiesta è chiamato "plugin"
corrisponde ai **moduli funzionali** elencati sopra (motore generativo, boost,
voci, musica adattiva, streak, offline, cast, famiglia di app).

## 4. Vincolo legale importante

Non è possibile creare un'app **"uguale"**: nome "Down Dog", logo del cagnolino,
grafica, video, audio e musica sono protetti da copyright e marchio registrato.
Si può invece realizzare legittimamente un'app **con le stesse funzionalità**
(motore generativo di sequenze, personalizzazione, streak, ecc.) con nome,
grafica e contenuti originali.

## 5. Domande aperte prima della realizzazione

1. **Piattaforma**: web app (PWA usabile anche da telefono), app nativa
   iOS/Android (React Native/Flutter), o entrambe? → proposta: partire dalla web app.
2. **Contenuti pose**: non possiamo usare i video di Down Dog. Opzioni:
   illustrazioni/animazioni SVG delle pose, foto proprie, o solo audio+testo?
3. **Lingua**: solo italiano, o italiano + inglese?
4. **Audio guida**: voce sintetica (TTS), registrazioni proprie, o solo testo a schermo?
5. **Stili da includere nella v1**: tutti i 12, o un sottoinsieme (es. Vinyasa,
   Hatha, Gentle, Yin)?
6. **Account e backend**: serve login con salvataggio su server, o basta il
   salvataggio locale sul dispositivo per la v1?
7. **Modello di business**: app gratuita personale o abbonamento con paywall?
8. **Musica**: libreria royalty-free integrata o nessuna musica nella v1?
9. **Nome e identità visiva** dell'app (serve un nome originale).
10. **Extra**: includere fin da subito anche Meditazione/Pilates/HIIT (come
    nell'onboarding dello screenshot) o solo Yoga nella v1?
