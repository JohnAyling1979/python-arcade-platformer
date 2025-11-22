"""
Platformer Game

python -m arcade.examples.platform_tutorial.01_open_window
"""
import arcade
from pathlib import Path

current_dir = Path(__file__).parent

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Pyrio"

TILE_SCALING = .5
COIN_SCALING = .5

GRAVITY = 1.75
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 30

class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, vsync=True)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.wall_list = None
        self.coin_list = None

        self.camera = None

        self.score_text = None
        self.gui_camera = None
        self.score = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def setup(self):
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()

        self.player_texture = arcade.load_texture(current_dir / 'assets' / 'Player-4.png')
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 42
        self.player_sprite.center_y = 96

        self.gui_camera = arcade.Camera2D()
        self.score = 0
        self.score_text = arcade.Text(
            f"Score: {self.score}",
             x=WINDOW_WIDTH - 10,
             y=WINDOW_HEIGHT,
             color=arcade.csscolor.BLACK,
             font_size=16,
             align="right",
             anchor_x="right",
             anchor_y="top"
        )

        self.player_list.append(self.player_sprite)

        for x in range(0, 1281, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        self.camera = arcade.Camera2D()

        self.background_color = arcade.csscolor.AQUA

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.wall_list, gravity_constant=GRAVITY
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.ESCAPE:
            self.setup()

        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"

        self.camera.position = self.player_sprite.position


    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        self.camera.use()

        # Code to draw other things will go here
        # Code to draw other things will go here
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        self.gui_camera.use()
        self.score_text.draw()

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()