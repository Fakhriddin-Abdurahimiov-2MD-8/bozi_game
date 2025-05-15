import arcade
import random
import os

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "BOZI"

PLAYER_SCALING = 1
COIN_SCALING = 2.5
OBSTACLE_SCALING = 1.6
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5
JUMP_SPEED = 10

COIN_COUNT = 10
OBSTACLE_COUNT = 5

# Состояния игры
MENU = 0
GAME = 1
GAME_OVER = 2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("player.png", PLAYER_SCALING)
        self.center_x = 100
        self.center_y = 100
        self.change_y = 0
        self.is_jumping = False
        self.jump_animation_timer = 0
        self.jump_texture = arcade.load_texture("player1.png")
        self.normal_texture = arcade.load_texture("player.png")

    def update(self, delta_time: float = 1 / 60):
        self.center_y += self.change_y
        self.change_y -= GRAVITY

        if self.is_jumping:
            self.jump_animation_timer += delta_time
            if self.jump_animation_timer >= 0.1:
                self.texture = self.normal_texture
                self.is_jumping = False
                self.jump_animation_timer = 0

        if self.center_y < 0:
            self.center_y = 0
            self.change_y = 0
        elif self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
            self.change_y = 0

    def jump(self):
        self.change_y = JUMP_SPEED
        self.is_jumping = True
        self.texture = self.jump_texture


class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__("coin1.png", COIN_SCALING)
        self.textures = [arcade.load_texture(f"coin{i + 1}.png") for i in range(3)]
        self.current_texture = 0
        self.texture = self.textures[0]
        self.animation_speed = 0.1
        self.time_since_last_frame = 0
        self.reset()

    def update(self, delta_time: float = 1 / 60):
        self.center_x -= 2 * (delta_time * 60)

        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.animation_speed:
            self.current_texture = (self.current_texture + 1) % len(self.textures)
            self.texture = self.textures[self.current_texture]
            self.time_since_last_frame = 0

        if self.right < 0:
            self.reset()

    def reset(self):
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT)


