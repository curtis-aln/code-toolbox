import pygame as pg
from pygame import Vector2


# initilising pygame
pg.init()


class Simulation:
    SCREEN_BOUNDS = Vector2(1000, 600)
    SCREEN_COLOR  = (20, 20, 20)
    FPS = 144
    WINDOW_TITLE = 'Proton Electron Simulation'

    def __init__(self) -> None:
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(Simulation.SCREEN_BOUNDS)

        self.paused = False
        self.running = True
    

    def event_check(self):
        # event check
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                
                elif event.key == pg.K_SPACE:
                    self.paused = not self.paused
    

    def run(self):
        while self.running:
            self.prep_frame()
            self.process_frame()
            self.end_frame()
    

    def prep_frame(self):
        self.clock.tick(Simulation.FPS)
        self.event_check()

    def process_frame(self):
        pass

    def end_frame(self):
        pg.display.update()
        pg.display.set_caption(f"{Simulation.WINDOW_TITLE} | fps: {round(self.clock.get_fps())} / {Simulation.FPS}")


if __name__ == "__main__":
    Simulation().run()
