import pygame as pygame
import time

class Anim:
    def __init__(self, uni):
        self.uni   = uni
        self.running = True
        self.setup = uni.setup_dict['anim']
        self.w, self.h = self.uni.dims
        
    def run(self):
        """ A coroutine that wait till it is given a list of boids, then places them on the screen and yields back to the main sim """
        pygame.init()
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode( (self.w, self.h) )
        pygame.display.set_caption('Boids')

        # handel the vizual setup for the boids
        for boid in (yield):
            x,y = boid.pos[0]
            boid.radius = self.setup['boid']['rad']
            boid.pyg_rect   = pygame.Rect(x-boid.radius, y-boid.radius, boid.radius, boid.radius)
            colour          = self.setup['boid']['color']() 
            boid.pyg_colour = colour if (colour != self.setup['screen']['bg']).all() else tuple((i*2+3)%256 for i in colour)

        updates = 0
        while True:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    pygame.quit()
            if not self.running:
                break

            

            # ANIM ----------------------
            screen.fill(self.setup['screen']['bg'])
            boids, tree = (yield)

            # Tree
            if self.setup['tree']['anim_tree']:
                self.draw_Tree(
                                tree.tree, 
                                screen, 
                                self.setup['tree']['colour'], 
                                self.setup['tree']['thickness']
                              )

            # Update Boids
            for boid in boids:
                x,y = boid.pos[0]
                boid.pyg_rect.x = x
                boid.pyg_rect.y = y
                pygame.draw.ellipse(screen, boid.pyg_colour, boid.pyg_rect)


            # LOOP END -------------- ### TODO add update/tick count to canvas
            print(f"{updates=}")            
            updates += 1
            pygame.display.flip()
            clock.tick(self.setup['tick'])
        return 'PYGAME-CLOSED'
    
    def draw_Tree(self, tree, screen, colour, thickness):
        """ recursively draw the Qtree, for debugging mostly """
        cx,cy = tree.rect.cx, tree.rect.cy
        h, w  = tree.rect.h,  tree.rect.w

        rect = pygame.Rect(cx-w/2, cy-h/2, w, h)
        pygame.draw.rect(screen, 
                         colour, 
                         rect, 
                         thickness
                        )
        if tree.devided:
            self.draw_Tree(tree.quad_NE, screen, colour, thickness)
            self.draw_Tree(tree.quad_SE, screen, colour, thickness)
            self.draw_Tree(tree.quad_SW, screen, colour, thickness)
            self.draw_Tree(tree.quad_NW, screen, colour, thickness)




if __name__ == "__main__":
    # call the simulation from main
    from Main import Universe
    uni = Universe()
    uni.start()