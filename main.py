import pygame
import os

# =========================
# COSTANTI E INIZIALIZZAZIONE
# =========================

WIDTH, HEIGHT = 1280, 896  # Dimensioni finestra
FPS = 60                   # Frame per secondo
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SCOUNDREL")

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

# Altri asset (esempio)
HEART = pygame.image.load(os.path.join("assets", "images", "ui", "heart.png"))
FIGHT_BTN = pygame.image.load(os.path.join("assets", "images", "ui", "fight_btn.png"))

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

def draw_game_window():
    """
    Disegna la schermata di gioco con il tasto indietro (hover).
    Restituisce il rect del tasto indietro e la posizione del mouse.
    """
    WIN.blit(GAME_BG, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
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

# =========================
# MAIN LOOP E LOGICA DI GIOCO
# =========================

def main():
    # Stati delle schermate
    menu = True
    game = False
    options = False

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
            back_rect, mouse_pos = draw_game_window()
        elif options:
            back_rect, mouse_pos = draw_options_window()

        # --- Gestione click sui pulsanti ---
        if fade_sprite is None:  # Solo se non c'è una transizione in corso
            if menu:
                if pygame.mouse.get_pressed()[0] and mouse_released:
                    if new_game_rect.collidepoint(mouse_pos):
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

if __name__ == "__main__":
    main()