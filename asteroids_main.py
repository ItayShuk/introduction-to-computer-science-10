from screen import Screen
import sys
import random
import math
from asteroid import *
from ship import *
from torpedo import *

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.special_shot_lst = []
        self.asteroid_lst = []
        self.torpedo_lst = []
        self.__asteroid_amount = asteroids_amount
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__delta = self.__screen_max_y - self.__screen_min_x
        self.__points = 0
        self.__x = random.randint(self.__screen_min_x, self.__screen_max_x + 1)
        self.__y = random.randint(self.__screen_min_y, self.__screen_max_y + 1)
        self.__heading = 0
        self.__screen.draw_ship(self.__x, self.__y, self.__heading)
        self.__ship = Ship(self.__x, 0, self.__y, 0, 0)
        self.adding_asteroid(asteroids_amount, 0)

    def adding_asteroid(self, num_of_ast, i):
        if num_of_ast == 0:
            return
        x = random.randint(self.__screen_min_x, self.__screen_max_x + 1)
        y = random.randint(self.__screen_min_x, self.__screen_max_x + 1)
        while x == self.__ship.get_location_x():
            x = random.randint(self.__screen_min_x, self.__screen_max_x + 1)
        while y == self.__ship.get_location_y():
            y = random.randint(self.__screen_min_x, self.__screen_max_x + 1)
        x_speed, y_speed = [random.randint(1, 5), random.randint(1, 5)]
        self.asteroid_lst.append(Asteroid(x_speed, x, y_speed, y, 3))
        self.__screen.register_asteroid(self.asteroid_lst[i], 3)
        self.__screen.draw_asteroid(self.asteroid_lst[i], x, y)
        self.adding_asteroid(num_of_ast - 1, i + 1)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.__ship.update_ship_direction(self.__ship.get_direction() + self.new_direction())
        self.update_speed()
        self.__ship.update_ship_x_location(self.new_location(self.__ship.get_location_x(), self.__ship.get_speed_x()))
        self.__ship.update_ship_y_location(self.new_location(self.__ship.get_location_y(), self.__ship.get_speed_y()))
        self.asteroid_updating()
        self.__screen.draw_ship(self.__ship.get_location_x(), self.__ship.get_location_y(), self.__ship.get_direction())
        self.torpedo_update()
        self.torpedo_shooting()
        self.teleportation()
        self.special_shot()
        self.special_shot_colision()
        if self.__screen.should_end() :
            self.__screen.show_message("Exit","You wanted to exit you fool!")
            self.__screen.end_game()
            sys.exit()
        if len(self.asteroid_lst) == 0:
            self.__screen.show_message("Win","You finished the game you fool!")
            self.__screen.end_game()
            sys.exit()


    def special_shot(self):
        if self.__screen.is_special_pressed() and len(self.special_shot_lst)<5:
            x_speed = self.__ship.get_speed_x() + 2 * math.cos((self.__ship.get_direction() * math.pi) / 180)
            y_speed = self.__ship.get_speed_y() + 2 * math.sin((self.__ship.get_direction() * math.pi) / 180)
            self.special_shot_lst.append(
                [(Torpedo(x_speed, self.__ship.get_location_x(), y_speed, self.__ship.get_location_y(),
                          self.__ship.get_direction())), 0])
            self.__screen.register_torpedo(self.torpedo_lst[len(self.special_shot_lst) - 1][0])


    def special_shot_colision(self):
        for sp in self.special_shot_lst:
            return     ######################needs to finish



    def teleportation(self):
        if self.__screen.is_teleport_pressed():
            x_astr_loc_list = self.x_list_creator()
            y_astr_loc_list = self.y_list_creator()
            x_random = random.randint(self.__screen_min_x,self.__screen_max_x+1)
            y_random = random.randint(self.__screen_min_x,self.__screen_max_x+1)
            while x_random in x_astr_loc_list:
                x_random = random.randint(self.__screen_min_x,self.__screen_max_x+1)
            while y_random in y_astr_loc_list:
                y_random = random.randint(self.__screen_min_x,self.__screen_max_x+1)
            self.__ship.update_ship_x_location(x_random)
            self.__ship.update_ship_y_location(y_random)


    def x_list_creator(self):
        lst = []
        for asteroid in self.asteroid_lst:
            lst.append(asteroid.get_location_x())
        return lst

    def y_list_creator(self):
        lst = []
        for asteroid in self.asteroid_lst:
            lst.append(asteroid.get_location_y())
        return lst



    def torpedo_update(self):
        if self.__screen.is_space_pressed() and len(self.torpedo_lst) < 10:
            x_speed = self.__ship.get_speed_x() + 2 * math.cos((self.__ship.get_direction() * math.pi) / 180)
            y_speed = self.__ship.get_speed_y() + 2 * math.sin((self.__ship.get_direction() * math.pi) / 180)
            self.torpedo_lst.append(
                [(Torpedo(x_speed, self.__ship.get_location_x(), y_speed, self.__ship.get_location_y(),
                          self.__ship.get_direction())), 0])
            self.__screen.register_torpedo(self.torpedo_lst[len(self.torpedo_lst) - 1][0])


    def torpedo_shooting(self):
        for torpedo in self.torpedo_lst:
            torpedo[0].update_torp_x_location(self.new_location(torpedo[0].get_location_x(), torpedo[0].get_speed_x()))
            torpedo[0].update_torp_y_location(self.new_location(torpedo[0].get_location_y(), torpedo[0].get_speed_y()))
            self.__screen.draw_torpedo(torpedo[0], torpedo[0].get_location_x(), torpedo[0].get_location_y(),
                                       torpedo[0].get_direction())
            torpedo[1] += 1
            if torpedo[1] == 200:
                self.__screen.unregister_torpedo(torpedo[0])
                self.torpedo_lst.remove(torpedo)

    def new_location(self, old_loc, speed):
        return ((speed + old_loc - self.__screen_min_x) % self.__delta + self.__screen_min_x)

    def new_direction(self):
        direction = 0
        if self.__screen.is_right_pressed():
            direction -= 7
        elif self.__screen.is_left_pressed():
            direction += 7
        return direction

    def update_speed(self):
        if self.__screen.is_up_pressed():
            self.__ship.update_ship_x_speed(
                self.__ship.get_speed_x() + math.cos(((self.__ship.get_direction()) * math.pi) / 180))
            self.__ship.update_ship_y_speed(
                self.__ship.get_speed_y() + math.sin(((self.__ship.get_direction()) * math.pi) / 180))

    def asteroid_updating(self):
        for asteroid in self.asteroid_lst:
            asteroid.update_ast_x_location(self.new_location(asteroid.get_location_x(), asteroid.get_speed_x()))
            asteroid.update_ast_y_location(self.new_location(asteroid.get_location_y(), asteroid.get_speed_y()))
            self.__screen.draw_asteroid(asteroid, asteroid.get_location_x(), asteroid.get_location_y())
            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message("Collision", "Watch out you fool!")
                self.__ship.remove_a_life()
                if self.__ship.get_lives() == 0:
                    self.__screen.show_message("Lose","You lost you fool!")
                    self.__screen.end_game()
                    sys.exit()
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                self.asteroid_lst.remove(asteroid)
            else:
                for torpedo in self.torpedo_lst:
                    if asteroid.has_intersection(torpedo[0]):
                        if asteroid.get_size() == 3:
                            self.__points += 20
                        if asteroid.get_size() == 2:
                            self.__points += 50
                        if asteroid.get_size() == 1:
                            self.__points += 100
                        if asteroid.get_size() > 1:
                            new_speed_x1 = ((torpedo[0].get_speed_x() + asteroid.get_speed_x()) / (
                                        (asteroid.get_speed_x() ** 2 +
                                         asteroid.get_speed_y() ** 2) ** 0.5))
                            new_speed_x2 = ((torpedo[0].get_speed_x() + asteroid.get_speed_x() * -1) / (
                                        (asteroid.get_speed_x() ** 2 +
                                         asteroid.get_speed_y() ** 2) ** 0.5))
                            new_speed_y1 = ((torpedo[0].get_speed_y() + asteroid.get_speed_y()) / (
                                        (asteroid.get_speed_x() ** 2 +
                                         asteroid.get_speed_y() ** 2) ** 0.5))
                            new_speed_y2 = ((torpedo[0].get_speed_y() + asteroid.get_speed_y() * -1) / (
                                        (asteroid.get_speed_x() ** 2 +
                                         asteroid.get_speed_y() ** 2) ** 0.5))
                            self.asteroid_lst.append(Asteroid(new_speed_x1, asteroid.get_location_x(), new_speed_y1,
                                                              asteroid.get_location_y(), asteroid.get_size() - 1))
                            self.asteroid_lst.append(Asteroid(new_speed_x2, asteroid.get_location_x(), new_speed_y2,
                                                              asteroid.get_location_y(), asteroid.get_size() - 1))
                            self.__screen.register_asteroid(self.asteroid_lst[len(self.asteroid_lst) - 2],
                                                            self.asteroid_lst[len(self.asteroid_lst) - 2].get_size())
                            self.__screen.register_asteroid(self.asteroid_lst[len(self.asteroid_lst) - 1],
                                                            self.asteroid_lst[len(self.asteroid_lst) - 1].get_size())
                        self.__screen.unregister_asteroid(asteroid)
                        self.__screen.unregister_torpedo(torpedo[0])
                        self.torpedo_lst.remove(torpedo)
                        self.asteroid_lst.remove(asteroid)
                        self.__screen.set_score(self.__points)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
