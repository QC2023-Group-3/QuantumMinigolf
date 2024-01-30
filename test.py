import pygame
pygame.init()
font=pygame.font.SysFont("Arial", 36)
white=(255,255,255)
screen = pygame.display.set_mode((400,400))
txt = font.render("Hello World", True, white)
txt_rect= txt.get_rect(center=(200,200))
done = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    screen.blit(txt,txt_rect)
    pygame.display.flip()