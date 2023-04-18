from ast import List, Tuple
from typing import Optional, Any
import arcade
import arcade.color as colors
from arcade import Sprite, SpriteList, SpriteCircle, Texture
from random import random, randint, randrange, choice
from math import cos, tan, sin, pi
import numpy as np
import math
# import modular_ai as ai
from modular_ai import *
from sprite_ai import *
from constants import *

# https://realpython.com/arcade-python-game-framework/


# class Weapon():

#     def __init__(self) -> None:
#         pass

# class Gun(Weapon):
#     def __init__(self, bullet_capacity:int. spread:float, b) -> None:
#         super().__init__()


# class Person(arcade.Sprite):

#     def __init__(self, hp: int, max_speed: float, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
#         super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x,
#                          repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)
#         self.hp = hp
#         # self.ammo = 20
#         self.max_speed = max_speed

#     def update(self):
#         super().update()

#     def take_damage(self, damage: int):
#         self.hp -= damage
#         # if self.hp <= 0:
#         #     self.kill()

#     # returns true if already at
#     def move_to_pos(self, target_pos:tuple[float,float]) -> bool:
#         if (dist_btwn:=dist(self.position,target_pos)) == 0:
#             self.change_x = 0
#             self.change_y = 0
#             return True
#         target_dir = norm_vect_btwn(self.position,target_pos)
#         target_velocity_vect = target_dir*min(dist_btwn,self.max_speed)
#         self.change_x = target_velocity_vect[0]
#         self.change_y = target_velocity_vect[1]
#         return False

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
        # self.players_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles_list = arcade.SpriteList()
        self.score = 0
        self.time_elapsed = 0
        self.EnemyAIs: list[SpriteAI] = []
        # self.all_sprites = arcade.SpriteList()

        self.setup()

    def setup(self):

        # setup up background
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        # set up player
        self.player = Person(
            is_player=True,
            hp=PLAYER_HEALTH_NORMAL, speed=PLAYER_SPEED, filename="resources/sprites/player.png", scale=PLAYER_SCALE)
        self.player.center_x = CENTER_X
        self.player.center_y = CENTER_Y
        # self.players_list.append(self.player)

        self.generate_obstacles()


    def generate_obstacles(self):
        # for i in range(randint(10, 20)):
        for i in range(1):
            # North/South facing obstacle
            # if random() < 0.5:
            #     obs = arcade.SpriteSolidColor(width=randint(75, 150),
            #                                   height=randint(20, 30),
            #                                   color=choice(OBSTACLE_COLORS))
            # else:
            #     obs = arcade.SpriteSolidColor(width=randint(20, 30),
            #                                   height=randint(75, 150),
            #                                   color=choice(OBSTACLE_COLORS))
            obs = arcade.SpriteSolidColor(
                # width=randint(20,40) if random() < 0.5 else randint(40,60),
                # height=randint(20,40) if random() < 0.5 else randint(40,60),
                width=randint(40, 60),
                height=randint(40, 60),
                color=choice(OBSTACLE_COLORS))
            obs.center_x = randint(150, SCREEN_WIDTH-150)
            obs.center_y = randint(150, SCREEN_HEIGHT-150)
            self.obstacles_list.append(obs)

    def spawn_enemy(self, d_time: float, force_spawn=False):
        enemy_freq = 0.5
        if random() < enemy_freq * d_time or force_spawn == True:
            # enemy = arcade.Sprite("resources/sprites/enemy.png",image_height=ENEMY_HEIGHT,image_width=ENEMY_WIDTH)
            enemy = SpriteAI(
                hp=ENEMY_HEALTH_NORMAL,
                speed=ENEMY_SPEED,
                filename="resources/sprites/enemy2.png",
                scale=ENEMY_SCALE)
            enemy.update_game_state(*self.getGameState())
            considerations = [
                AboveThreshold(1, 0, enemy.line_of_sight),
                # AboveThreshold(1, 0, enemy.line_of_sight),
            ]
            shoot_on_sight = Option(5,considerations=considerations,actions=["shoot"])
            enemy.add_option(shoot_on_sight)
            # spawn on left and right of screen
            if randint(0, 1):
                enemy.center_x = CENTER_X + CENTER_X * \
                    (dir := (-1)**randint(0, 1)) + \
                    0.01*randint(0, 25) * CENTER_X * dir
                enemy.center_y = SCREEN_HEIGHT * random()
                enemy.angle = 270 if dir == -1 else 90
                enemy.change_x = 1 if dir == -1 else -1
            # spawn on top and bottom of screen
            else:
                enemy.center_y = CENTER_Y + CENTER_Y * \
                    (dir := (-1)**randint(0, 1)) + \
                    0.01*randint(0, 25) * CENTER_Y * dir
                enemy.center_x = SCREEN_WIDTH * random()
                enemy.angle = 0 if dir == -1 else 180
                enemy.change_y = 1 if dir == -1 else -1

            # Add it to the enemies list
            self.enemies_list.append(enemy)
            self.EnemyAIs.append(enemy)


    def shoot_from(self, sprite: Sprite):
        bullet = SpriteCircle(FRIENDLY_BULLET_RADIUS if sprite == self.player else ENEMY_BULLET_RADIUS,
                              color=(FRIENDLY_BULLET_COLOR if sprite == self.player else ENEMY_BULLET_COLOR))
        # bullet.center_x = sprite.center_x + sprite.width * 0.65 * cos(sprite.radians+pi*0.44)
        # bullet.center_y = sprite.center_y + sprite.height * 0.65 * sin(sprite.radians+pi*0.44)
        bullet.center_x = sprite.center_x + \
            sprite.width * 0.7 * cos(sprite.radians+0.5*pi)
        bullet.center_y = sprite.center_y + \
            sprite.height * 0.7 * sin(sprite.radians+0.5*pi)
        # bullet.face_point((self._mouse_x,self._mouse_y))
        spread = 10  # in degrees, cone of innaccuracy
        bullet.radians = sprite.radians + 0.5 * \
            pi + (pi*spread*(random()-0.5)/180)

        bullet.change_x = BULLET_SPEED * cos(bullet.radians)
        bullet.change_y = BULLET_SPEED * sin(bullet.radians)
        # bullet.forward(10)
        self.projectiles_list.append(bullet)
        # bullet.color

    def getGameState(self):
        return self.player, self.enemies_list, self.obstacles_list, self.projectiles_list

    def end_game(self):
        pass

    def updateProjectiles(self):
        for proj in self.projectiles_list:
            # if ((proj.color == FRIENDLY_BULLET_COLOR and (enemies:=proj.collides_with_list(self.enemies_list)))
            # or (proj.color == ENEMY_BULLET_COLOR and (players:=proj.collides_with_list(self.players_list)))):
            if proj.width/2 == FRIENDLY_BULLET_RADIUS and (enemies := proj.collides_with_list(self.enemies_list)):
                if enemies:
                    [e.take_damage(BULLET_DMG) for e in enemies]
                proj.kill()
            if proj.width/2 == ENEMY_BULLET_RADIUS and (player := proj.collides_with_sprite(self.player)):
                if player:
                    self.player.take_damage(BULLET_DMG)
                    print("OUCH")
                proj.kill()
            if (obstacle := proj.collides_with_list(self.obstacles_list)):
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
            self.player.shoot()

        if symbol == arcade.key.R:
            self.player.reload()

        if symbol == arcade.key.ENTER:
            self.spawn_enemy(0, force_spawn=True)

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

        self.player.face_point((self._mouse_x, self._mouse_y))
        # self.player.change_x = 1.0 * cos(self.player.radians+0.5*pi)
        # self.player.change_y = 1.0 * sin(self.player.radians+0.5*pi)

        # self.spawn_enemy(dt)
        # self.players_list[0].change_x = 0
        # self.players_list[0].change_y = 0

        # self.players_list.update()
        self.player.update_game_state(*self.getGameState())
        self.player.tick(dt)
        self.player.update()
        self.projectiles_list.update()
        self.obstacles_list.update()
        self.updateProjectiles()

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        # do EnemyAI stuff
        for enemyAI in self.EnemyAIs:
            enemyAI.update_game_state(*self.getGameState())
            enemyAI.tick(dt)

        for enemyAI in self.EnemyAIs:
            if enemyAI.hp <= 0:
                enemyAI.kill()
                self.EnemyAIs.remove(enemyAI)
                self.score += 1
        self.enemies_list.update()

    def on_draw(self):
        """Called whenever you need to draw your window
        """
        # Clear the screen and start drawing
        arcade.start_render()

        # draw rectangle
        # arcade.draw_rectangle_filled(self._mouse_x,self._mouse_y,20,100,colors.BLACK)
        self.enemies_list.draw()
        self.player.draw()
        self.obstacles_list.draw()
        self.projectiles_list.draw()

        # def draw_sightlines(self):
        for enemyAI in self.EnemyAIs:
            if (has_los := has_line_of_sight(viewer=self.player, target=enemyAI, obstacles=self.obstacles_list)):
                arcade.draw_line(
                    enemyAI.center_x,
                    enemyAI.center_y,
                    self.player.center_x,
                    self.player.center_y,
                    color=colors.RED_DEVIL if enemyAI.player_is_facing() else colors.CADMIUM_GREEN,
                    line_width=1
                )

        arcade.draw_rectangle_filled(
            center_x=CENTER_X, center_y=SCREEN_HEIGHT-30, width=200, height=60, color=colors.GRAY_ASPARAGUS)
        arcade.draw_text(f"Score: {self.score}", start_x=CENTER_X-100, start_y=SCREEN_HEIGHT -
                         30, font_size=20, align="center", color=colors.WHITE_SMOKE, width=200)
        arcade.draw_text(
            f"AMMO: " + "▕" +"▓"*self.player.ammo_left + "░"*(self.player.magazine_size-self.player.ammo_left) + '▏' 
                + f" {self.player.ammo_left}/{self.player.magazine_size}",
            start_x=SCREEN_WIDTH-400, start_y=30, 
            font_size=16, align="left", color=colors.VEGAS_GOLD, width=200
        )  
        if self.player.reloading:
            arcade.draw_text(
                "RELOADING...",
                start_x=SCREEN_WIDTH-300, start_y=60, 
                font_size=16, align="left", color=colors.VEGAS_GOLD, width=200
            )    
        arcade.draw_text(
            f"HEALTH: " + "▕" +"▓"*math.ceil((self.player.hp/self.player.max_hp)*20) 
                + "░"*math.ceil((1.0-(self.player.hp/self.player.max_hp))*20) + '▏' 
                + f" {self.player.hp}/{self.player.max_hp}",
            start_x=50, start_y=30, 
            font_size=16, align="left", 
            color=(colors.GREEN if (self.player.hp/self.player.max_hp > 0.5) else colors.FALU_RED), width=400
        )   


# Main code entry point
if __name__ == "__main__":
    app = ColdpointSeattle()
    arcade.run()
