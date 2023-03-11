import pygame
from random import randint
import time

WIDTH, HEIGHT = 800, 700
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Never Ending Game")

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY  = 128, 128, 128
RED = 255, 0, 0

FONT = pygame.font.SysFont("comicsans", 30)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.width = 15
        self.height = 30
        self.color = WHITE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def shot(self, y):
        pygame.draw.rect(window, RED, (self.x, y, 10, 10))


class Enemy:
    def __init__(self):
        self.x = randint(0, WIDTH - 10)
        self.y = 0
        self.width = 10
        self.height = 20
        self.color = WHITE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


def collison(player, enemy):
    if player.x + player.width > enemy.x and player.x < enemy.x + enemy.width:
        if player.y + player.height > enemy.y and player.y < enemy.y + enemy.height:
            return True

    return False


def endGame():
    text = FONT.render("Game Over", 1, WHITE)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


def enemyCollisionWithShot(enemy, y, player):
    if enemy.x + enemy.width > player.x and enemy.x < player.x + player.width:
        if y + 10 > enemy.y and y < enemy.y + enemy.height:
            return True

    return False


def displayTime(elapsedTime):
    text = FONT.render("Time: " + str(int(elapsedTime)), 1, WHITE)
    window.blit(text, (WIDTH - text.get_width() - 10, 50))

def displayEnemiesKilled(numOfEnemiesKilled):
    text = FONT.render("Enemies Killed: " + str(numOfEnemiesKilled), 1, WHITE)
    window.blit(text, (10, 50))


def main():
    clock = pygame.time.Clock()
    run = True
    start = time.time()
    startTime = time.time()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    velocity = 30
    spawnTime = 2000
    spawnCount = 0
    shot = False
    y = player.y
    numOfEnemiesKilled = 0

    while run:
        elapsedTime = time.time() - startTime

        if elapsedTime % 30 == 0:
            # Make a line of enemies
            for _ in range(12):
                enemies.append(Enemy())

        spawnCount += clock.tick(60)

        if spawnCount >= spawnTime:
            for _ in range(5):
                enemies.append(Enemy())

            spawnCount = 0
            spawnTime = max(200, spawnTime - 50)

        for enemy in enemies:
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

            if collison(player, enemy):
                endGame()
                run = False

        if time.time() - start > 1:
            for enemy in enemies:
                enemy.y += velocity
            start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x -= 10

                elif event.key == pygame.K_RIGHT:
                    player.x += 10

                if event.key == pygame.K_SPACE and not shot:
                    shot = True
                    y = player.y

        if y == 0 and shot:
            shot = False

        window.fill(BLACK)
        if shot:
            player.shot(y)
            y -= 5

        displayTime(elapsedTime)
        displayEnemiesKilled(numOfEnemiesKilled)
        player.draw(window)
        for enemy in enemies:
            if enemyCollisionWithShot(enemy, y, player):
                numOfEnemiesKilled += 1
                enemies.remove(enemy)

            enemy.draw(window)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
