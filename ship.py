

class Ship:

    def __init__(self,x_location,x_speed,y_location,y_speed,direction):
        self.lives =4
        self.radius= 1
        self.__x_speed = x_speed
        self.__x_location = x_location
        self.__y_speed=y_speed
        self.__y_location=y_location
        self.__direction = direction


    def remove_a_life(self):
        self.lives-=1

    def get_lives(self):
        return self.lives


    def get_location_x (self):
        return self.__x_location

    def get_radius(self):
        return self.radius

    def get_location_y (self):
        return self.__y_location

    def get_speed_x (self):
        return self.__x_speed

    def get_speed_y (self):
        return self.__y_speed

    def get_direction(self):
        return self.__direction

    def update_ship_x_location(self, new_x_location):
        self.__x_location = new_x_location

    def update_ship_y_location(self, new_y_location):
        self.__y_location = new_y_location

    def update_ship_x_speed(self, new_x_speed):
        self.__x_speed = new_x_speed

    def update_ship_y_speed(self, new_y_speed):
        self.__y_speed = new_y_speed

    def update_ship_direction(self, new_direction):
        self.__direction = new_direction