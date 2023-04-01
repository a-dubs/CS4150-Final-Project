from typing import Optional, Any
import arcade
import arcade.color as colors
from arcade import Sprite,SpriteList,SpriteCircle, Texture
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
PLAYER_HEALTH_NORMAL = 1000
ENEMY_HEALTH_NORMAL = 200
BULLET_DMG = 100

ENEMY_SPEED = 5
# ENEMY_ACCEL = 
PLAYER_SPEED = 5

BULLET_SPEED = 35.0
FRIENDLY_BULLET_COLOR = colors.GOLDEN_POPPY
FRIENDLY_BULLET_RADIUS = 5
ENEMY_BULLET_RADIUS = 4
ENEMY_BULLET_COLOR = colors.RED_PURPLE


class Person(arcade.Sprite):

    def __init__(self, hp : int, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)
        self.hp = hp

    def update(self):
        super().update()

    def take_damage(self,damage:int):
        self.hp -= damage

# class PersonList(SpriteList):
#     def __init__(self, use_spatial_hash=None, spatial_hash_cell_size=128, is_static=False, atlas: "TextureAtlas" = None, capacity: int = 100, lazy: bool = False, visible: bool = True):
#         super().__init__(use_spatial_hash, spatial_hash_cell_size, is_static, atlas, capacity, lazy, visible)
    
