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

DECK_POS = (150, 150) # Posizione del mazzo degli scarti
GAME_POS = [(350, 180), (495, 180), (640, 180), (785, 180)]  # Posizioni delle carte in gioco
DISCARD_POS = (985, 150)  # Posizione del mazzo degli scarti

pygame.display.set_caption("SCOUNDREL")

CARDS_LEFT = 44 # Numero di carte iniziali nel mazzo (escludendo il dorso e figure ed assi rossi)
LIFT_AMOUNT = 15 # Quanti pixel sollevare la carta selezionata
DARK_RED = (139, 0, 0) # Colore per l'highlight di selezione

pygame.font.init()  # Inizializzazione del modulo font di Pygame
FONT_PATH = os.path.join("assets", "fonts", "Jersey15-Regular.ttf")  # Cambia con il nome del tuo file
FONT = pygame.font.Font(FONT_PATH, 36)  # 36 è la dimensione del font

deck = CardDeck(os.path.join("assets", "images", "cards", "cards_tileMap.png"))  # Caricamento mazzo di carte

global carte_pescate, nomi_pescati, scarti
                        

# =========================
# CARICAMENTO ASSETS
# =========================

# Backgrounds
MENU_BG = pygame.image.load(os.path.join("assets", "images", "ui", "menu_bg_blur.png"))
GAME_BG = pygame.image.load(os.path.join("assets", "images", "ui", "game_bg_blur.png"))
OPTIONS_BG = pygame.image.load(os.path.join("assets", "images", "ui", "options_bg_blur.png"))

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

# Pulsante indietro (per gioco e opzioni)
BACK_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "back_btn.png"))
BACK = pygame.transform.scale(BACK_BTN, (160, 100))
BACK_BTN_HOVER = pygame.image.load(os.path.join("assets", "images", "ui", "back_btn_hover.png"))
BACK_HOVER = pygame.transform.scale(BACK_BTN_HOVER, (160, 100))

# Tavolo
TABLE_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "table.png"))

# Pergamena
SCROLL_IMG = pygame.image.load(os.path.join("assets", "images", "ui", "scroll_test_2.png"))

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

