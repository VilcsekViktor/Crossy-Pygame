

# Pygame library importálása
import pygame

#Képernyő méret
SCREEN_TITLE = 'Crossy Viktor'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
# Színek RBG kódokkal
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Órajel meghatározása, ami alapján az eventek frissülnek
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    # FPS meghatározása
    TICK_RATE = 60

    # Játék osztály
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Hozzon létre egy új ablakot fehér háttérrel adott méretben
        self.game_screen = pygame.display.set_mode((width, height))
        # Állítsa a háttér színét fehérre
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        # Töltse be a háttérképet
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 375, 700, 50, 100)
        enemy_0 = NonPlayerCharacter('enemy.png', 20, 600, 50, 50)
        # Ellenség gyorsítása, ha szintet lépünk
        enemy_0.SPEED *= level_speed

        # Új ellenség létrehozása
        enemy_1 = NonPlayerCharacter('enemy.png', self.width - 40, 250, 50, 50)
        enemy_1.SPEED *= level_speed

        # Új ellenség létrehozása
        enemy_2 = NonPlayerCharacter('enemy.png', 20, 200, 100, 50)
        enemy_2.SPEED *= level_speed

        treasure = GameObject('treasure.png', 375, 50, 50, 50)

        # Maga a játék ciklus
        # Addig fut ameddig is_game_over == True parancs be nem következik
        while not is_game_over:

            # Egy ciklus ami elindítja az event-eket
            for event in pygame.event.get():
                # Ha kilépés típusú event indul zárja be a játékot
                if event.type == pygame.QUIT:
                    is_game_over = True
                # Érzékelje ha lenyomjuk a gombot
                elif event.type == pygame.KEYDOWN:
                    # Mozgás a felfele nyílra
                    if event.key == pygame.K_UP:
                        direction = 1
                    # Mozgás a lefele nyílra
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                # Érzékelje ha felengedjük a gombot
                elif event.type == pygame.KEYUP:
                    # Mozgás megállítása ha a gombot felengedjük
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
                print(event)

            # Képernyő kitöltése fehér háttérrel
            self.game_screen.fill(WHITE_COLOR)
            # Játékos rajzolása a háttérre
            self.game_screen.blit(self.image, (0, 0))

            # Kincs rajzolása
            treasure.draw(self.game_screen)
            
            # Játékos pozicíójának frissítése
            player_character.move(direction, self.height)
            # Játékos új pozíciójának rajzolása
            player_character.draw(self.game_screen)

            # Ellenség mozgása és rajzolása
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            # Ellenség mozgása és rajzolása, ha magasabb szintre jutunk
            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # Játék befejezése ha két karakter ütközik
            # Kilépés a ciklusból vesztés esetén
            # Ciklus újra indítása nyerés esetén
            if player_character.detect_collision(enemy_0):
                is_game_over = True
                did_win = False
                text = font.render('Vesztettél!', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('Nyertél!', True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # Frissítsen minden játék grafikát
            pygame.display.update()
            # Képernyő frissítése adott FPS-sel
            clock.tick(self.TICK_RATE)

        # Ha nyerünk játék ciklus újra indítása, gyorsabban
        # Ha vesztünk lépjen ki a ciklusból
        if did_win:
            self.run_game_loop(level_speed + 0.5)
        else:
            return

class GameObject:

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        # Kép méretezés
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    # Karakter elhelyezése a háttérképen
    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

# Osztály ami leírja a játékos karakter mozgását
class PlayerCharacter(GameObject):

    # Karakter sebessége
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Mozgás funkció
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        # Nem engedi hogy a játékos alul kimenjen a kijelzőről
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    # Ütközés érzékelés, ha két karakter egymáshoz ér
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True

# Osztály ami leírja az alternáló mozgást
class NonPlayerCharacter(GameObject):

    # Karakter sebessége
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Ha az ellenség eléri a kijező szélét forduljon vissza
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED
            
pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

# Lépjen ki a játékból és zárja be az ablakot
pygame.quit()
quit()


