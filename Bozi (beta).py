import arcade
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "BOZI"

PLAYER_SCALING = 0.5
COIN_SCALING = 0.6
OBSTACLE_SCALING = 0.7
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5
JUMP_SPEED = 10

COIN_COUNT = 10
OBSTACLE_COUNT = 5



class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("player.png", PLAYER_SCALING)
        self.center_x = 100
        self.center_y = 100
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        # Применяем гравитацию
        self.center_y += self.change_y
        self.change_y -= GRAVITY

        if self.center_y < 0:
            self.center_y = 0
            self.change_y = 0
        elif self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
            self.change_y = 0


class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__("coin.png", COIN_SCALING)
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT)

    def update(self, delta_time: float = 1 / 60):
        self.center_x -= 2
        if self.center_x < 0:
            self.reset()

    def reset(self):
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT)


class Obstacle(arcade.Sprite):
    def __init__(self):
        super().__init__("obstacle.png", OBSTACLE_SCALING)
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT // 2)  # Препятствия на разной высоте
        self.height = random.randint(50, 150)  # Случайная высота препятствия

    def update(self, delta_time: float = 1 / 60):
        self.center_x -= 2
        if self.center_x < 0:
            self.reset()

    def reset(self):
        self.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.center_y = random.randint(0, SCREEN_HEIGHT // 2)  # Препятствия на разной высоте
        self.height = random.randint(50, 150)  # Случайная высота препятствия


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.coin_list = None
        self.obstacle_list = None

        self.player_sprite = None
        self.score = 0

        self.score_text = None  # Добавляем объект для текста

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        for i in range(COIN_COUNT):
            coin = Coin()
            self.coin_list.append(coin)

        for i in range(OBSTACLE_COUNT):
            obstacle = Obstacle()
            self.obstacle_list.append(obstacle)

        self.score = 0
        self.score_text = arcade.Text(
            f"{self.score} Монет",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.BLACK,
            15,
        )

    def on_draw(self):
        # Очищаем экран перед отрисовкой
        self.clear()

        # Отрисовываем спрайты
        self.player_list.draw()
        self.coin_list.draw()
        self.obstacle_list.draw()

        # Отрисовываем текст
        self.score_text.draw()

    def on_update(self, delta_time: float):
        self.player_list.update(delta_time)
        self.coin_list.update(delta_time)
        self.obstacle_list.update(delta_time)

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.reset()
            self.score += 1
            self.score_text.text = f"{self.score} Монет "  # Обновляем текст

        obstacle_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list)
        if obstacle_hit_list:
            self.setup()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key== arcade.key.UP:
            self.player_sprite.change_y  = JUMP_SPEED


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()