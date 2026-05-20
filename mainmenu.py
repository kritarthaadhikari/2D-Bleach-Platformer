import pygame
import setup as st
menu=pygame.transform.scale(pygame.image.load('images/setup/mainmenu.jpg'),(1280,720)).convert()

def draw():
    st.win.blit(menu,(0,0))
    playquit_text= pygame.transform.scale(pygame.image.load('images/setup/playquit.png').convert_alpha(), (400, 225))
    st.win.blit(playquit_text,(st.screen_width//2-200, st.screen_height//2+150))
    play_rect=pygame.Rect(st.screen_width//2-110, st.screen_height//2+203, 230, 60)
    quit_rect = pygame.Rect(st.screen_width//2-110, st.screen_height//2+280, 230, 60)
    pygame.display.update()
    return play_rect,quit_rect

def handleMenu():
    play_rect, quit_rect = draw()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()

        if event.type==pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                st.game_state="start"
            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                quit()

