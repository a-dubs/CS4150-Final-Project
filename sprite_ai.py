from modular_ai import *
from constants import *


class Person(arcade.Sprite):
    def __init__(self, hp:float, speed:float, magazine_size=10, reload_time=2.0,  fire_speed=3.0, is_player=False, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)

        self.is_player = is_player
        self.reload_time = 2
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.fire_speed = fire_speed
        self.reload_time = reload_time
        self.magazine_size = magazine_size
        self.ammo_left = self.magazine_size
        self.dead = False
        self.current_action = None
        self.action_history : list[str] = []
        self.enemies_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles_list = arcade.SpriteList()
        self.shooting_cooldown = 0
        self.reloading = False

    def take_damage(self, damage: int):
        self.hp -= damage

    # returns true if already at 
    def move_to_pos(self, target_pos:tuple[float,float]) -> bool:
        if (dist_btwn:=dist(self.position,target_pos)) == 0:
            self.change_x = 0
            self.change_y = 0
            return True
        target_dir = norm_vect_btwn(self.position,target_pos)
        target_velocity_vect = target_dir*min(dist_btwn,self.speed)
        self.change_x = target_velocity_vect[0]
        self.change_y = target_velocity_vect[1]
        return False
    
    def shoot(self) -> None:
        if self.can_shoot():
            if self.is_player:
                bullet = SpriteCircle(FRIENDLY_BULLET_RADIUS, color=FRIENDLY_BULLET_COLOR)
                bullet.center_x = self.center_x + \
                    self.width * 0.7 * cos(self.radians+0.5*pi)
                bullet.center_y = self.center_y + \
                    self.height * 0.7 * sin(self.radians+0.5*pi)
                spread = 10  # in degrees, cone of innaccuracy
                bullet.radians = self.radians + 0.5 * pi + (pi*spread*(random()-0.5)/180)
                bullet.change_x = BULLET_SPEED * cos(bullet.radians)
                bullet.change_y = BULLET_SPEED * sin(bullet.radians)
            
            else:
                bullet = SpriteCircle(ENEMY_BULLET_RADIUS, color=ENEMY_BULLET_COLOR)
                bullet.center_x = self.center_x + \
                    self.width * 0.7 * cos(self.radians+0.5*pi)
                bullet.center_y = self.center_y + \
                    self.height * 0.7 * sin(self.radians+0.5*pi)
                spread = 10  # in degrees, cone of innaccuracy
                bullet.radians = self.radians + 0.5 * pi + (pi*spread*(random()-0.5)/180)
                bullet.change_x = BULLET_SPEED * cos(bullet.radians)
                bullet.change_y = BULLET_SPEED * sin(bullet.radians)
        
            self.projectiles_list.append(bullet)
            self.ammo_left -= 1
            self.shooting_cooldown = 1/self.fire_speed


    def update_game_state(self, player:Sprite, enemies_list: SpriteList, obstacles_list: SpriteList, projectiles_list: SpriteList) -> None:
        self.enemies_list = enemies_list
        self.obstacles_list = obstacles_list
        self.projectiles_list = projectiles_list  

    def can_shoot(self) -> bool:
        return self.ammo_left > 0 and self.shooting_cooldown <= 0

    def reload(self) -> None:
        # self.ammo_left = self.magazine_size
        self.shooting_cooldown = self.reload_time
        self.reloading = True

    def tick(self, dt: float) -> None:
        self.shooting_cooldown -= dt
        if self.reloading == True and self.shooting_cooldown <= 0:
            self.reloading = False
            self.ammo_left = self.magazine_size
        # if self.ammo_left <= 0:
        #     self.reload()



