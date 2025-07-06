import pygame

CARD_WIDTH = 42
CARD_HEIGHT = 60

class Card(pygame.sprite.Sprite):
    def __init__(self, image, name, value, pos=(0, 0)):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name
        self.value = value
        self.suit = name.split("_of_")[1]
        self.rank = name.split("_of_")[0]

    def update(self, *args):
        pass


def round_card_corners(card_image):
        mask = pygame.Surface((42, 60), pygame.SRCALPHA)
        mask.fill((255, 255, 255, 255))  # tutto opaco

        # Angoli trasparenti
        for x, y in [(0, 0), (41, 0), (0, 59), (41, 59)]:
            mask.set_at((x, y), (0, 0, 0, 0))  # trasparente

        card_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return card_image

class CardDeck:
    def __init__(self, sprite_path):
        self.sheet = pygame.image.load(sprite_path).convert_alpha()
        self.cards = {}
        self._load_cards()

    def _load_cards(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        values = {'A': 14, 'J': 11, 'Q': 12, 'K': 13}
        for i in range(2, 11):
            values[str(i)] = i

        for row, suit in enumerate(suits):
            for col, rank in enumerate(ranks):
                name = f"{rank}_of_{suit}"
                value = values[rank]
                self.cards[name] = self._make_card(col, row, name, value)
    
    def _make_card(self, col, row, name, value):
        x = col * CARD_WIDTH
        y = row * CARD_HEIGHT
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        image = self.sheet.subsurface(rect).copy()
        image = round_card_corners(image)
        
        return Card(image, name, value)

    def get(self, name, pos=(0, 0)):
        base_card = self.cards.get(name)
        if base_card:
            return Card(base_card.image.copy(), base_card.name, base_card.value, pos)
        return None

    def all_cards(self):
        return list(self.cards.values())
