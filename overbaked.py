import pygame, sys
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

num_players = 2

allsprites = pygame.sprite.RenderPlain()

def main():
    global screen, joysticks, bh
    
    pygame.init()
    pygame.display.set_caption('Overbaked!')

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((480, 480))

    joysticks = []
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    joysticks.append(joystick)

    joystick = pygame.joystick.Joystick(1)
    joystick.init()
    joysticks.append(joystick)

    bh = ButtonHandler()

    create_sprites()
    
    while True: # main game loop

        #checkForQuit()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
#            if event.type == KEYDOWN and event.key == K_x:
#                boy.handle_event_action()
#            if event.type == pygame.JOYBUTTONDOWN and joystick.get_button(2) == 1:
#                boy.handle_event_action()
            
        draw_background()
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.update()

        clock.tick(60)    

def create_sprites():
    global countertops, players
    
    # Countertop
    countertops = []
    countertops.append(Countertop('empty', 0, 0))
    countertops.append(Countertop('empty', 0, 1))
    countertops.append(Countertop('empty', 0, 2))
    countertops.append(Countertop('flourbin', 0, 3))
    countertops.append(Countertop('sugarbin', 0, 4))
    countertops.append(Countertop('butterbin', 0, 5))
    countertops.append(Countertop('empty', 0, 6))
    countertops.append(Countertop('empty', 0, 7))
    countertops.append(Countertop('empty', 1, 7))
    countertops.append(Countertop('mixer', 2, 7))
    countertops.append(Countertop('empty', 3, 7))
    countertops.append(Countertop('mixer', 4, 7))
    countertops.append(Countertop('empty', 5, 7))
    countertops.append(Countertop('empty', 6, 7))
    countertops.append(Countertop('empty', 7, 7))
    countertops.append(Countertop('empty', 7, 6))
    countertops.append(Countertop('empty', 7, 5))
    countertops.append(Countertop('empty', 7, 4))
    countertops.append(Countertop('empty', 7, 3))
    countertops.append(Countertop('empty', 7, 2))
    countertops.append(Countertop('empty', 7, 1))
    countertops.append(Countertop('empty', 7, 0))
    countertops.append(Countertop('empty', 6, 0))
    countertops.append(Countertop('empty', 5, 0))
    countertops.append(Countertop('oven', 4, 0))
    countertops.append(Countertop('empty', 3, 0))
    countertops.append(Countertop('oven', 2, 0))
    countertops.append(Countertop('empty', 1, 0))
    for x in countertops:
        allsprites.add(x)

    # Players
    players = []
    for i in range(0, num_players):
        players.append(Boy(i))
    for x in players:
        allsprites.add(x)

def draw_background():
    screen.fill(WHITE)


###########
# Sprites
###########

