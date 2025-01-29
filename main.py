import pygame
from home import HomeScreen

pygame.init()
running = True
SIZE = WIDTH, HEIGHT = 1080, 710
pygame.display.set_caption("Puppyteer")

window = pygame.display.set_mode(SIZE)
home = HomeScreen(SIZE)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break

    home.loop(events)
    home.draw()
    window.blit(home, (0, 0))
    pygame.display.update()

pygame.quit()