def draw_game_window(selected_card):
    """
    Disegna la schermata di gioco con il tasto indietro (hover).
    Mostra la pila dinamica del mazzo e degli scarti, e le 4 carte pescate.
    Restituisce il rect del tasto indietro e la posizione del mouse.
    """
    WIN.blit(GAME_BG, (0, 0))
    WIN.blit(TABLE_IMG, (0, HEIGHT / 5))
    WIN.blit(SCROLL_IMG, (0, 0))
    
    draw_mazzo_pila()  # Disegna la pila del mazzo
    draw_scarti_pila()  # Disegna la pila degli scarti

    # --- Mostra il numero di carte rimaste nel mazzo ---
    num_carte_rimaste = len(mazzo)
    text = FONT.render(f"Carte rimaste: {num_carte_rimaste}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    WIN.blit(text, text_rect)

    # --- Mostra le 4 carte pescate in GAME_POS ---
    mouse_pos = pygame.mouse.get_pos()
    for card in carte_pescate:
        draw_pos = card.rect.topleft
        is_selected = (card == selected_card)

        # Se la carta è selezionata, calcola la posizione sollevata e disegna il bordo lì
        if is_selected:
            # Calcola la posizione sollevata PRIMA di disegnare qualsiasi cosa
            lifted_pos = (card.rect.x, card.rect.y - LIFT_AMOUNT)
            # Crea un rettangolo per il bordo basato sulla NUOVA posizione
            border_rect = pygame.Rect(lifted_pos, (card.rect.width, card.rect.height)).inflate(8, 8)
            # Disegna il bordo rosso usando il rettangolo corretto
            pygame.draw.rect(WIN, DARK_RED, border_rect, border_radius=8, width=4)
            draw_pos = lifted_pos # Aggiorna la posizione di disegno per l'immagine
        # Altrimenti, se il mouse è sopra, disegna il bordo bianco di hover
        elif card.rect.collidepoint(mouse_pos):
            pygame.draw.rect(WIN, (255, 255, 255), card.rect.inflate(8, 8), border_radius=8, width=4)
        
        # Disegna la carta nella posizione calcolata (normale o sollevata)
        WIN.blit(card.image, draw_pos)


    # --- Tasto indietro ---
    back_rect = BACK.get_rect(bottomleft=(30, HEIGHT - 30))
    if back_rect.collidepoint(mouse_pos):
        WIN.blit(BACK_HOVER, back_rect.topleft)
    else:
        WIN.blit(BACK, back_rect.topleft)

    pygame.display.update()
    return back_rect, mouse_pos

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



# =========================
# MAIN LOOP E LOGICA DI GIOCO
# =========================

def main():
    # Stati delle schermate
    menu = True
    game = False
    options = False

    # AGGIUNTO: Variabile per tenere traccia della carta selezionata
    selected_card = None

    clock = pygame.time.Clock()
    run = True
    mouse_released = True  # Per evitare click "ereditati"
    fade_sprite = None     # Sprite per la transizione fade
    fade_group = pygame.sprite.Group()  # Gruppo per gestire la transizione

    while run:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_released = True

        # --- Disegna la schermata attuale ---
        if menu:
            new_game_rect, option_rect, exit_rect, mouse_pos = draw_starting_window()
        elif game:
            # MODIFICATO: Passa la carta selezionata alla funzione di disegno
            back_rect, mouse_pos = draw_game_window(selected_card)
        elif options:
            back_rect, mouse_pos = draw_options_window()

        # --- Gestione click sui pulsanti ---
        if fade_sprite is None:  # Solo se non c'è una transizione in corso
            if menu:
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if new_game_rect.collidepoint(mouse_pos):
                        global scarti 
                        scarti = [] # Resetta la pila degli scarti a ogni nuova partita
                        selected_card = None # Resetta la selezione
                        mazzo = [k for k in deck.cards.keys()
                                if k != "back" and not (
                                    ("hearts" in k or "diamonds" in k) and (k.startswith("J_") or k.startswith("Q_") or k.startswith("K_") or k.startswith("A_"))
                                )]
                        random.shuffle(mazzo)
                        carte_pescate, nomi_pescati = pesca_4_carte(deck)
                        # Avvia fade-out prima di cambiare schermata
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
                # NUOVA LOGICA DI SELEZIONE CARTA
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    # Prima, gestisce il click sul tasto indietro
                    if back_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "menu"
                        mouse_released = False
                    else:
                        clicked_on_a_card = False
                        # Controlla se il click è su una delle carte in gioco
                        for card in carte_pescate:
                            if card.rect.collidepoint(mouse_pos):
                                # Se la carta cliccata è già quella selezionata, la deseleziona
                                if card == selected_card:
                                    selected_card = None
                                # Altrimenti, seleziona la nuova carta
                                else:
                                    selected_card = card
                                clicked_on_a_card = True
                                break # Esce dal ciclo, ha trovato la carta cliccata
                        
                        # Se il click non è avvenuto su una carta, deseleziona qualunque carta
                        if not clicked_on_a_card:
                            selected_card = None

                        mouse_released = False


            else: 
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if back_rect.collidepoint(mouse_pos):
                        fade_sprite = FadeOutTransition()
                        fade_group.add(fade_sprite)
                        next_state = "menu"
                        mouse_released = False

        # --- Gestione transizione fade-out/fade-in ---
        if fade_sprite is not None:
            fade_group.update(dt)
            fade_group.draw(WIN)
            pygame.display.update()
            # Se la transizione è finita
            if not fade_sprite.is_transitioning():
                if isinstance(fade_sprite, FadeOutTransition):
                    # Cambio schermata e avvio fade-in
                    if next_state == "menu":
                        menu, game, options = True, False, False
                    elif next_state == "game":
                        menu, game, options = False, True, False
                    elif next_state == "options":
                        menu, game, options = False, False, True
                    fade_sprite = FadeInTransition()
                    fade_group.empty()
                    fade_group.add(fade_sprite)
                elif isinstance(fade_sprite, FadeInTransition):
                    # Quando il fade-in è finito, rimuovo la transizione
                    fade_group.empty()
                    fade_sprite = None

    pygame.quit()

# =========================
# AVVIO DEL GIOCO
# =========================

scarti = [] 

if __name__ == "__main__":
    mazzo = [k for k in deck.cards.keys()
             if k != "back" and not (
                 ("hearts" in k or "diamonds" in k) and (k.startswith("J_") or k.startswith("Q_") or k.startswith("K_") or k.startswith("A_"))
             )]
    random.shuffle(mazzo)
    scarti = []
    main()