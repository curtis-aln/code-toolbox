import pygame as pg

# initilising pygame
pg.init()

# screen settings
screen_width  = 1000
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
window_title = "Simulation"

# framerate
clock = pg.time.Clock()
FPS = 144

# settings
screen_color = (0, 0, 0)

# main game loop
paused = False

while True:
    # preparing the frame
    clock.tick(FPS)
    screen.fill(screen_color)

    # event check
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()
            
            elif event.key == pg.K_SPACE:
                paused = not paused
    

    # simulation logic

    
    # rendering


    # ending frame
    pg.display.update()
    pg.display.set_caption(f"{window_title} | fps: {round(clock.get_fps())} / {FPS}")