#     def append(self, person: Person):
#         return super().append(sprite)
    
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
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles_list = arcade.SpriteList()
        self.score = 0
        self.time_elapsed = 0
        # self.all_sprites = arcade.SpriteList()
        
        self.setup()

    def setup(self):

        # setup up background
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        
        # set up player
        self.player = Person(hp=PLAYER_HEALTH_NORMAL,filename="resources/sprites/player.png",scale=PLAYER_SCALE)
        self.player.center_x =  CENTER_X
        self.player.center_y =  CENTER_Y
        self.players_list.append(self.player)

        # Spawn a new enemy every  seconds
        # arcade.schedule(self.spawn_enemy, 1)
        arcade.schedule(self.make_enemies_shoot, 1)

    def spawn_enemy(self, d_time: float):
        enemy_freq = 0.5
        if random() < enemy_freq * d_time:
            # enemy = arcade.Sprite("resources/sprites/enemy.png",image_height=ENEMY_HEIGHT,image_width=ENEMY_WIDTH)
            enemy = Person(hp=ENEMY_HEALTH_NORMAL,filename="resources/sprites/enemy2.png",scale=ENEMY_SCALE)
            # spawn on left and right of screen
            if randint(0,1): 
                enemy.center_x = CENTER_X + CENTER_X * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_X * dir
                enemy.center_y = SCREEN_HEIGHT * random()
                enemy.angle = 270 if dir == -1 else 90
                enemy.change_x = 1 if dir == -1 else -1
            # spawn on top and bottom of screen
            else:
                enemy.center_y = CENTER_Y + CENTER_Y * (dir:=(-1)**randint(0,1)) + 0.01*randint(0,25) * CENTER_Y * dir
                enemy.center_x = SCREEN_WIDTH * random()
                enemy.angle = 0 if dir == -1 else 180
                enemy.change_y = 1 if dir == -1 else -1

            # Add it to the enemies list
            self.enemies_list.append(enemy)

    def make_enemies_shoot(self, dt: float):
        for e in self.enemies_list:
            self.shoot_from(e)

    def shoot_from(self, sprite : arcade.Sprite):
        bullet = SpriteCircle(FRIENDLY_BULLET_RADIUS if sprite in self.players_list else ENEMY_BULLET_RADIUS,
                              color=(FRIENDLY_BULLET_COLOR if sprite in self.players_list else ENEMY_BULLET_COLOR))
        # bullet.center_x = sprite.center_x + sprite.width * 0.65 * cos(sprite.radians+pi*0.44)
        # bullet.center_y = sprite.center_y + sprite.height * 0.65 * sin(sprite.radians+pi*0.44)
        bullet.center_x = sprite.center_x + sprite.width * 0.7 * cos(sprite.radians+0.5*pi)
        bullet.center_y = sprite.center_y + sprite.height * 0.7 * sin(sprite.radians+0.5*pi)
        # bullet.face_point((self._mouse_x,self._mouse_y))
        spread = 20 # in degrees, cone of innaccuracy
        bullet.radians = sprite.radians + 0.5*pi + (pi*spread*(random()-0.5)/180)

        bullet.change_x = BULLET_SPEED * cos(bullet.radians)
        bullet.change_y = BULLET_SPEED * sin(bullet.radians)
        # bullet.forward(10)
        self.projectiles_list.append(bullet)
        # bullet.color


    def end_game(self):
        pass
        

    def updateProjectiles(self):
        for proj in self.projectiles_list:
            # if ((proj.color == FRIENDLY_BULLET_COLOR and (enemies:=proj.collides_with_list(self.enemies_list))) 
                # or (proj.color == ENEMY_BULLET_COLOR and (players:=proj.collides_with_list(self.players_list)))):
            if proj.width/2 == FRIENDLY_BULLET_RADIUS and (enemies:=proj.collides_with_list(self.enemies_list)):
                if enemies:
                    [e.take_damage(BULLET_DMG) for e in enemies]  
                proj.kill()
            if proj.width/2 == ENEMY_BULLET_RADIUS and (players:=proj.collides_with_list(self.players_list)):
                if players:
                    [p.take_damage(BULLET_DMG) for p in players]  
                proj.kill()
            if (obstacle:=proj.collides_with_list(self.obstacles_list)):
                proj.kill()
            if not 0 < proj.center_x < SCREEN_WIDTH or not 0 < proj.center_y < SCREEN_HEIGHT:
                proj.kill()



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F4:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.ESCAPE:
            self.paused = not self.paused
            # print(self.paused)

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = PLAYER_SPEED

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -PLAYER_SPEED

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -PLAYER_SPEED

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = PLAYER_SPEED

        if symbol == arcade.key.SPACE:
            self.shoot_from(self.players_list[0])

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            if self.player.change_y == PLAYER_SPEED:
                self.player.change_y = 0

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            if self.player.change_y == -PLAYER_SPEED:
                self.player.change_y = 0

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            if self.player.change_x == -PLAYER_SPEED:
                self.player.change_x = 0

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            if self.player.change_x == PLAYER_SPEED:
                self.player.change_x = 0


    def on_update(self, dt: float):
        """
        Update the positions and statuses of all game objects
        
        Arguments:
            delta_time {float} -- Time since the last update
        """

        if self.paused:
            return
        
        self.time_elapsed += dt
        
        self.players_list[0].face_point((self._mouse_x,self._mouse_y))
        # self.player.change_x = 1.0 * cos(self.player.radians+0.5*pi)
        # self.player.change_y = 1.0 * sin(self.player.radians+0.5*pi)

        self.spawn_enemy(dt)
        # self.players_list[0].change_x = 0
        # self.players_list[0].change_y = 0
        
        # Update everything
        self.players_list.update()
        self.enemies_list.update()
        self.projectiles_list.update()
        self.obstacles_list.update()
        self.updateProjectiles()

        for enemy in self.enemies_list:
            if enemy.hp <= 0:
                enemy.kill()
                self.score += 1

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0    


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
        arcade.draw_rectangle_filled(center_x=CENTER_X,center_y=SCREEN_HEIGHT-30, width=200, height=60,color=colors.GRAY_ASPARAGUS)
        arcade.draw_text(f"Score: {self.score}", start_x=CENTER_X-100, start_y=SCREEN_HEIGHT-30,font_size=20,align="center",color=colors.WHITE_SMOKE,width=200)


# Main code entry point
if __name__ == "__main__":
    app = ColdpointSeattle()
    arcade.run()
