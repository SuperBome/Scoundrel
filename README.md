# 🎮 Scoundrel

Un prototipo di gioco di carte 2D in stile rogue-like dungeon crawler, creato con [Pygame](https://www.pygame.org/news). Immergiti in un'atmosfera oscura, gestisci la tua mano di carte e sopravvivi stanza dopo stanza. **Scoundrel** è una base solida e in continua evoluzione per un'avventura completa.

![Screenshot del gameplay di Scoundrel](https'immagine che hai fornito.png)

---

## 📜 Come si Gioca

L'obiettivo è superare una serie di "stanze" rappresentate da quattro carte pescate dal mazzo.

- **Azioni**: Seleziona una carta per vedere quale azione si attiva. Ogni seme corrisponde a un'azione diversa:
    - **Picche (♠️) e Fiori (♣️)**: Mostri da sconfiggere. Attivano l'azione **Combatti**.
    - **Cuori (♥️)**: Pozioni di guarigione. Attivano l'azione **Cura**.
    - **Quadri (♦️)**: Armi. Attivano l'azione **Raccogli**.
- **Progressione**: Dopo aver giocato tre carte, la stanza viene riempita con tre nuove carte dal mazzo, mantenendo l'ultima carta giocata. La tua avventura continua con una nuova mano.
- **Fuga**: All'inizio di ogni nuova mano, hai la possibilità di **fuggire**. Questa azione rimescola le carte in gioco nel mazzo e te ne presenta quattro nuove, ma può essere usata solo se non hai ancora compiuto un'azione in quella stanza. Scegli saggiamente!

---

## 🚀 Come Eseguire il Gioco

### 1. Prerequisiti

Assicurati di avere installato **Python 3.9+** e la libreria `pygame`.

```
pip install pygame
```

### 2. Avvio

Clona il repository e avvia il gioco con:

```
git clone https://github.com/tuonomeutente/scoundrel.git
cd scoundrel
python main.py
```

---

### 🎯 Funzionalità attuali

- ✨ Menu Principale Interattivo: Pulsanti con effetto hover per avviare, accedere alle opzioni o uscire.
- 🎬 Transizioni Animate: Dissolvenze fluide tra le diverse schermate per un'esperienza più gradevole.
- 🕹️ Logica di Gioco Base:
  - Sistema di pesca e gestione delle mani di carte.
  - Interfaccia dinamica con pulsanti azione (Combatti, Cura, Raccogli) che si attivano in base alla carta selezionata.
  - Meccanica di progressione tra le "stanze".
  - Funzione strategica di "Fuga" per cambiare una mano sfavorevole.
- 🔊 Supporto per asset audio e grafici
- 🔙 Pulsanti "Indietro" e "Esci"

### 🛠️ Struttura del progetto

```text
scoundrel/
│
├── assets/
│   ├── images/
│   │   ├── ui/         # Elementi dell'interfaccia (pulsanti, sfondi)
│   │   └── cards/      # Sprite delle carte
│   ├── fonts/          # Font utilizzati nel gioco
│   └── sounds/         # Cartella per musica ed effetti sonori, attualmente vuota          
├── deck.py             # Classe per la gestione del mazzo di carte
├── main.py             # Loop principale e logica di gioco
└── README.md
```

### 🧪 In sviluppo

- Effetti delle Azioni: Implementare le conseguenze reali delle azioni Combatti, Cura e Raccogli.
- Audio: Aggiungere musica di sottofondo ed effetti sonori per le azioni.
- Schermata Opzioni: Completare la schermata delle opzioni con controlli per volume e altre impostazioni.

### 🔨 Autore
Sviluppato da Domenico Romano
