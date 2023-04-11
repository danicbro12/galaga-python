import pygame


class SpriteSheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
            self.sheet.set_colorkey(-1, pygame.RLEACCEL)
        except pygame.error as e:
            print(f"Не вдалося завантажити зображення спрайту: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
