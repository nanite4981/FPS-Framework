# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Shooter"
SCALING = 2.0

class Sprite(arcade.Sprite):
    def update(self):
        super().update()
        if self.right < 0:
            self.remove_from_sprite_lists()

class shooter(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.enemies_list = arcade.SpriteList()
        self.civilians_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player = arcade.Sprite("images/wizard.png", SCALING)
        self.player.height = 100
        self.player.width = 100
        self.player.center_y = self.height / 1.5
        self.player.center_x = self.width / 2
        self.all_sprites.append(self.player)

        arcade.schedule(self.add_enemy, 5.0)
        arcade.schedule(self.add_civilian, 10.0)

        self.background_music = arcade.load_sound("sounds/Apoxode_-_Electric_1.wav")

        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")
        self.strike_sound = arcade.load_sound("sounds/strike.wav")
        self.saved_sound = arcade.load_sound("sounds/thanks.mp3")

        arcade.play_sound(self.background_music)

        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    def add_enemy(self, delta_time: float):
        enemy = Sprite("images/zombie.png", SCALING)
        enemy.height = 50
        enemy.width = 50
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        enemy.velocity = (random.randint(-20, -5), 0)
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)
    def add_civilian(self, delta_time: float):
        civilian = Sprite("images/peasant.png", SCALING)
        civilian.height = 50
        civilian.width = 50
        civilian.left = random.randint(self.width, self.width + 80)
        civilian.top = random.randint(10, self.height - 10)
        civilian.velocity = (random.randint(-5, -2), 0)
        self.civilians_list.append(civilian)
        self.all_sprites.append(civilian)
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.close_window()
        if symbol == arcade.key.P:
            self.paused = not self.paused
        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 250
            arcade.play_sound(self.move_up_sound)
        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -250
            arcade.play_sound(self.move_down_sound)
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -250
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 250

    def on_key_release(self, symbol: int, modifiers: int):
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0
        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        if self.collided:
            self.collision_timer += delta_time
            # If we've paused for two seconds, we can quit
            if self.collision_timer > 2.0:
                arcade.close_window()
            # Stop updating things as well
            return
        
        if self.paused:
            return
        
        if self.player.collides_with_list(self.enemies_list):
            self.collided = True
            self.collision_timer = 0.0
            arcade.play_sound(self.collision_sound)
        for civilian in self.civilians_list:
            rescue_list = arcade.check_for_collision_with_list(self.player, self.civilians_list)
            if len(rescue_list) > 0:
                arcade.play_sound(self.saved_sound)
                civilian.remove_from_sprite_lists()

        for sprite in self.all_sprites:
            sprite.center_x = int(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(sprite.center_y + sprite.change_y * delta_time)

        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0
    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
    def on_mouse_press(self, x, y, button, modifiers):
        for enemy in self.enemies_list:
            if enemy.center_x - 10 <= x <= enemy.center_x + 10 and enemy.center_y - 10 <= y <= enemy.center_y + 10:
                arcade.play_sound(self.strike_sound)
                enemy.remove_from_sprite_lists()

if __name__ == "__main__":
    # Create a new Space Shooter window
    space_game = shooter(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    # Setup to play
    space_game.setup()
    # Run the game
    arcade.run()