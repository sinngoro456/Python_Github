import pygame
import math


class Car:
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 0), [0, 0, 40, 20])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05

    def update(self, keys, width, height):
        # キー入力の処理
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            self.speed *= 0.95  # 摩擦

        if keys[pygame.K_LEFT]:
            self.angle += 2
        if keys[pygame.K_RIGHT]:
            self.angle -= 2

        # 車の移動
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))

        # 画面の端での跳ね返り
        if self.rect.left < 0 or self.rect.right > width:
            self.speed = -self.speed / 2
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed = -self.speed / 2

    def draw(self, screen):
        rotated_car = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_car.get_rect(center=self.rect.center)
        screen.blit(rotated_car, new_rect.topleft)

    def get_velocity(self):
        return self.speed


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("簡単なカーシミュレーター")
        self.clock = pygame.time.Clock()
        self.car = Car(self.WIDTH // 2, self.HEIGHT // 2)
        self.running = True
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.car.update(keys, self.WIDTH, self.HEIGHT)

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.car.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

            # 速度の表示（デバッグ用）
            print(f"Velocity: {self.car.get_velocity()}")

        pygame.quit()

    def draw_speedometer(self):
        speed = abs(self.car.get_velocity())  # 速度の絶対値を取得
        speed_text = self.font.render(f"Speed: {speed:.2f}", True, (0, 0, 0))
        self.screen.blit(speed_text, (10, 10))  # 左上に表示

        # スピードメーターの円弧を描画
        center = (100, 100)
        radius = 50
        start_angle = 0
        end_angle = start_angle + (math.pi * speed / self.car.max_speed)
        pygame.draw.arc(
            self.screen,
            (255, 0, 0),
            (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
            start_angle,
            end_angle,
            5,
        )

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.car.draw(self.screen)
        self.draw_speedometer()  # スピードメーターを描画
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
