import arcade

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Платформер"
CHARACTER_SCALING = 1
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 15

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Инициализация игровых объектов
        self.player_list = None
        self.platform_list = None

        # Игрок
        self.player_sprite = None

        # Физика
        self.physics_engine = None

        # Камера
        self.camera = None

    def setup(self):
        # Инициализация игровых объектов
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()

        # Создание игрока
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 100
        self.player_list.append(self.player_sprite)

        # Создание платформ
        platform = arcade.Sprite(":resources:images/tiles/grassMid.png", CHARACTER_SCALING)
        platform.center_x = 400
        platform.center_y = 50
        self.platform_list.append(platform)

        # Инициализация физического движка
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.platform_list, gravity_constant=GRAVITY
        )

        # Инициализация камеры
        self.camera = arcade.camera(self.width, self.height)

    def on_draw(self):
        # Очистка экрана и начало отрисовки
        arcade.start_render()

        # Отрисовка игровых объектов
        self.player_list.draw()
        self.platform_list.draw()

    def on_update(self, delta_time):
        # Обновление физики
        self.physics_engine.update()

        # Перемещение камеры за игроком
        self.center_camera_to_player()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Ограничение камеры, чтобы она не выходила за пределы карты
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

    def on_key_press(self, key, modifiers):
        # Обработка нажатия клавиш
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        # Обработка отпускания клавиш
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()