class SpriteAI(Person):
    def __init__(self, hp:float, speed:float, magazine_size=10, reload_time=2.0,  fire_speed=2.0, is_player=False, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
        
        # init super
        super().__init__(hp, speed, magazine_size, reload_time, fire_speed, is_player, filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)

        self.options : list[Option]= []
        self.hp = hp
        self.speed = speed
        self.fire_speed = fire_speed
        self.reload_time = reload_time
        self.magazine_size = magazine_size
        self.ammo_left = self.magazine_size
        self.target_pos = None
        self.player : Person = None
        self.enemies_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles_list = arcade.SpriteList()

        self.dead = False
        self.queued_actions : list[str] = [] 
        # self.current_action = None
        self.action_history : list[str] = []

    def add_option(self, option: Option) -> None:
        self.options.append(option)


    # def update(self, dt: float) -> None:
        # update all considerations for all options
        # for option in self.options:
        #     for consideration in option.considerations:
        #         consideration.update(dt)

    def tick(self, dt: float) -> None:
        super().tick(dt)

        # print(self.current_action)
        # if self.current_action == None:
        #     if len(self.action_history) == 0 or self.action_history[-1] == "shooting":
        #         if (best_obs := find_closest_obs(self, self.obstacles_list)):
        #             print("hiding!")
        #             self.target_pos = get_target_cover_pos(hider=self,hiding_from=self.player,obstacle=best_obs)
        #             self.current_action = "hiding"
        #             self.move_to_pos(self.target_pos)
        #     elif len(self.action_history) > 0 and self.action_history[-1] == "hiding":
        #         if (best_obs := find_closest_obs(self, self.obstacles_list)):
        #             print("peeking!")
        #             self.target_pos = get_best_peek_pos(self,target=self.player,obstacle=best_obs)
        #             self.current_action = "peeking"
        #             self.move_to_pos(self.target_pos)
        #     elif len(self.action_history) > 0 and self.action_history[-1] == "peeking":
        #         self.current_action = "shooting"
        #         print("shooting!")
        # else:
        #     if self.current_action == "shooting":
        #         self.face_point(self.player.position)
        #         if self.ammo_left > 0:
        #             self.shoot()
        #             self.action_history.append(self.current_action)
        #             self.current_action = None
        #     elif self.current_action == "hiding":
        #         self.target_pos = get_best_peek_pos(self,target=self.player,obstacle=best_obs)    
        #     elif self.current_action == "peeking":
        #         self.face_point(self.player.position)
        #         if (arrived:=self.move_to_pos(self.target_pos)):
        #             self.action_history.append(self.current_action)
        #             self.current_action = None
            # self.peek()
        self.face_point(self.player.position)
        for option in self.options:
            for consideration in option.considerations:
                consideration.update(dt)
        if len(self.queued_actions) == 0:
            selected_option = choose(self.options)
            if selected_option:
                actions = selected_option.actions
                for action in actions:
                    if action == "shoot" and self.can_shoot():
                        self.queued_actions.append(action)
        elif self.queued_actions[0] == "shoot" and self.can_shoot():
            self.shoot()
            self.queued_actions.pop(0)
        

        

    def update_game_state(self, player:Person, enemies_list: SpriteList, obstacles_list: SpriteList, projectiles_list: SpriteList) -> None:
        self.player = player
        self.enemies_list = enemies_list
        self.obstacles_list = obstacles_list
        self.projectiles_list = projectiles_list 

    # def choose_cover(self, obstacles: arcade.SpriteList) -> None:    
    def peek(self) -> None:
        self.move_to_pos(self.position)
    
    def player_is_facing(self) -> bool:
        return abs(self.player.angle + 180 - self.angle) < 20
    
    def line_of_sight(self) -> bool:
        return has_line_of_sight(self, self.player, self.obstacles_list)
    


####################################
### GENERALIZED HELPER FUNCTIONS ###
####################################

def is_hidden_at_pos(from_pos: tuple[float, float], to_pos: tuple[float, float], obstacle: Sprite):
    to_obs = np.array(from_pos) - np.array(obstacle.position)
    dist_to_obs = magnitude(to_obs)
    to_target = np.array(from_pos) - np.array(to_pos)
    dist_to_target = magnitude(to_target)
    to_target_norm = to_target/dist_to_target
    # print("dist to obs",dist_to_obs)
    # print("to_obs_norm", to_obs_norm)
    # print("to_target_norm", to_target_norm)
    return dist(to_target_norm * dist_to_obs, to_obs) < np.average([obstacle.width, obstacle.height])*0.5

def points_around_obstacle(hider: Sprite, obstacle: Sprite, padding=10):
    hider_size = max(hider.width, hider.height)
    positions = [(obstacle.center_x + x_dir * (padding + obstacle.width*0.5 + hider_size*0.5),
        obstacle.center_y + y_dir * (padding + obstacle.height*0.5 + hider_size*0.5))
        for y_dir in (-1, 0, 1) for x_dir in (-1, 0, 1) if not (x_dir == 0 and y_dir == 0)]
    return positions

def get_best_peek_pos(sprite: Sprite, target: Sprite, obstacle: Sprite) -> tuple[float,float]:
    positions = points_around_obstacle(sprite, obstacle, padding=15)
    peek_spots = [pos for pos in positions if not is_hidden_at_pos(pos,target.position,obstacle)]
    # print(len(cover_spots), "cover spots found!")
    # for pos in peek_spots:
        # arcade.draw_point(pos[0],pos[1],colors.BLACK,3)
    distances = {ps:dist(ps,target.position) for ps in peek_spots}
    min_dist = max(list(distances.values()))
    return [pos for pos in distances if distances[pos] == min_dist][0]

def get_target_cover_pos(hider: Sprite, hiding_from: Sprite, obstacle: Sprite):
    positions = points_around_obstacle(hider, obstacle)
    cover_spots = [pos for pos in positions if is_hidden_at_pos(pos,hiding_from.position,obstacle)]
    # print(len(cover_spots), "cover spots found!")
    # for pos in cover_spots:
        # arcade.draw_point(pos[0],pos[1],colors.BLACK,3)
    distances = {cp:dist(cp,hiding_from.position) for cp in cover_spots}
    min_dist = min(list(distances.values()))
    dest_pos = [pos for pos in distances if distances[pos] == min_dist][0]
    cover_spots.sort(key=lambda x: magnitude((dist(dest_pos,hider.position),dist(x,hider.position))))
    return cover_spots[0]

def find_closest_obs(sprite: Sprite, obstacles: arcade.SpriteList):
    min_dist = float("inf")
    best_cover = None
    for obs in obstacles:
        if (d := sprite_dist(obs, sprite)) < min_dist:
            best_cover = obs
            min_dist = d
    return best_cover

# check if viewer has line of sight to to_person
def has_line_of_sight(viewer: Sprite, target: Sprite, obstacles: SpriteList, simple=True) -> bool:
    # just do calculation center to center
    result = True
    if simple:
        for obs in obstacles:
            if is_hidden_at_pos(viewer.position, target.position, obs):
                result = False
                break
    return result