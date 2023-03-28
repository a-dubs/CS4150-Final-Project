import arcade
import arcade.color as colors
from arcade import Sprite,SpriteList,SpriteCircle
from random import random, randint, randrange
from math import cos, tan, sin, pi

# https://realpython.com/arcade-python-game-framework/

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HEIGHT / 2
# SCALING = 10.0
SCREEN_TITLE = "Coldpoint Seattle"

ENEMY_SCALE = 0.2
PLAYER_SCALE = 0.2
# ENEMY_HEIGHT = 50
# ENEMY_WIDTH = 50
# PLAYER_HEIGHT = 50
# PLAYER_WIDTH = 50

BULLET_SPEED = 35.0
FRIENDLY_BULLET_COLOR = colors.GOLDEN_POPPY
ENEMY_BULLET_COLOR = colors.RED_PURPLE

# Classes
class ColdpointSeattle(arcade.Window):
    """Main welcome window
    """
    def __init__(self):
        """Initialize the window
        """

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # setup random member variables
        self.paused = False
        # set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.players_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()
        self.projectiles_list = arcade.SpriteList()
        # self.all_sprites = arcade.SpriteList()
        
        self.setup()

    def setup(self):

        # setup up background
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        
        
        # set up player
        self.player = arcade.Sprite("resources/sprites/player.png",scale=PLAYER_SCALE)
        self.player.center_x =  CENTER_X
        self.player.center_y =  CENTER_Y
        self.players_list.append(self.player)

        # Spawn a new enemy every  seconds
        arcade.schedule(self.spawn_enemy, 1)

    def spawn_enemy(self, d_time: float):
        # enemy = arcade.Sprite("resources/sprites/enemy.png",image_height=ENEMY_HEIGHT,image_width=ENEMY_WIDTH)
        enemy = arcade.Sprite("resources/sprites/enemy2.png",scale=ENEMY_SCALE)
        # enemy.center_x = CENTER_X + 0.75 * CENTER_X * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_X * dir
        # enemy.center_y = CENTER_Y + 0.75 * CENTER_Y * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_Y * dir
        if randint(0,1):
            enemy.center_x = CENTER_X + CENTER_X * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_X * dir
            enemy.center_y = SCREEN_HEIGHT + 0.01*randint(0,25) * SCREEN_HEIGHT * (dir2:=(-1)**randint(0,1))
            enemy.angle = 270 if dir == -1 else 90
            enemy.change_x = 1 if dir == -1 else -1
        else:
            enemy.center_y = CENTER_Y + CENTER_Y * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_Y * dir
            enemy.center_x = SCREEN_WIDTH + 0.01*randint(0,25) * SCREEN_WIDTH * (dir2:=(-1)**randint(0,1))
            enemy.angle = 0 if dir == -1 else 180
            enemy.change_y = 1 if dir == -1 else -1

        # enemy.forward(2.0)
        # Add it to the enemies list
        self.enemies_list.append(enemy)
        # self.all_sprites.append(enemy)

    def on_draw(self):
        """Called whenever you need to draw your window
        """
        # Clear the screen and start drawing
        arcade.start_render()

        # draw rectangle 
        # arcade.draw_rectangle_filled(self._mouse_x,self._mouse_y,20,100,colors.BLACK)
        self.enemies_list.draw()
        self.players_list.draw()
        self.obstacles_list.draw()
        self.projectiles_list.draw()

    def shoot(self, sprite : arcade.Sprite):
        bullet = SpriteCircle(4,color=(FRIENDLY_BULLET_COLOR if sprite.position in [p.position for p in self.players_list] else ENEMY_BULLET_COLOR))
        # bullet.center_x = sprite.center_x + sprite.width * 0.65 * cos(sprite.radians+pi*0.44)
        # bullet.center_y = sprite.center_y + sprite.height * 0.65 * sin(sprite.radians+pi*0.44)
        bullet.center_x = sprite.center_x + sprite.width * 0.5 * cos(sprite.radians+0.5*pi)
        bullet.center_y = sprite.center_y + sprite.height * 0.5 * sin(sprite.radians+0.5*pi)
        # bullet.face_point((self._mouse_x,self._mouse_y))
        bullet.radians = sprite.radians + 0.5*pi
        bullet.change_x = BULLET_SPEED * cos(bullet.radians)
        bullet.change_y = BULLET_SPEED * sin(bullet.radians)
        # bullet.forward(10)
        self.projectiles_list.append(bullet)
        # bullet.color
        

    def updateProjectiles(self):
        for proj in self.projectiles_list:
            players = None
            enemies = None
            if ((proj.color == FRIENDLY_BULLET_COLOR and (enemies:=proj.collides_with_list(self.enemies_list))) 
                or (proj.color == ENEMY_BULLET_COLOR and (players:=proj.collides_with_list(self.enemies_list)))):
                if enemies:
                    [e.kill() for e in enemies]  
                proj.kill()
            elif (obstacle:=proj.collides_with_list(self.obstacles_list)):
                proj.kill()
            


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F4:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.ESCAPE:
            self.paused = not self.paused

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

        if symbol == arcade.key.SPACE:
            self.shoot(self.players_list[0])

    
    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If paused, do nothing

        Arguments:
            delta_time {float} -- Time since the last update

        """
        if self.paused:
            return
        
        self.players_list[0].face_point((self._mouse_x,self._mouse_y))
        self.player.change_x = 1.0 * cos(self.player.radians+0.5*pi)
        self.player.change_y = 1.0 * sin(self.player.radians+0.5*pi)

        # Update everything
        self.players_list.update()
        self.enemies_list.update()
        self.projectiles_list.update()
        self.obstacles_list.update()

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0    

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        return super().on_mouse_motion(x, y, dx, dy)
    


# Main code entry point
if __name__ == "__main__":
    app = ColdpointSeattle()
    arcade.run()
