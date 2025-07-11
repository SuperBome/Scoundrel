import pygame
import os
import random
from deck import CardDeck

# =========================
# COSTANTI E INIZIALIZZAZIONE
# =========================

WIDTH, HEIGHT = 1280, 896  # Dimensioni finestra
FPS = 60                   # Frame per secondo
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

DECK_POS = (150, 150) # Posizione del mazzo
GAME_POS = [(350, 180), (495, 180), (640, 180), (785, 180)]  # Posizioni delle carte in gioco
DISCARD_POS = (985, 150)  # Posizione del mazzo degli scarti

pygame.display.set_caption("SCOUNDREL")

LIFT_AMOUNT = 15 # Quanti pixel sollevare la carta selezionata
DARK_RED = (139, 0, 0) # Colore per l'highlight di selezione

pygame.font.init()
FONT_PATH = os.path.join("assets", "fonts", "Jersey15-Regular.ttf")
FONT = pygame.font.Font(FONT_PATH, 36)
VICTORY_FONT = pygame.font.Font(FONT_PATH, 96)

deck = CardDeck(os.path.join("assets", "images", "cards", "cards_tileMap.png"))

global carte_pescate, nomi_pescati, scarti, player_interacted_this_turn, fuga_usata_nel_turno_precedente
                        

# =========================
# CARICAMENTO ASSETS
# =========================

# Backgrounds
MENU_BG = pygame.image.load(os.path.join("assets", "images", "ui", "menu_bg_blur.png"))
GAME_BG = pygame.image.load(os.path.join("assets", "images", "ui", "game_bg_blur.png"))
OPTIONS_BG = pygame.image.load(os.path.join("assets", "images", "ui", "options_bg_blur.png"))
WINNING_BG = pygame.image.load(os.path.join("assets", "images", "ui", "winning_bg_blur.png"))

# Banner
BANNER_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "banner.png"))
BANNER = pygame.transform.scale(BANNER_IMG, (700, 300))

# Pulsanti menu
NEW_GAME_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "ng_btn.png"))
NEW_GAME = pygame.transform.scale(NEW_GAME_BTN, (450, 200))
NEW_GAME_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "ng_btn_hover.png"))
NEW_GAME_HOVER = pygame.transform.scale(NEW_GAME_BTN_HOVER, (450, 200))

OPTION_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "optn_btn.png"))
OPTION = pygame.transform.scale(OPTION_BTN, (300, 130))
OPTION_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "optn_btn_hover.png"))
OPTION_HOVER = pygame.transform.scale(OPTION_BTN_HOVER, (300, 130))

EXIT_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "exit_btn.png"))
EXIT = pygame.transform.scale(EXIT_BTN, (105, 100))
EXIT_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "exit_btn_hover.png"))
EXIT_HOVER = pygame.transform.scale(EXIT_BTN_HOVER, (105, 100))

# Pulsante indietro
BACK_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "back_btn.png"))
BACK = pygame.transform.scale(BACK_BTN, (160, 100))
BACK_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "back_btn_hover.png"))
BACK_HOVER = pygame.transform.scale(BACK_BTN_HOVER, (160, 100))

# Pulsante fuggi
ESCAPE_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "escape_btn.png"))
ESCAPE = pygame.transform.scale(ESCAPE_BTN, (160, 100)) 
ESCAPE_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "escape_btn_hover.png"))
ESCAPE_HOVER = pygame.transform.scale(ESCAPE_BTN_HOVER, (160, 100))
ESCAPE_DISABLED = ESCAPE.copy()
ESCAPE_DISABLED.set_alpha(100)

# Tavolo
TABLE_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "table.png"))

# Pergamena
SCROLL_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "scroll_test_2.png"))

# Dimensioni dei pulsanti azione
BTN_WIDTH, BTN_HEIGHT = 230, 90  # Dimensioni standard per i pulsanti azione

# Pulsante COMBATTI
FIGHT_BTN_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "fight_btn.png"))
FIGHT_BTN = pygame.transform.scale(FIGHT_BTN_IMG, (300, 270))
FIGHT_BTN_DISABLED = FIGHT_BTN.copy()
FIGHT_BTN_DISABLED.set_alpha(100)

# Pulsante CURA
HEAL_BTN_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "heal_btn.png"))
HEAL_BTN = pygame.transform.scale(HEAL_BTN_IMG, (300, 270))
HEAL_BTN_DISABLED = HEAL_BTN.copy()
HEAL_BTN_DISABLED.set_alpha(100)

