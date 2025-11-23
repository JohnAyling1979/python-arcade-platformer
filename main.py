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

        self.scene = None

        self.camera = None
        self.gui_camera = None

        self.score = 0
        self.score_text = None

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def setup(self):
        self.scene = arcade.Scene()

        self.player_texture = arcade.load_texture(current_dir / 'assets' / 'Player-4.png')
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = 42
        self.player_sprite.center_y = 96
        self.scene.add_sprite("Player", self.player_sprite)

        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )

        self.camera = arcade.Camera2D()
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

        self.background_color = arcade.csscolor.AQUA

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.camera.use()

        self.scene.draw()

        self.gui_camera.use()

        self.score_text.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"

        self.camera.position = self.player_sprite.position

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

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()