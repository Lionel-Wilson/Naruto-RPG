import pygame as pg
import os

pg.init()


class Screen:
    def __init__(self, path, caption):
        # set the name of the screen
        pg.display.set_caption(caption)
        self.pic = pg.image.load(path)
        self.screen_width = self.pic.get_rect()[2]
        self.screen_height = self.pic.get_rect()[3]

    def make_screen(self):
        return pg.display.set_mode((self.screen_width, self.screen_height))

    def choose_Background(self):
        return self.pic


# draw the screen and the backgroud of the game:
init_screen = Screen('tree.png', 'Pirates')
# set the screen width and height
screen_width, screen_height = init_screen.screen_width, init_screen.screen_height
screen = init_screen.make_screen()
Backgroud_picture = init_screen.choose_Background()
# the border
BORDER = 10
# Ground border
Ground_edge = 20
fg_color = pg.Color("blue")
platform_color = pg.Color((209, 162, 8))

# actor attributes
actor_width = 50
actor_height = 100
controller_actor1 = pg.Rect(
    BORDER, screen_height - Ground_edge - actor_height, actor_width, actor_height)
controller_actor2 = pg.Rect(
    screen_width-BORDER-actor_width, screen_height - Ground_edge - actor_height, actor_width, actor_height)


class Actor:
    def __init__(self, actor_width, actor_height, stand_images, walk_left_images, walk_right_images,  left_key, right_key, jump_key, controller, stay_frames=3, walk_frames=4, vel=10, vy=-15, standCount=0, walk_count=0, jump=False):
        self.actor_width = actor_width
        self.actor_height = actor_height
        self.actor = 'the picture of every frame'
        self.stand_images = stand_images
        self.walk_left_images = walk_left_images
        self.walk_right_images = walk_right_images
        # load all images for this actor
        self.load_images()
        self.stay_frames = stay_frames
        self.walk_frames = walk_frames
        self.stand = 1
        self.walk_left = 0
        self.walk_right = 0
        self.pic_rate_control = len(self.stand_images) * self.stay_frames
        self.pic_rate_control_left_walk = len(
            self.walk_left_images) * self.walk_frames
        self.pic_rate_control_right_walk = len(
            self.walk_right_images) * self.walk_frames

        self.left_key = left_key
        self.right_key = right_key
        self.controller = controller
        self.vel = vel
        self.standCount = standCount
        self.walk_count = walk_count
        self.jump = jump
        self.up = jump_key
        self.g = 0.65  # the rate to fall
        self.vy = vy
        self.vel_y = vy

    def actor_scale(self, path):
        return pg.transform.scale(pg.image.load(path), (self.actor_width, self.actor_height))

    def images_list(self, path):
        images = os.listdir(path)
        image_list = []
        for i in images:
            image_list += [path+i]
        return image_list

    def load_images(self):
        self.stand_images = self.images_list(self.stand_images)
        self.walk_left_images = self.images_list(self.walk_left_images)
        self.walk_right_images = self.images_list(self.walk_right_images)

    def walk(self):
        self.keys = pg.key.get_pressed()

        if self.keys[self.left_key] and self.controller.x > BORDER:
            self.controller.x -= self.vel
            self.stand = False
            self.walk_left = True
            self.walk_right = False

        elif self.keys[self.right_key] and self.controller.x+actor_width+self.vel < screen_width-BORDER:
            self.controller.x += self.vel
            self.stand = False
            self.walk_left = False
            self.walk_right = True
        else:
            self.stand = True
            self.walk_left = False
            self.walk_right = False
            self.walk_count = 0

        if self.stand:
            if self.standCount < self.pic_rate_control:
                self.actor = self.actor_scale(
                    self.stand_images[self.standCount//self.stay_frames])
                self.standCount += 1
            else:
                self.standCount = 0
        if self.walk_left:
            if self.walk_count < self.pic_rate_control_left_walk:
                self.actor = self.actor_scale(
                    self.walk_left_images[self.walk_count//self.walk_frames])
                self.walk_count += 1
            else:
                self.walk_count = 0
        if self.walk_right:
            if self.walk_count < self.pic_rate_control_right_walk:
                self.actor = self.actor_scale(
                    self.walk_right_images[self.walk_count // self.walk_frames])
                self.walk_count += 1
            else:
                self.walk_count = 0

    def Jump(self):
        self.keys = pg.key.get_pressed()
        if not self.jump:  # 这里参考了https://www.youtube.com/watch?v=2-DNswzCkqk
            if self.keys[self.up]:
                self.jump = True
        else:
            if self.vel_y <= abs(self.vy):
                self.vel_y += self.g
                self.controller.y += self.vel_y
            else:
                self.controller.y = screen_height - Ground_edge - actor_height
                self.vel_y = self.vy
                self.jump = False


# Create actor1
actor1 = Actor(actor_width, actor_height, 'skeleton/stand/',
               'skeleton/WalkingLeft/', 'skeleton/WalkingRight/', pg.K_a, pg.K_d, pg.K_w, controller_actor1)
actor2 = Actor(actor_width, actor_height,  'Hero/Stand/', 'Hero/WalkingLeft/',
               'Hero/WalkingRight/', pg.K_LEFT, pg.K_RIGHT, pg.K_UP, controller_actor2)
# the FPS of this game
FPS = 60
clock = pg.time.Clock()


class Pf():

    def __init__(self, PFW=screen_width//5, PFH=10):
        self.PFW = PFW
        self.PFH = PFH

    def show(self, x, y):
        global screen
        global platform_color
        pg.draw.rect(screen, platform_color, pg.Rect(x, y, self.PFW, self.PFH))
        pg.draw.rect(screen, platform_color, pg.Rect(
            screen_width-x-self.PFW, y, self.PFW, self.PFH))


# 画那些边界矩形
edges = [pg.Rect(0, 0, screen_width, BORDER),
         pg.Rect(0, screen_height - Ground_edge, screen_width, Ground_edge),
         pg.Rect(0, 0, BORDER, screen_height),
         pg.Rect(screen_width - BORDER, 0, BORDER, screen_height)
         ]


def main():
    run = True

    while run:
        # draw the background
        screen.blit(Backgroud_picture, (0, 0))
        # drawing the edge of the border
        # Top side
        for i in edges:
            pg.draw.rect(screen, fg_color, i)

        # drawing the platforms(in pair to ensure the equity)

        Pf().show(screen_width//8, screen_height//6)  # The highest group
        Pf().show(BORDER, screen_height//3)  # second highest group
        # the board players stand on.
        Pf().show(screen_width//10, screen_height//2)
        Pf().show(screen_width//6, screen_height - screen_height//3)  # lowest board
        Pf().show(screen_width//2-screen_width//8, screen_height//3.5)  # middle board
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        actor1.walk()
        actor1.Jump()
        actor2.walk()
        actor2.Jump()
        screen.blit(actor1.actor, (controller_actor1.x, controller_actor1.y))
        screen.blit(actor2.actor, (controller_actor2.x, controller_actor2.y))

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