class Boy(pygame.sprite.Sprite):
    """Boy that can move around the screen"""
    speed = 3
    
    def __init__(self, joystick):
        pygame.sprite.Sprite.__init__(self)

        self.load_sprite_images()
        self.image = self.costumes_right[0]
        self.rect = self.image.get_rect()
        self.rect.center = screen.get_rect().center
        if joystick == 0:
            self.rect.move_ip(-40, 0)
        else:
            self.rect.move_ip(40, 0)

        self.step = 0
        self.chopstep = 0

        self.carrying_ingredient = False
        self.is_chopping = False

        self.joystick = joystick

    def update(self):

        # Handle move
        newrect = self.rect.copy()
        self.step = (self.step + 1) % 40
        if is_joystick(self.joystick, 'UP'):
            newrect.move_ip(0, -self.speed)
            self.image = self.costumes_up[self.step // 10]
            self.dir = 'UP'
        if is_joystick(self.joystick, 'DOWN'):
            newrect.move_ip(0, self.speed)
            self.image = self.costumes_down[self.step // 10]
            self.dir = 'DOWN'
        if is_joystick(self.joystick, 'RIGHT'):
            newrect.move_ip(self.speed, 0)
            self.image = self.costumes_right[self.step // 10]
            self.dir = 'RIGHT'
        if is_joystick(self.joystick, 'LEFT'):
            newrect.move_ip(-self.speed, 0)
            self.image = self.costumes_left[self.step // 10]
            self.dir = 'LEFT'
        
        # Check for wall collision
        counter_rects = []
        for x in countertops:
            counter_rects.append(x.rect)
        for x in players:
            if(x.joystick != self.joystick):
                counter_rects.append(x.rect)
        if newrect.collidelist(counter_rects) == -1:
            self.rect = newrect

        # Set active countertop
        active_countertop = self.get_active_countertop()
        
        # Handle button presses
        if False and bh.is_button_pressed('a'):
            if active_countertop != False:
                if self.carrying_ingredient:
                    self.carrying_ingredient = False
                    self.ingredient.place_on_countertop(active_countertop)
                    self.ingredient = 0
                elif active_countertop.current_ingredient != False and active_countertop.current_ingredient.can_be_picked_up():
                    self.carrying_ingredient = True
                    self.ingredient = active_countertop.current_ingredient
                    active_countertop.current_ingredient.pick_up(self)
                else:
                    if active_countertop.type == 'sugarbin':
                        self.carrying_ingredient = True
                        self.ingredient = Ingredient('sugar', self)
                    elif active_countertop.type == 'butterbin':
                        self.carrying_ingredient = True
                        self.ingredient = Ingredient('butter', self)
                    elif active_countertop.type == 'flourbin':
                        self.carrying_ingredient = True
                        self.ingredient = Ingredient('flour', self)

        if False and bh.is_button_pressed('b'):
            # Check if at chopping block

            # Check if there is an ingredient there

            # Set chopping state and notify ingredient that its being chopped
            self.is_chopping = True
            closest_ingredient = self.get_closest_ingredient()
            closest_ingredient.notify_chopping(self)

        if self.is_chopping:
            self.chopstep = (self.chopstep + 1) % 12
            self.image = self.costumes_downchop[self.chopstep // 3]

    def get_active_countertop(self):
        active_countertop = False
        active_area = 0
        for countertop in countertops:
            countertop.is_active = False
            if self.rect.inflate(5, 5).colliderect(countertop):
                active_clip = self.rect.inflate(5, 5).clip(countertop)
                if active_clip.width * active_clip.height > active_area:
                    active_countertop = countertop
                    active_area = active_clip.width * active_clip.height

        if active_countertop != False:
            active_countertop.is_active = True
        return active_countertop

    def get_closest_ingredient(self):
        for ingredient in ingredients:
            closest_ingredient = ingredient
            #if self.rect.inflate(5, 5).colliderect(ingredient):
            #    return ingredient
        return ingredient
        
    def notify_done_chopping(self):
        self.is_chopping = False
                        
    def handle_event_action(self):
        # Check if at a pantry
        if self.rect.inflate(10, 10).colliderect(pantry):
            print('Grab ingredient')
            #self.carrying_ingredient = true
            ingredient = Ingredient(self)
            #self.ingredient_being_carried = ingredient

    def load_sprite_images(self):
        sprite_image = pygame.image.load('images/mainguy.png')
        
        down1 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        down1.blit(sprite_image, (0, 0), Rect(2, 2, 52, 58))
        down2 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        down2.blit(sprite_image, (0, 0), Rect(78, 2, 52, 58))
        down3 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        down3.blit(sprite_image, (0, 0), Rect(154, 2, 52, 58))
        down4 = down2
        self.costumes_down = [down1, down2, down3, down4]

        right1 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        right1.blit(sprite_image, (0, 0), Rect(3, 60, 52, 58))
        right2 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        right2.blit(sprite_image, (0, 0), Rect(79, 60, 52, 58))
        right3 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        right3.blit(sprite_image, (0, 0), Rect(152, 60, 52, 58))
        right4 = right2
        self.costumes_right = [right1, right2, right3, right4]

        up1 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        up1.blit(sprite_image, (0, 0), Rect(1, 119, 52, 58))
        up2 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        up2.blit(sprite_image, (0, 0), Rect(77, 119, 52, 58))
        up3 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        up3.blit(sprite_image, (0, 0), Rect(153, 119, 52, 58))
        up4 = up2
        self.costumes_up = [up1, up2, up3, up4]

        left1 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        left1.blit(sprite_image, (0, 0), Rect(0, 178, 52, 58))
        left2 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        left2.blit(sprite_image, (0, 0), Rect(75, 178, 52, 58))
        left3 = pygame.Surface((52, 58), flags=pygame.SRCALPHA)
        left3.blit(sprite_image, (0, 0), Rect(150, 178, 52, 58))
        left4 = left2
        self.costumes_left = [left1, left2, left3, left4]

        downchop1 = pygame.Surface((62, 58), pygame.SRCALPHA)
        downchop1.blit(sprite_image, (0, 0), Rect(206, 2, 62, 58))
        downchop2 = pygame.Surface((62, 58), pygame.SRCALPHA)
        downchop2.blit(sprite_image, (0, 0), Rect(276, 2, 62, 58))
        downchop3 = pygame.Surface((62, 58), pygame.SRCALPHA)
        downchop3.blit(sprite_image, (0, 0), Rect(342, 2, 62, 58))
        downchop4 = downchop2
        self.costumes_downchop = [downchop1, downchop2, downchop3, downchop4]

        rightchop1 = pygame.Surface((52, 58), pygame.SRCALPHA)
        rightchop1.blit(sprite_image, (0, 0), Rect(219, 60, 52, 58))
        rightchop2 = pygame.Surface((63, 58), pygame.SRCALPHA)
        rightchop2.blit(sprite_image, (0, 0), Rect(289, 60, 63, 58))
        rightchop3 = pygame.Surface((74, 58), pygame.SRCALPHA)
        rightchop3.blit(sprite_image, (0, 0), Rect(355, 60, 74, 58))
        rightchop4 = rightchop2
        self.costumes_rightchop = [rightchop1, rightchop2, rightchop3, rightchop4]

        upchop1 = pygame.Surface((55, 58), pygame.SRCALPHA)
        upchop1.blit(sprite_image, (0, 0), Rect(217, 119, 55, 58))
        upchop2 = pygame.Surface((62, 58), pygame.SRCALPHA)
        upchop2.blit(sprite_image, (0, 0), Rect(287, 119, 62, 58))
        upchop3 = pygame.Surface((60, 58), pygame.SRCALPHA)
        upchop3.blit(sprite_image, (0, 0), Rect(353, 119, 60, 58))
        upchop4 = upchop2
        self.costumes_upchop = [upchop1, upchop2, upchop3, upchop4]

        leftchop1 = pygame.Surface((74, 58), pygame.SRCALPHA)
        leftchop1.blit(sprite_image, (0, 0), Rect(207, 178, 74, 58))
        leftchop2 = pygame.Surface((74, 58), pygame.SRCALPHA)
        leftchop2.blit(sprite_image, (0, 0), Rect(296, 178, 74, 58))
        leftchop3 = pygame.Surface((74, 58), pygame.SRCALPHA)
        leftchop3.blit(sprite_image, (0, 0), Rect(375, 178, 74, 58))
        leftchop4 = leftchop2
        self.costumes_leftchop = [leftchop1, leftchop2, leftchop3, leftchop4]

class Countertop(pygame.sprite.Sprite):
    def __init__(self, mytype, gridx, gridy):
        pygame.sprite.Sprite.__init__(self)

        self.type = mytype
        self.load_sprite_images()

        self.rect = self.baseimage.get_rect()
        self.rect.left = gridx * 60
        self.rect.top = gridy * 60

        self.is_active = False
        self.current_ingredient = False

    def update(self):
        self.image = self.baseimage.copy()
        
        if self.is_active:
            pygame.draw.rect(self.image, BLUE, self.image.get_rect(), 2)

    def load_sprite_images(self):
        
        if(self.type == 'empty'):
            self.baseimage = pygame.image.load('images/countertop.png')
        elif(self.type == 'flourbin'):
            self.baseimage = pygame.image.load('images/flour.png')
        elif(self.type == 'sugarbin'):
            self.baseimage = pygame.image.load('images/sugar.png')
        elif(self.type == 'butterbin'):
            self.baseimage = pygame.image.load('images/butter.png')
        elif(self.type == 'mixer'):
            self.baseimage = pygame.image.load('images/mixerempty.png')
        elif(self.type == 'oven'):
            self.baseimage = pygame.image.load('images/oven.png')
        

class Ingredient(pygame.sprite.Sprite):
    """Ingredient that can be used to make recipes"""
    def __init__(self, mytype, parent):
        pygame.sprite.Sprite.__init__(self)

        self.load_sprite_images()
        self.image = self.costume_unchopped
        self.rect = self.image.get_rect()
        self.parent = parent
        allsprites.add(self)

        self.is_being_carried = True
        self.is_being_chopped = False
        self.chopstep = 0

        ingredients.append(self)

    def update(self):
        if self.is_being_carried:
            if self.parent.dir == 'LEFT':
                self.rect.centery = self.parent.rect.centery
                self.rect.right = self.parent.rect.left
            elif self.parent.dir == 'RIGHT':
                self.rect.centery = self.parent.rect.centery
                self.rect.left = self.parent.rect.right
            elif self.parent.dir == 'UP':
                self.rect.centerx = self.parent.rect.centerx
                self.rect.bottom = self.parent.rect.top
            elif self.parent.dir == 'DOWN':
                self.rect.centerx = self.parent.rect.centerx
                self.rect.top = self.parent.rect.bottom

        if self.is_being_chopped:
            self.chopstep = self.chopstep + 1
            if self.chopstep == 360:
                self.image = self.costume_chopped
                self.is_being_chopped = False
                self.player_chopping.notify_done_chopping()
            else:
                self.image = self.costumes_chopping[self.chopstep // 60]

    def can_be_picked_up(self):
        if self.is_being_chopped:
            return False
        else:
            return True

    def pick_up(self, player):
        self.is_being_carried = True
        self.parent = player

    def place_on_countertop(self, countertop):
        self.rect.center = countertop.rect.center
        self.is_being_carried = False
        countertop.current_ingredient = self

    def notify_chopping(self, player_chopping):
        self.is_being_chopped = True
        self.player_chopping = player_chopping

    def load_sprite_images(self):
        #sprite_image = pygame.image.load('images/.png')
        
        unchopped = pygame.Surface((36, 36), flags=pygame.SRCALPHA)
        unchopped.blit(sprite_image, (0, 0), Rect(0, 0, 36, 36))
        chopping1 = pygame.Surface((40, 36), flags=pygame.SRCALPHA)
        chopping1.blit(sprite_image, (0, 0), Rect(0, 36, 40, 36))
        chopping2 = pygame.Surface((40, 36), flags=pygame.SRCALPHA)
        chopping2.blit(sprite_image, (0, 0), Rect(0, 72, 40, 36))
        chopping3 = pygame.Surface((40, 36), flags=pygame.SRCALPHA)
        chopping3.blit(sprite_image, (0, 0), Rect(0, 108, 40, 36))
        chopping4 = pygame.Surface((49, 36), flags=pygame.SRCALPHA)
        chopping4.blit(sprite_image, (0, 0), Rect(0, 145, 49, 36))
        chopping5 = pygame.Surface((49, 36), flags=pygame.SRCALPHA)
        chopping5.blit(sprite_image, (0, 0), Rect(0, 181, 49, 36))
        chopping6 = pygame.Surface((49, 36), flags=pygame.SRCALPHA)
        chopping6.blit(sprite_image, (0, 0), Rect(0, 217, 49, 36))
        chopped = pygame.Surface((49, 36), flags=pygame.SRCALPHA)
        chopped.blit(sprite_image, (0, 0), Rect(0, 256, 49, 36))

        self.costume_unchopped = unchopped
        self.costume_chopped = chopped
        self.costumes_chopping = [chopping1, chopping2, chopping3, chopping4, chopping5, chopping6]

###########
# Framework Functions
###########

def is_joystick(i, dir):
    joystick = joysticks[i]
    if dir == 'RIGHT':
        axis = joystick.get_axis(0)
        return (axis > 0.9)
    if dir == 'LEFT':
        axis = joystick.get_axis(0)
        return (axis < -0.9)
    if dir == 'DOWN':
        axis = joystick.get_axis(1)
        return (axis > 0.9)
    if dir == 'UP':
        axis = joystick.get_axis(1)
        return (axis < -0.9)

class ButtonHandler:
    def __init__(self):
        self.button_is_pressed = [False, False, False, False]

    def is_button_pressed(self, btn):
        retval = False
        btn_index = self.get_button_index(btn)
        if joystick.get_button(btn_index) == 1:
            if not self.button_is_pressed[btn_index]:
                retval = True
            self.button_is_pressed[btn_index] = True
        else:
            self.button_is_pressed[btn_index] = False
        return retval

    def get_button_index(self, btn):
        btn_index = -1
        if(btn == 'a'):
            btn_index = 1
        if(btn == 'b'):
            btn_index = 2
        if(btn == 'x'):
            btn_index = 0
        if(btn == 'y'):
            btn_index = 3
        
        return btn_index


def terminate():
    print('Terminate called')
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        print('event quit')
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

# Run main loop if run as script
if __name__ == '__main__':
    main()
