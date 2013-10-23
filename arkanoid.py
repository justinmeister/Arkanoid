import pygame
import sys
from pygame.locals import *

#CONSTANTS#

DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480

## COLORS ##

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)

BGCOLOR = BLACK
BLOCKGAP = 2
BLOCKWIDTH = 62
BLOCKHEIGHT = 25
ARRAYWIDTH = 10
ARRAYHEIGHT = 5
PADDLEWIDTH = 100
PADDLEHEIGHT = 10
BALLRADIUS = 20
BALLCOLOR = WHITE
BLOCK = 'block'
BALL = 'ball'
PADDLE = 'paddle'
BALLSPEED = 4


class Block(pygame.sprite.Sprite):
 
    def __init__(self):
        self.blockWidth = BLOCKWIDTH
        self.blockHeight = BLOCKHEIGHT
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.blockWidth, self.blockHeight))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.name = BLOCK


        
class Ball(pygame.sprite.Sprite):
    def __init__(self, displaySurf):
        pygame.sprite.Sprite.__init__(self)
        self.name = BALL
        self.moving = False
        self.image = pygame.Surface((15, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vectorx = BALLSPEED
        self.vectory = BALLSPEED * -1
        self.score = 0
        

    def update(self, mousex, blocks, paddle, *args):
        if self.moving == False:
            self.rect.centerx = mousex

        else:
            self.rect.y += self.vectory

            hitGroup = pygame.sprite.Group(paddle, blocks)

            spriteHitList = pygame.sprite.spritecollide(self, hitGroup, False)
            if len(spriteHitList) > 0:
                for sprite in spriteHitList:
                    if sprite.name == BLOCK:
                        sprite.kill()
                        self.score += 1
                self.vectory *= -1
                self.rect.y += self.vectory
            
            self.rect.x += self.vectorx
            
            blockHitList = pygame.sprite.spritecollide(self, blocks, True)
                
            if len(blockHitList) > 0:
                self.vectorx *= -1
                self.score += 1
                
                

            if self.rect.right > DISPLAYWIDTH:
                self.vectorx *= -1
                self.rect.right = DISPLAYWIDTH

            elif self.rect.left < 0:
                self.vectorx *= -1
                self.rect.left = 0

            if self.rect.top < 0:
                self.vectory *= -1
                self.rect.top = 0


        
class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PADDLEWIDTH, PADDLEHEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.name = PADDLE


    def update(self, mousex, *args):
        if self.rect.x >= 0 and self.rect.right <= DISPLAYWIDTH:
            self.rect.centerx = mousex

        if self.rect.x < 0:
            self.rect.x = 0

        elif self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
        
        
class Score(object):
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont('Helvetica', 25)
        self.render = self.font.render('Score: ' + str(self.score), True, WHITE, BLACK)
        self.rect = self.render.get_rect()
        self.rect.x = 0
        self.rect.bottom = DISPLAYHEIGHT

        


class App(object):
    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.mousex = 0
        self.blocks = self.createBlocks()
        self.paddle = self.createPaddle()
        self.ball = self.createBall()
        self.score = Score()

        self.allSprites = pygame.sprite.Group(self.blocks, self.paddle, self.ball)


    def updateScore(self):
        self.score.score = self.ball.score
        self.score.render = self.score.font.render('Score: ' + str(self.score.score), True, WHITE, BLACK)
        self.score.rect = self.score.render.get_rect()
        self.score.rect.x = 0
        self.score.rect.bottom = DISPLAYHEIGHT


    def makeScreen(self):
        pygame.display.set_caption('Arkanoid')
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        displaySurf.fill(BGCOLOR)
        displaySurf.convert()

        return displaySurf, displayRect


    def createBall(self):
        ball = Ball(self.displaySurf)
        ball.rect.centerx = self.paddle.rect.centerx
        ball.rect.bottom = self.paddle.rect.top

        return ball


    def createPaddle(self):
        paddle = Paddle()
        paddle.rect.centerx = self.displayRect.centerx
        paddle.rect.bottom = self.displayRect.bottom

        return paddle


    def createBlocks(self):
        blocks = pygame.sprite.Group()
        
        for row in range(ARRAYHEIGHT):
            for i in range(ARRAYWIDTH):
                block = Block()
                block.rect.x = i * (BLOCKWIDTH + BLOCKGAP)
                block.rect.y = row * (BLOCKHEIGHT + BLOCKGAP)
                block.color = self.setBlockColor(block, row, i)
                block.image.fill(block.color)
                blocks.add(block)

        return blocks


    def setBlockColor(self, block, row, column):
        if column == 0 or column % 2 == 0:
            return YELLOW
        else:
            return CYAN
        

    def checkInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()

            if event.type == MOUSEMOTION:
                #We only need the x value of a mousemotion, so we grab
                #only the first value of the event.pos tuple
                self.mousex = event.pos[0]

            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    self.ball.moving = True
                

    def terminate(self):
        pygame.quit()
        sys.exit()



    def mainLoop(self):
        while True:
            self.displaySurf.fill(BGCOLOR)
            self.updateScore()
            self.displaySurf.blit(self.score.render, self.score.rect)
            self.allSprites.update(self.mousex, self.blocks, self.paddle)
            self.allSprites.draw(self.displaySurf)
            pygame.display.update()
            self.checkInput()
            
            
if __name__ == '__main__':

    runGame = App()
    runGame.mainLoop()
   