class Obstacle(arcade.Sprite):
    def __init__(self):
        super().__init__("obstacle.png", OBSTACLE_SCALING)
        self.reset()

    def update(self, delta_time: float = 1 / 60):
        self.center_x -= 2 * (delta_time * 60)
        if self.right < 0:
            self.reset()

    def reset(self):
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT // 2)
        self.height = random.randint(50, 150)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.coin_list = None
        self.obstacle_list = None

        # Звуковые эффекты
        self.background_music = None
        self.coin_sound = None
        self.crash_sound = None
        self.music_player = None
        self.music_playing = False

        self.player_sprite = None
        self.score = 0
        self.high_score = 0
        self.game_time = 0
        self.game_state = MENU
        self.blink_timer = 0

        self.background_layers = []
        self.background_speed = [0.5, 1.0, 1.5]

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        # Параллакс-фон
        self.background_layers = []
        for i in range(3):
            layer = arcade.SpriteList()
            for j in range(2):
                bg = arcade.Sprite(f"background_layer_{i + 1}.png")
                bg.scale = SCREEN_HEIGHT / bg.height
                bg.left = SCREEN_WIDTH * j
                bg.center_y = SCREEN_HEIGHT // 2
                layer.append(bg)
            self.background_layers.append(layer)

        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        for _ in range(COIN_COUNT):
            self.coin_list.append(Coin())
        for _ in range(OBSTACLE_COUNT):
            self.obstacle_list.append(Obstacle())

        self.score = 0
        self.game_time = 0
        self.blink_timer = 0

        # Загрузка звуков
        self.load_sounds()

        self._init_text()

    def load_sounds(self):
        """Загрузка всех звуковых файлов"""
        try:
            # Полные пути к файлам
            base_path = os.path.dirname(os.path.abspath(__file__))
            bg_path = os.path.join(base_path, "bg_music.mp3")
            coin_path = os.path.join(base_path, "coin_gain.mp3")
            crash_path = os.path.join(base_path, "crash.mp3")

            self.background_music = arcade.Sound(bg_path)
            self.coin_sound = arcade.Sound(coin_path)
            self.crash_sound = arcade.Sound(crash_path)
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")

    def play_background_music(self):
        """Запуск фоновой музыки"""
        if self.background_music and not self.music_playing:
            try:
                self.music_player = self.background_music.play(loop=True)
                self.music_playing = True
            except Exception as e:
                print(f"Ошибка воспроизведения музыки: {e}")

    def stop_background_music(self):
        """Остановка фоновой музыки"""
        if self.music_playing and self.music_player:
            try:
                self.music_player.pause()
                self.music_playing = False
            except Exception as e:
                print(f"Ошибка остановки музыки: {e}")

    def _init_text(self):
        self.score_text = arcade.Text(
            f"{self.score} Монет", 10, SCREEN_HEIGHT - 30,
            arcade.color.YELLOW, 18, font_name="Pixelify Sans")
        self.time_text = arcade.Text(
            "0 с", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 18, font_name="Pixelify Sans")
        self.menu_text = arcade.Text(
            "Нажмите SPACE для старта", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            arcade.color.WHITE, 30, anchor_x="center", anchor_y="center",
            align="center", font_name="Pixelify Sans")
        self.high_score_text = arcade.Text(
            f"Рекорд: {self.high_score} Монет", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
            arcade.color.YELLOW, 24, anchor_x="center", anchor_y="center",
            font_name="Pixelify Sans")
        self.game_over_title = arcade.Text(
            "Игра окончена", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            arcade.color.RED_DEVIL, 40, anchor_x="center", anchor_y="center",
            font_name="Pixelify Sans")
        self.game_over_instruction = arcade.Text(
            "Нажмите SPACE для рестарта", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE, 30, anchor_x="center", anchor_y="center",
            font_name="Pixelify Sans")

    def update_background(self):
        for i, layer in enumerate(self.background_layers):
            for sprite in layer:
                sprite.center_x -= self.background_speed[i]

            first, second = layer[0], layer[1]
            if first.right < 0:
                first.left = second.right
            elif second.right < 0:
                second.left = first.right

    def on_draw(self):
        self.clear()

        for layer in self.background_layers:
            layer.draw()

        if self.game_state == MENU:
            self.menu_text.draw()
            self.high_score_text.draw()
        elif self.game_state == GAME:
            self.player_list.draw()
            self.coin_list.draw()
            self.obstacle_list.draw()
            self.score_text.draw()
            self.time_text.draw()
        elif self.game_state == GAME_OVER:
            self.game_over_title.draw()
            self.game_over_instruction.draw()
            self.high_score_text.draw()

    def on_update(self, delta_time: float):
        if self.game_state == GAME_OVER:
            self.blink_timer += delta_time
            if self.blink_timer > 0.5:
                self.game_over_instruction.visible = not self.game_over_instruction.visible
                self.blink_timer = 0
            return

        if self.game_state != GAME:
            return

        self.update_background()
        self.player_list.update(delta_time)
        self.coin_list.update(delta_time)
        self.obstacle_list.update(delta_time)

        self.game_time += delta_time
        self.time_text.text = f"{int(self.game_time)} с"

        coin_hits = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hits:
            coin.reset()
            self.score += 1
            self.score_text.text = f"{self.score} Монет"
            if self.coin_sound:
                self.coin_sound.play(volume=0.5)  # Звук сбора монеты
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_text.text = f"Рекорд: {self.high_score} Монет"

        if arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list):
            self.game_state = GAME_OVER
            self.game_over_instruction.visible = True
            self.stop_background_music()
            if self.crash_sound:
                self.crash_sound.play(volume=0.7)  # Звук столкновения

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == MENU or self.game_state == GAME_OVER:
                self.game_state = GAME
                self.setup()
                self.play_background_music()
            elif self.game_state == GAME:
                self.player_sprite.jump()
        elif (key == arcade.key.UP or key == arcade.key.W) and self.game_state == GAME:
            self.player_sprite.jump()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.game_state == GAME:
            self.player_sprite.jump()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()