import pygame
import os
import random
from config import *
from logic.tank import Tank
from logic.enemy import AnimatedEnemyHelicopter
from logic.boom import Boom
from logic.hotBalloon import AnimatedHotBalloon


class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # אתחול מודול הסאונד
        pygame.mixer.init()

        # טען צליל ירי
        shoot_sound_path = os.path.join("assets", "sounds", "shoot.mp3")
        self.shoot_sound = pygame.mixer.Sound(shoot_sound_path)
        self.shoot_sound.set_volume(0.3)

        # טען והשמע את צליל הליקופטר בלולאה
        helicopter_sound_path = os.path.join("assets", "sounds", "helicopter.wav")
        self.helicopter_sound = pygame.mixer.Sound(helicopter_sound_path)
        self.helicopter_sound.set_volume(0.3)
        self.helicopter_sound.play(loops=-1)

        # טען את תמונות הטנק והכדור
        tank_img_path = os.path.join("assets", "images", "tank_blue.png")
        bullet_img_path = os.path.join("assets", "images", "bullet.png")
        self.tank_image = pygame.image.load(tank_img_path).convert_alpha()
        self.tank_image = pygame.transform.scale(self.tank_image, (60, 60))
        self.bullet_image = pygame.image.load(bullet_img_path).convert_alpha()
        self.bullet_image = pygame.transform.scale(self.bullet_image, (10, 20))

        # צור את הטנק
        self.tank = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 24, self.tank_image)

        # טען פריימים של הליקופטר
        self.helicopter_frames = []
        for i in range(1, 4):
            path = f"assets/images/helicopter/helicopter{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (80, 50))
            self.helicopter_frames.append(frame)

        # הגדרות עבור אויבים
        self.enemies = []
        self.spawn_timer = 0

        # טען את פריימי הפיצוץ (Boom)
        self.boom_frames = []
        for i in [1, 3, 4, 5]:
            path = f"assets/images/boom/boom{i}.png"
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (80, 80))
            self.boom_frames.append(img)

        self.booms = []

        # טען סאונד פיצוץ
        explosion_sound_path = os.path.join("assets", "sounds", "explosion.mp3")
        self.explosion_sound = pygame.mixer.Sound(explosion_sound_path)
        self.explosion_sound.set_volume(1.0)

        # טען פריימים של כדור פורח
        self.balloon_frames = []
        for i in range(1, 5):
            path = f"assets/images/hotBalloon/hotBalloon{i}.png"
            frame = pygame.image.load(path).convert_alpha()
            frame = pygame.transform.scale(frame, (60, 80))
            self.balloon_frames.append(frame)

        self.balloons = []
        self.balloon_timer = 0

        self.lives = 3
        heart_path = os.path.join("assets", "images", "ui", "heart", "heart.png")
        self.heart_image = pygame.image.load(heart_path).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (60, 60))

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 28)

        self.highscore = 0
        try:
            with open("data/highScore.txt", "r") as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0

        self.new_highscore = False

        # טען פריימים של אנימציית New Record
        self.new_record_frames = []
        for i in range(1, 6):
            path = f"assets/images/newRecord/newRecord{i}.png"
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (250, 100))  # אפשר לשנות לפי הצורך
            self.new_record_frames.append(img)

        self.new_record_index = 0
        self.new_record_counter = 0
        self.new_record_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.tank.shoot(self.bullet_image)
                    self.shoot_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()
        self.tank.handle_input(keys)
        self.tank.update()

        self.spawn_timer += 1
        if self.spawn_timer >= 90:
            y = random.randint(0, SCREEN_HEIGHT - 50)
            heli = AnimatedEnemyHelicopter(SCREEN_WIDTH + 60, y, self.helicopter_frames)
            self.enemies.append(heli)
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()

        self.enemies = [e for e in self.enemies if e.rect.right > 0]

        for bullet in self.tank.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.tank.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.explosion_sound.play()
                    boom = Boom(enemy.rect.centerx, enemy.rect.centery, self.boom_frames)
                    self.booms.append(boom)
                    self.score += 1
                    break

        for bullet in self.tank.bullets[:]:
            for balloon in self.balloons[:]:
                if bullet.rect.colliderect(balloon.rect):
                    self.tank.bullets.remove(bullet)
                    self.balloons.remove(balloon)
                    self.lives -= 1
                    break

        for boom in self.booms:
            boom.update()
        self.booms = [b for b in self.booms if not b.done]

        self.balloon_timer += 1
        if self.balloon_timer >= 150:
            x = random.randint(0, SCREEN_WIDTH - 60)
            balloon = AnimatedHotBalloon(x, -80, self.balloon_frames)
            self.balloons.append(balloon)
            self.balloon_timer = 0

        for balloon in self.balloons:
            balloon.update()

        self.balloons = [b for b in self.balloons if b.rect.top < SCREEN_HEIGHT]

        if self.lives <= 0:
            self.running = False

        if self.score > self.highscore:
            self.highscore = self.score
            self.new_record_active = True
            self.new_record_counter = 0
            self.new_record_index = 0
            with open("data/highScore.txt", "w") as f:
                f.write(str(self.score))

    def draw(self):
        self.screen.fill(WHITE)
        self.tank.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for boom in self.booms:
            boom.draw(self.screen)

        for balloon in self.balloons:
            balloon.draw(self.screen)

        for i in range(self.lives):
            x = 10 + i * 35
            self.screen.blit(self.heart_image, (x, 10))

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        highscore_text = self.font.render(f"High Score: {self.highscore}", True, (100, 0, 0))
        self.screen.blit(highscore_text, (SCREEN_WIDTH - 200, 40))

        if self.new_record_active:
            frame = self.new_record_frames[self.new_record_index]
            x = SCREEN_WIDTH // 2 - frame.get_width() // 2
            y = SCREEN_HEIGHT // 2 - frame.get_height() // 2
            self.screen.blit(frame, (x, y))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

            if self.score > self.highscore:
                with open("data/highScore.txt", "w") as f:
                    f.write(str(self.score))

        if self.score > self.highscore:
            self.new_record_active = True  # ← הפעלת האנימציה
            with open("data/highScore.txt", "w") as f:
                f.write(str(self.score))

        self.helicopter_sound.stop()