# Pulsante RACCOGLI
PICKUP_BTN_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "pickup_btn.png"))
PICKUP_BTN = pygame.transform.scale(PICKUP_BTN_IMG, (300, 270))
PICKUP_BTN_DISABLED = PICKUP_BTN.copy()
PICKUP_BTN_DISABLED.set_alpha(100)

# Scritta vittoria
VICTORY_TEXT = pygame.image.load(os.path.join("assets", "images", "ui", "win_text.png"))
VICTORY = pygame.transform.scale(VICTORY_TEXT, (1000, 800))

# =========================
# CLASSI DI TRANSIZIONE (FADE)
# =========================
class FadeOutTransition(pygame.sprite.Sprite):
    """
    Dissolvenza verso nero (fade-out): copre la schermata con una superficie nera crescente.
    """
    def __init__(self):
        super().__init__()
        self.width, self.height = pygame.display.get_window_size()
        self.image = pygame.Surface((self.width, int(self.height * 1.5))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 0
        self.image.fill((0, 0, 0, self.alpha))
        self.transitioning = True

    def update(self, dt):
        self.check_for_transition_complete()
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha <= 240:
            self.alpha += 10

    def check_for_transition_complete(self):
        if self.alpha > 240:
            self.transitioning = False

    def is_transitioning(self):
        return self.transitioning

class FadeInTransition(pygame.sprite.Sprite):
    """
    Dissolvenza da nero a trasparente (fade-in): scopre la schermata togliendo la superficie nera.
    """
    def __init__(self):
        super().__init__()
        self.width, self.height = pygame.display.get_window_size()
        self.image = pygame.Surface((self.width, int(self.height * 1.5))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 255
        self.image.fill((0, 0, 0, self.alpha))
        self.transitioning = True

    def update(self, dt):
        self.check_for_transition_complete()
        self.image.fill((0, 0, 0, self.alpha))
        if self.alpha >= 15:
            self.alpha -= 10

    def check_for_transition_complete(self):
        if self.alpha < 15:
            self.transitioning = False

    def is_transitioning(self):
        return self.transitioning
# =========================
# FUNZIONI DI DISEGNO SCHERMATE
# =========================

def draw_starting_window():
    """
    Disegna il menu principale con:
    - Banner
    - Pulsante Nuova Partita (hover)
    - Pulsante Opzioni (hover)
    - Pulsante Exit (hover)
    Restituisce i rect dei pulsanti e la posizione del mouse.
    """
    WIN.blit(MENU_BG, (0, 0))
    WIN.blit(BANNER, (WIDTH // 2 - BANNER.get_width() // 2, HEIGHT // 2 - BANNER.get_height() // 2 - 220))
    
    mouse_pos = pygame.mouse.get_pos()
    new_game_rect = NEW_GAME.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    option_rect = OPTION.get_rect(center=(WIDTH // 2, HEIGHT // 2 + NEW_GAME.get_height() // 2 + 50 + OPTION.get_height() // 2))
    exit_rect = EXIT.get_rect(bottomleft=(30, HEIGHT - 30))

    # Gestione hover per ogni pulsante
    if new_game_rect.collidepoint(mouse_pos):
        WIN.blit(NEW_GAME_HOVER, new_game_rect.topleft)
    else:
        WIN.blit(NEW_GAME, new_game_rect.topleft)

    if option_rect.collidepoint(mouse_pos):
        WIN.blit(OPTION_HOVER, option_rect.topleft)
    else:
        WIN.blit(OPTION, option_rect.topleft)

    if exit_rect.collidepoint(mouse_pos):
        WIN.blit(EXIT_HOVER, exit_rect.topleft)
    else:
        WIN.blit(EXIT, exit_rect.topleft)

    pygame.display.update()
    return new_game_rect, option_rect, exit_rect, mouse_pos

def pesca_4_carte(deck):
    global mazzo, carte_pescate, nomi_pescati
    scelte = mazzo[:4]
    carte_pescate = [deck.get(nome, GAME_POS[i]) for i, nome in enumerate(scelte)]
    nomi_pescati = scelte
    mazzo = mazzo[4:]
    return carte_pescate, nomi_pescati

def pesca_tre_nuove_carte():
    """
    Pesca 3 carte dal mazzo e le aggiunge a quella rimasta in gioco,
    posizionandole negli slot liberi.
    """
    global mazzo, carte_pescate, nomi_pescati, deck, player_interacted_this_turn, fuga_usata_nel_turno_precedente

    # Controlla se ci sono abbastanza carte da pescare
    if len(mazzo) < 3:
        print("Non ci sono abbastanza carte nel mazzo per riempire la stanza!")
        # Qui potresti inserire una logica di fine gioco o di rimescolamento degli scarti
        return

    # Trova le posizioni libere sul tavolo
    posizioni_occupate = {card.rect.topleft for card in carte_pescate}
    posizioni_disponibili = [pos for pos in GAME_POS if pos not in posizioni_occupate]
    
    # Pesca le prime 3 carte dal mazzo
    carte_da_aggiungere_nomi = mazzo[:3]
    mazzo = mazzo[3:] # Rimuovi le carte pescate dal mazzo

    # Crea gli oggetti carta e aggiungili alla mano
    for i, nome_carta in enumerate(carte_da_aggiungere_nomi):
        if i < len(posizioni_disponibili):
            nuova_posizione = posizioni_disponibili[i]
            nuova_carta = deck.get(nome_carta, nuova_posizione)
            carte_pescate.append(nuova_carta)
            nomi_pescati.append(nome_carta)
    
    print("Pesca di 3 nuove carte completata.")
    # All'inizio di una nuova "mano", il giocatore non ha ancora interagito
    # e può di nuovo fuggire (se non lo ha fatto nel turno precedente).
    player_interacted_this_turn = False
    fuga_usata_nel_turno_precedente = False

def pesca_rimanenti_carte():
    """
    Pesca tutte le carte rimanenti nel mazzo e le aggiunge a quella rimasta,
    posizionandole negli slot liberi.
    """
    
    global mazzo, carte_pescate, nomi_pescati, deck, player_interacted_this_turn, fuga_usata_nel_turno_precedente

    # Trova le posizioni libere sul tavolo
    posizioni_occupate = {card.rect.topleft for card in carte_pescate}
    posizioni_disponibili = [pos for pos in GAME_POS if pos not in posizioni_occupate]

    # Pesca tutte le carte rimanenti nel mazzo
    carte_da_aggiungere_nomi = mazzo[:]
    mazzo.clear()  # Svuota il mazzo

    # Crea gli oggetti carta e aggiungili alla mano
    for i, nome_carta in enumerate(carte_da_aggiungere_nomi):
        if i < len(posizioni_disponibili):
            nuova_posizione = posizioni_disponibili[i]
            nuova_carta = deck.get(nome_carta, nuova_posizione)
            carte_pescate.append(nuova_carta)
            nomi_pescati.append(nome_carta)

    print("Pesca delle carte rimanenti completata.")
    # All'inizio di una nuova "mano", il giocatore non ha ancora interagito
    # e può di nuovo fuggire (se non lo ha fatto nel turno precedente).
    player_interacted_this_turn = False
    fuga_usata_nel_turno_precedente = False

def draw_game_window(selected_card):
    """
    Disegna la schermata di gioco, gestendo dinamicamente l'aspetto dei pulsanti azione
    in base alla carta selezionata.
    """
    WIN.blit(GAME_BG, (0, 0))
    WIN.blit(TABLE_IMG, (0, HEIGHT / 5))
    WIN.blit(SCROLL_IMG, (0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    
    # --- Disegna Pile e Testi ---
    draw_mazzo_pila()
    draw_scarti_pila()
    num_carte_rimaste = len(mazzo)
    text = FONT.render(f"Carte rimaste: {num_carte_rimaste}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    WIN.blit(text, text_rect)

    # --- Disegna le 4 Carte in Gioco (con logica di selezione/hover) ---
    for card in carte_pescate:
        draw_pos = card.rect.topleft
        is_selected = (card == selected_card)

        if is_selected:
            lifted_pos = (card.rect.x, card.rect.y - LIFT_AMOUNT)
            border_rect = pygame.Rect(lifted_pos, (card.rect.width, card.rect.height)).inflate(8, 8)
            pygame.draw.rect(WIN, DARK_RED, border_rect, border_radius=8, width=4)
            draw_pos = lifted_pos
        elif card.rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, (255, 255, 255), card.rect.inflate(8, 8), border_radius=8, width=4)
        
        WIN.blit(card.image, draw_pos)

    # --- Logica di abilitazione e disegno dei pulsanti azione ---
    
    # 1. Definisci lo stato di default (disabilitato)
    fight_enabled = False
    heal_enabled = False
    pickup_enabled = False

    # 2. Se una carta è selezionata, controlla il suo seme e abilita il pulsante corrispondente
    if selected_card:
        card_name = selected_card.name
        if "spades" in card_name or "clubs" in card_name:
            fight_enabled = True
        elif "hearts" in card_name:
            heal_enabled = True
        elif "diamonds" in card_name:
            pickup_enabled = True

    # 3. Definisci le posizioni e i rect dei pulsanti
    fight_rect = FIGHT_BTN.get_rect(center=(WIDTH // 2 - 180, 630))
    heal_rect = HEAL_BTN.get_rect(center=(WIDTH // 2 + 180, 630))
    pickup_rect = PICKUP_BTN.get_rect(center=(WIDTH // 2, 750))

    # 4. Disegna il pulsante corretto (abilitato o disabilitato) in base allo stato
    if fight_enabled:
        WIN.blit(FIGHT_BTN, fight_rect)
    else:
        WIN.blit(FIGHT_BTN_DISABLED, fight_rect)
    
    if heal_enabled:
        WIN.blit(HEAL_BTN, heal_rect)
    else:
        WIN.blit(HEAL_BTN_DISABLED, heal_rect)

    if pickup_enabled:
        WIN.blit(PICKUP_BTN, pickup_rect)
    else:
        WIN.blit(PICKUP_BTN_DISABLED, pickup_rect)
    
    # --- Disegna pulsanti Indietro e Fuggi ---
    back_rect = BACK.get_rect(bottomleft=(30, HEIGHT - 30))
    if back_rect.collidepoint(mouse_pos):
        WIN.blit(BACK_HOVER, back_rect.topleft)
    else:
        WIN.blit(BACK, back_rect.topleft)
        
    escape_rect = ESCAPE.get_rect(bottomright=(WIDTH - 30, HEIGHT - 30))
    fuga_possibile = (len(mazzo) >= 4 and not player_interacted_this_turn and not fuga_usata_nel_turno_precedente)
    if fuga_possibile:
        if escape_rect.collidepoint(mouse_pos):
            WIN.blit(ESCAPE_HOVER, escape_rect.topleft)
        else:
            WIN.blit(ESCAPE, escape_rect.topleft)
    else:
        WIN.blit(ESCAPE_DISABLED, escape_rect.topleft)

    pygame.display.update()
    
    # Restituisce tutti i rect cliccabili
    return back_rect, escape_rect, fight_rect, heal_rect, pickup_rect, mouse_pos

def draw_options_window():
    """
    Disegna la schermata delle opzioni con il tasto indietro (hover).
    Restituisce il rect del tasto indietro e la posizione del mouse.
    """
    WIN.blit(OPTIONS_BG, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    back_rect = BACK.get_rect(bottomleft=(30, HEIGHT - 30))
    if back_rect.collidepoint(mouse_pos):
        WIN.blit(BACK_HOVER, back_rect.topleft)
    else:
        WIN.blit(BACK, back_rect.topleft)
    pygame.display.update()
    return back_rect, mouse_pos

def draw_mazzo_pila():
    """
    Disegna la pila del mazzo: le carte sono sovrapposte sopra DISCARD_POS,
    con offset negativo (verso l'alto) e meno pixel di differenza.
    """
    offset = -1 # o il valore che preferisci
    num = len(mazzo)
    base_x, base_y = DECK_POS
    for i in range(num):
        pos = (base_x, base_y + offset * i)
        back_card = deck.get("back", pos)
        WIN.blit(back_card.image, back_card.rect.topleft)

def draw_scarti_pila():
    """
    Disegna la pila degli scarti solo se ci sono carte. 
    L'ultima carta scartata (top della pila) va disegnata per ultima, in cima.
    """
    if not scarti:
        return  # Non disegna nulla se la pila è vuota

    offset = -1
    base_x, base_y = DISCARD_POS

    for i, card_name in enumerate(scarti):
        pos = (base_x, base_y + offset * i)
        card = deck.get(card_name, pos)
        if card:
            WIN.blit(card.image, card.rect.topleft)

def funzione_fuggi():
    """
    Mette le 4 carte in gioco in fondo al mazzo, le mischia,
    e poi pesca 4 nuove carte. Aggiorna le variabili di stato della fuga.
    """
    global mazzo, nomi_pescati, carte_pescate, deck, fuga_usata_nel_turno_precedente, player_interacted_this_turn
    
    print("Fuga! Le carte in gioco tornano nel mazzo.")

    carte_da_spostare = list(nomi_pescati)
    random.shuffle(carte_da_spostare)
    mazzo.extend(carte_da_spostare)
    
    pesca_4_carte(deck)
    
    fuga_usata_nel_turno_precedente = True
    player_interacted_this_turn = False

# Funzione per gestire la logica di una carta selezionata    
def gioca_carta(card_to_play):
    """
    Sposta una carta dalla mano (carte_pescate) alla pila degli scarti.
    Questa funzione non gestisce più lo stato del gioco (selezione, turni).
    """
    global scarti, nomi_pescati, carte_pescate

    print(f"AZIONE COMPLETATA con la carta: {card_to_play.name}")

    # Aggiungi la carta agli scarti
    scarti.append(card_to_play.name)

    # Rimuovi la carta dalla mano del giocatore
    # Questo può causare un errore se la carta non è presente, quindi è un buon punto di controllo
    if card_to_play in carte_pescate:
        carte_pescate.remove(card_to_play)
        nomi_pescati.remove(card_to_play.name)
    else:
        print(f"ERRORE: Si è tentato di giocare la carta {card_to_play.name} ma non era in mano.")
 
def draw_winning_window():
    WIN.blit(WINNING_BG, (0, 0))
    WIN.blit(VICTORY, (WIDTH // 2 - VICTORY.get_width() // 2, HEIGHT // 2 - VICTORY.get_height() // 2 - 220))
    
    mouse_pos = pygame.mouse.get_pos()
    
    new_game_rect = NEW_GAME.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    back_rect = BACK.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
    
    if new_game_rect.collidepoint(mouse_pos):
        WIN.blit(NEW_GAME_HOVER, new_game_rect.topleft)
    else:
        WIN.blit(NEW_GAME, new_game_rect.topleft)
        
    if back_rect.collidepoint(mouse_pos):
        WIN.blit(BACK_HOVER, back_rect.topleft)
    else:
        WIN.blit(BACK, back_rect.topleft)
    pygame.display.update()
    
    return new_game_rect, back_rect, mouse_pos

def start_new_game():
    """
    Resetta tutte le variabili di gioco per iniziare una nuova partita.
    """
    global mazzo, carte_pescate, nomi_pescati, scarti, deck
    global selected_card, player_interacted_this_turn, fuga_usata_nel_turno_precedente
    
    scarti = []
    selected_card = None
    player_interacted_this_turn = False
    fuga_usata_nel_turno_precedente = False
    
    mazzo = [k for k in deck.cards.keys() if k != "back" and not (
        ("hearts" in k or "diamonds" in k) and 
        (k.startswith("J_") or k.startswith("Q_") or k.startswith("K_") or k.startswith("A_"))
    )]
    random.shuffle(mazzo)
    carte_pescate, nomi_pescati = pesca_4_carte(deck)
    print("Nuova partita iniziata!")
    
# =========================
# MAIN LOOP E LOGICA DI GIOCO
# =========================

def main():
    global player_interacted_this_turn, fuga_usata_nel_turno_precedente
    global mazzo, carte_pescate, nomi_pescati, scarti, deck # Aggiunte per chiarezza
    
    menu = True
    game = False
    options = False
    victory = False

    selected_card = None
    player_interacted_this_turn = False
    fuga_usata_nel_turno_precedente = False

    clock = pygame.time.Clock()
    run = True
    mouse_released = True
    fade_sprite = None
    fade_group = pygame.sprite.Group()

    while run:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True

        if menu:
            new_game_rect, option_rect, exit_rect, mouse_pos = draw_starting_window()
        elif game:
            back_rect, escape_rect, fight_rect, heal_rect, pickup_rect, mouse_pos = draw_game_window(selected_card)
        elif options:
            back_rect, mouse_pos = draw_options_window()
        elif victory:
            new_game_rect, back_rect, mouse_pos = draw_winning_window()

        if fade_sprite is None:
            if menu:
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if new_game_rect.collidepoint(mouse_pos):
                        start_new_game()
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "game"
                        mouse_released = False
                        random.shuffle(mazzo)
                        carte_pescate, nomi_pescati = pesca_4_carte(deck)
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "game"
                        mouse_released = False
                    elif option_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "options"
                        mouse_released = False
                    elif exit_rect.collidepoint(mouse_pos):
                        run = False
                        mouse_released = False

            elif game:
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    clicked_on_button = False

                    # --- Logica di gestione dell'azione ---
                    if fight_rect.collidepoint(mouse_pos):
                        if selected_card and ("spades" in selected_card.name or "clubs" in selected_card.name):
                            player_interacted_this_turn = True
                            gioca_carta(selected_card)
                            selected_card = None
                            clicked_on_button = True
                    
                    elif heal_rect.collidepoint(mouse_pos):
                        if selected_card and "hearts" in selected_card.name:
                            player_interacted_this_turn = True
                            gioca_carta(selected_card)
                            selected_card = None
                            clicked_on_button = True
                            
                    elif pickup_rect.collidepoint(mouse_pos):
                        if selected_card and "diamonds" in selected_card.name:
                            player_interacted_this_turn = True
                            gioca_carta(selected_card)
                            selected_card = None
                            clicked_on_button = True

                    # Se un'azione è stata eseguita, controlla se bisogna pescare
                    if clicked_on_button:
                        # 1. Controlla la condizione di vittoria (caso finale)
                        if len(mazzo) == 0 and len(carte_pescate) == 0:
                            print("VITTORIA! Mazzo e mano vuoti.")
                            
                            fade_sprite = FadeOutTransition()
                            fade_group.add(fade_sprite)
                                                        
                            next_state = "victory"
                        
                        # 2. Altrimenti, controlla se bisogna pescare (solo se è rimasta 1 carta in mano)
                        elif len(carte_pescate) == 1:
                            # 2a. CASO SPECIFICO: Ci sono carte nel mazzo, ma meno di 3.
                            if len(mazzo) > 0 and len(mazzo) < 3:
                                print(f"Mazzo quasi finito! Pesco le ultime {len(mazzo)} carte.")
                                pesca_rimanenti_carte()
                                
                            # 2b. CASO GENERALE: Ci sono abbastanza carte per una pesca normale.
                            elif len(mazzo) >= 3:
                                print("Pesca di 3 nuove carte.")
                                pesca_tre_nuove_carte()
                                
                            # Se len(mazzo) è 0, non succede nulla. Il giocatore giocherà l'ultima carta
                            # e al prossimo click si attiverà la condizione di vittoria.
                        
                        mouse_released = False
                    
                    # Gestione degli altri pulsanti e selezione carte
                    elif back_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "menu"
                        mouse_released = False
                    
                    elif escape_rect.collidepoint(mouse_pos):
                        fuga_possibile = (len(mazzo) >= 4 and not player_interacted_this_turn and not fuga_usata_nel_turno_precedente)
                        if fuga_possibile:
                            funzione_fuggi()
                            selected_card = None
                        else:
                            print("Fuga non permessa in questo momento.")
                        mouse_released = False
                    
                    else: # Logica di selezione carta (se non si è cliccato su nessun pulsante)
                        clicked_on_a_card = False
                        for card in carte_pescate:
                            if card.rect.collidepoint(mouse_pos):
                                if card == selected_card:
                                    selected_card = None
                                else:
                                    selected_card = card
                                clicked_on_a_card = True
                                break
                        if not clicked_on_a_card:
                            selected_card = None
                        mouse_released = False
            elif victory:
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if new_game_rect.collidepoint(mouse_pos):
                        start_new_game()
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "game"
                        mouse_released = False
                    elif back_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "menu"
                        mouse_released = False                
            
            elif options: 
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if back_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "menu"
                        mouse_released = False

        if fade_sprite is not None:
            fade_group.update(dt)
            fade_group.draw(WIN)
            pygame.display.update()
            if not fade_sprite.is_transitioning():
                if isinstance(fade_sprite, FadeOutTransition):
                    # Resetta tutti gli stati a False
                    menu, game, options, victory = False, False, False, False
                    # Imposta a True solo lo stato di destinazione
                    if next_state == "menu":
                        menu = True
                    elif next_state == "game":
                        game = True
                    elif next_state == "options":
                        options = True
                    elif next_state == "victory":
                        victory = True
                    
                    fade_sprite = FadeInTransition()
                    fade_group.empty()
                    fade_group.add(fade_sprite)
                elif isinstance(fade_sprite, FadeInTransition):
                    fade_group.empty()
                    fade_sprite = None

    pygame.quit()

# =========================
# AVVIO DEL GIOCO
# =========================

if __name__ == "__main__":
    mazzo = [k for k in deck.cards.keys() if k != "back" and not (("hearts" in k or "diamonds" in k) and (k.startswith("J_") or k.startswith("Q_") or k.startswith("K_") or k.startswith("A_")))]
    random.shuffle(mazzo)
    scarti = []
    main()