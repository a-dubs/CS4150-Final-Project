from modular_ai import *
from constants import *


class SpriteAI(arcade.Sprite):
    def __init__(self, hp:float, speed:float, filename: str = None, scale: float = 1, image_x: float = 0, image_y: float = 0, image_width: float = 0, image_height: float = 0, center_x: float = 0, center_y: float = 0, repeat_count_x: int = 1, repeat_count_y: int = 1, flipped_horizontally: bool = False, flipped_vertically: bool = False, flipped_diagonally: bool = False, hit_box_algorithm: Optional[str] = "Simple", hit_box_detail: float = 4.5, texture: Texture = None, angle: float = 0):
        super().__init__(filename, scale, image_x, image_y, image_width, image_height, center_x, center_y, repeat_count_x, repeat_count_y, flipped_horizontally, flipped_vertically, flipped_diagonally, hit_box_algorithm, hit_box_detail, texture, angle)

        self.options = []
        self.hp = hp
        self.speed = speed
        self.magazine_size = 10
        self.ammo_left = 10
        self.cover = None
        self.player = arcade.Sprite()
        self.enemies_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles_list = arcade.SpriteList()

        self.dead = False


    def update(self):
        super().update()

    def take_damage(self, damage: int):
        self.hp -= damage
        # if self.hp <= 0:
        #     self.kill()
        #     self.
        

    def add_option(self, option: Option) -> None:
        self.options.append(option)

    # def update(self, dt: float) -> None:
        # update all considerations for all options
        # for option in self.options:
        #     for consideration in option.considerations:
        #         consideration.update(dt)

    def tick(self, dt: float) -> None:
        # choose option
        # option = choose(self.options)
        # perform action
        # if option is not None:
            # action = option.action
            # getattr(action.target, action.action)(*action.args)
            # getattr(self.sprite, action.action)(*action.args)
        # reset all considerations for all options
        # for option in self.options:
        #     for consideration in option.considerations:
        #         consideration.reset()

        if (best_obs := find_closest_obs(self, self.obstacles_list)):
            best_spot = find_cover_spots_on_obs(hider=self,hiding_from=self.player,obstacle=best_obs)
            self.move_to_pos(best_spot)

    def update_game_state(self, player:Sprite, enemies_list: SpriteList, obstacles_list: SpriteList, projectiles_list: SpriteList) -> None:
        self.player = player
        self.enemies_list = enemies_list
        self.obstacles_list = obstacles_list
        self.projectiles_list = projectiles_list    

    # def choose_cover(self, obstacles: arcade.SpriteList) -> None:

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

    def peek(self) -> None:
        self.move_to_pos(self.position)

    def shoot(self):
        bullet = SpriteCircle(ENEMY_BULLET_RADIUS, color=ENEMY_BULLET_COLOR)
        # bullet.center_x = sprite.center_x + sprite.width * 0.65 * cos(sprite.radians+pi*0.44)
        # bullet.center_y = sprite.center_y + sprite.height * 0.65 * sin(sprite.radians+pi*0.44)
        bullet.center_x = self.center_x + \
            self.width * 0.7 * cos(self.radians+0.5*pi)
        bullet.center_y = self.center_y + \
            self.height * 0.7 * sin(self.radians+0.5*pi)
        # bullet.face_point((self._mouse_x,self._mouse_y))
        spread = 10  # in degrees, cone of innaccuracy
        bullet.radians = self.radians + 0.5 * pi + (pi*spread*(random()-0.5)/180)

        bullet.change_x = BULLET_SPEED * cos(bullet.radians)
        bullet.change_y = BULLET_SPEED * sin(bullet.radians)
        # bullet.forward(10)
        self.projectiles_list.append(bullet)
        # bullet.color


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

def find_cover_spots_on_obs(hider: Sprite, hiding_from: Sprite, obstacle: Sprite):
    hider_size = max(hider.width, hider.height)
    padding = 10
    positions = [(obstacle.center_x + x_dir * (padding + obstacle.width*0.5 + hider_size*0.5),
        obstacle.center_y + y_dir * (padding + obstacle.height*0.5 + hider_size*0.5))
        for y_dir in (-1, 0, 1) for x_dir in (-1, 0, 1) if not (x_dir == 0 and y_dir == 0)]
    cover_spots = [pos for pos in positions if is_hidden_at_pos(pos,hiding_from.position,obstacle)]
    # print(len(cover_spots), "cover spots found!")
    for pos in cover_spots:
        arcade.draw_point(pos[0],pos[1],colors.BLACK,3)
    distances = {cp:dist(cp,hiding_from.position) for cp in cover_spots}
    min_dist = min(list(distances.values()))
    return [pos for pos in distances if distances[pos] == min_dist][0]

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