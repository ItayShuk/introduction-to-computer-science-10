

class Asteroid:
    def __init__(self,x_speed,x_location,y_speed,y_location,size):
        self.__x_speed = x_speed
        self.__x_location = x_location
        self.__y_speed=y_speed
        self.__y_location=y_location
        self.__size = size

    def has_intersection(self, obj):
        distance = ((self.get_location_x()-obj.get_location_x())**2+
                            (self.get_location_y()-obj.get_location_y())**2)**0.5
        return distance<=self.get_radius()+obj.get_radius()

    def get_radius(self):
        return self.get_size()*10-5

    def get_location_x (self):
        return self.__x_location

    def get_location_y (self):
        return self.__y_location

    def get_speed_x (self):
        return self.__x_speed

    def get_speed_y (self):
        return self.__y_speed

    def get_size(self):
        return self.__size

    def update_ast_x_location(self, new_x_location):
        self.__x_location = new_x_location

    def update_ast_y_location(self, new_y_location):
        self.__y_location = new_y_location

    def update_ast_x_speed(self, new_x_speed):
        self.__x_speed = new_x_speed

    def update_ast_y_speed(self, new_y_speed):
        self.__y_speed = new_y_speed

    def update_ast_size(self, new_size):
        self.__size = new_size