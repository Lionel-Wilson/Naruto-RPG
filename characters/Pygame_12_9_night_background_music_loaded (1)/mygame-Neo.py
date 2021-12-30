import pygame as pg
import os

from pygame.display import update

pg.init()
pg.mixer.init()
pg.mixer.music.load('Blue Sky Athletics.mp3')


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
platform_list = []

# actor attributes
actor_width = 25
actor_height = 50
controller_actor1 = pg.Rect(
    BORDER, screen_height - Ground_edge - actor_height, actor_width, actor_height)
controller_actor2 = pg.Rect(
    screen_width-BORDER-actor_width, screen_height - Ground_edge - actor_height, actor_width, actor_height)


class Actor:
    def __init__(self, actor_width, actor_height, face_right_images, face_left_images, walk_left_images, walk_right_images, left_key, right_key, jump_key, controller, stay_frames=3, walk_frames=4, vel=10, vy=-15, standCount=0, walk_count=0, jump=False, face_reverse=False):
        self.actor_width = actor_width
        self.actor_height = actor_height
        self.actor = 'the picture of every frame'
        self.face_right_images = face_right_images
        self.face_left_images = face_left_images
        self.walk_left_images = walk_left_images
        self.walk_right_images = walk_right_images
        # load all images for this actor
        self.load_images()
        self.stay_frames = stay_frames
        self.walk_frames = walk_frames
        self.stand_face_right = True
        self.stand_face_left = False
        self.walk_left = False
        self.walk_right = False
        self.pic_rate_control_face_right = len(
            self.face_right_images) * self.stay_frames
        self.pic_rate_control_face_left = len(
            self.face_left_images) * self.stay_frames
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
        self.g = 0.7  # the rate to fall
        self.vy = vy
        self.vel_y = vy
        self.face_reverse = face_reverse

        self.upedge = screen_height - Ground_edge - actor_height

    def actor_scale(self, path):
        return pg.transform.scale(pg.image.load(path), (self.actor_width, self.actor_height))

    def images_list(self, path):
        images = os.listdir(path)
        image_list = []
        for i in images:
            image_list += [path+i]
        return image_list

    def load_images(self):
        self.face_right_images = self.images_list(self.face_right_images)
        self.face_left_images = self.images_list(self.face_left_images)
        self.walk_left_images = self.images_list(self.walk_left_images)
        self.walk_right_images = self.images_list(self.walk_right_images)

    def walk(self):
        self.keys = pg.key.get_pressed()
        if self.keys[self.left_key] and self.controller.x > BORDER:
            self.controller.x -= self.vel
            self.stand_face_right = False
            self.stand_face_left = False
            self.walk_left = True
            self.walk_right = False
            self.face_reverse = True

        elif self.keys[self.right_key] and self.controller.x+actor_width+self.vel < screen_width-BORDER:
            self.controller.x += self.vel
            self.stand_face_right = False
            self.stand_face_left = False
            self.walk_left = False
            self.walk_right = True
            self.face_reverse = False

        elif self.face_reverse:
            self.stand_face_right = False
            self.stand_face_left = True
            self.walk_left = False
            self.walk_right = False
            self.walk_count = 0

        else:
            self.stand_face_right = True
            self.stand_face_left = False
            self.walk_left = False
            self.walk_right = False
            self.face_reverse = False
            self.walk_count = 0

        if self.stand_face_right:
            if self.standCount < self.pic_rate_control_face_right:
                self.actor = self.actor_scale(
                    self.face_right_images[self.standCount // self.stay_frames])
                self.standCount += 1
            else:
                self.standCount = 0
        if self.stand_face_left:
            if self.standCount < self.pic_rate_control_face_left:
                self.actor = self.actor_scale(
                    self.face_left_images[self.standCount // self.stay_frames])
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
                self.vel_y = self.vy
        else:
            if self.controller.y + self.vel_y < self.upedge:
                self.vel_y += self.g
                self.controller.y += self.vel_y
            else:
                # self.controller.y = screen_height - Ground_edge - actor_height
                # 这里非常关键！！！！！！！！！！！！！！！！！！！！！8:46 一会儿接着做

                self.vel_y = self.upedge-self.controller.y
                self.controller.y += self.vel_y

                print(self.controller.y, self.upedge)
                if self.keys[self.up]:
                    self.jump = False
                else:
                    self.jump = True

    def action(self, platform_list):
        self.walk()
        self.Jump()
        self.upedge = screen_height - Ground_edge - actor_height
        self.rect = self.actor.get_rect()
        self.rect.x = self.controller.x
        self.rect.y = self.controller.y
        self.collide(platform_list)

    def float(self):
        if self.floating:
            self.vy += self.g
            self.vel_y = self.vy
            self.controller.y += self.vel_y

    def collide(self, platform_list):
        for i in platform_list:
            temp_rect = pg.Rect(i[0], i[1]-actor_height, i[2], i[3])
            if self.rect.colliderect(temp_rect) and self.vel_y > 0:
                print('发生碰撞')
                self.upedge = i[1]-actor_height


# Create actor1
actor1 = Actor(actor_width, actor_height, 'skeleton/StandR/', 'skeleton/StandL/',
               'skeleton/WalkingLeft/', 'skeleton/WalkingRight/', pg.K_a, pg.K_d, pg.K_w, controller_actor1)
actor2 = Actor(actor_width, actor_height,  'Hero/StandR/', 'Hero/StandL/', 'Hero/WalkingLeft/',
               'Hero/WalkingRight/', pg.K_LEFT, pg.K_RIGHT, pg.K_UP, controller_actor2)
# the FPS of this game
FPS = 60
clock = pg.time.Clock()


# the class of platform
class Pf():

    def __init__(self, x, y, PFW=screen_width//5, PFH=10):
        self.x = x
        self.y = y
        self.PFW = PFW
        self.PFH = PFH

    def show(self):
        global screen
        global platform_color
        global platform_list
        p1 = pg.Rect(self.x, self.y, self.PFW, self.PFH)
        p2 = pg.Rect(screen_width-self.x-self.PFW, self.y, self.PFW, self.PFH)
        pg.draw.rect(screen, platform_color, p1)
        pg.draw.rect(screen, platform_color, p2)
        if [self.x, self.y, self.PFW, self.PFH] in platform_list:
            pass
        else:
            platform_list += [[self.x, self.y, self.PFW, self.PFH],
                              [screen_width-self.x-self.PFW, self.y, self.PFW, self.PFH]]


# 画那些边界矩形
edges = [pg.Rect(0, 0, screen_width, BORDER),
         pg.Rect(0, screen_height - Ground_edge, screen_width, Ground_edge),
         pg.Rect(0, 0, BORDER, screen_height),
         pg.Rect(screen_width - BORDER, 0, BORDER, screen_height)
         ]


def main():
    run = True
    pg.mixer.music.play(loops=-1)
    while run:
        # draw the background
        screen.blit(Backgroud_picture, (0, 0))
        # drawing the edge of the border
        # Top side
        for i in edges:
            pg.draw.rect(screen, fg_color, i)

        # drawing the platforms(in pair to ensure the equity)
        # Top side
        Pf(screen_width // 8, screen_height // 6).show()  # The highest group
        Pf(BORDER, screen_height // 3).show()  # second highest group
        # the board players StandR on.
        Pf(screen_width // 10, screen_height // 2).show()
        Pf(screen_width // 6, screen_height -
           screen_height // 3).show()  # lowest board
        Pf(screen_width // 2 - screen_width // 8,
           screen_height // 3.5).show()  # middle board
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        actor1.action(platform_list)
        actor2.action(platform_list)

        screen.blit(actor1.actor, (actor1.controller.x, actor1.controller.y))
        pg.draw.rect(screen, (255, 255, 255), actor1.rect, 1)
        screen.blit(actor2.actor, (actor2.controller.x, actor2.controller.y))
        pg.draw.rect(screen, (255, 255, 255), actor2.rect, 1)

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
