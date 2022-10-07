import pygame
import math
# test coment
run = True
go = True

window_x = 1000
window_y = 600
window = pygame.display.set_mode((window_x, window_y))
map_scale = 400
number_cube = 10
cube_size = 64
real_map_size = cube_size * number_cube
cube_length_on_map = int(map_scale / number_cube)
map_background_color = 47, 79, 79
grid_color = (30, 30, 30)
line_size = 50
wall_list = []
rey_list = []
rey_step = 2
FOV = 90
projection_plane = [320, 200]
center_p_p = projection_plane[0] / 2, projection_plane[1] / 2
distance_to_p_p = (projection_plane[0] / 2) / math.tan(FOV / 2)
high_wall = projection_plane[1]
ray_degree = FOV / projection_plane[0]
clock = pygame.time.Clock()
map_list = '''##########
#00##0000#
#000#0000#
#000###00#
#0#0000#0#
#0##00000#
#000#0#00#
#000#0#00#
#00000000#
##########'''


class Game:

    @classmethod
    def draw_minimap(cls):
        pygame.draw.rect(window, map_background_color, (window_x - map_scale, 0, map_scale, map_scale))  # фон
        count_x = 0
        count_y = 0

        for item in map_list:  # рисование стени
            if count_x > number_cube:
                count_x = 0
                count_y += 1
            if item == '#':
                pygame.draw.rect(window, (0, 0, 0), (count_x * cube_length_on_map + window_x - map_scale, count_y * cube_length_on_map, cube_length_on_map, cube_length_on_map))
                # wall_list.add([count_x, count_y])
                # wall_list.append(Wall(count_x, count_y, cube_size, (0, 0, 0)))
            count_x += 1

        # сетка
        for number in range(number_cube):
            # горизонтальние линии
            pygame.draw.line(window, grid_color, [window_x - map_scale, number * cube_length_on_map], [window_x, number * cube_length_on_map], 1)
            # вертикальние линии
            pygame.draw.line(window, grid_color, [window_x - map_scale + (number * cube_length_on_map), 0], [window_x - map_scale + (number * cube_length_on_map), map_scale], 1)

        # игрок на карте
        pos_player_on_map = (int(window_x - map_scale + (map_scale * player.x) / (cube_size * number_cube)), int((map_scale * player.y) / (cube_size * number_cube)))
        pygame.draw.circle(window, (0, 0, 30), pos_player_on_map, 2, 2)

        # линии обзора
        a = convert_degree_in_vector2(player.degree + (player.v_a / 2))
        b = convert_degree_in_vector2(player.degree - (player.v_a / 2))
        c = convert_degree_in_vector2(player.degree)
        a[0] *= line_size
        a[1] *= line_size
        b[0] *= line_size
        b[1] *= line_size
        c[0] *= line_size
        c[1] *= line_size
        end_line_a = int(pos_player_on_map[0] + a[0]), int(pos_player_on_map[1] + a[1])
        end_line_b = int(pos_player_on_map[0] + b[0]), int(pos_player_on_map[1] + b[1])
        end_line_c = int(pos_player_on_map[0] + c[0]), int(pos_player_on_map[1] + c[1])
        pygame.draw.line(window, (0, 0, 50), pos_player_on_map, end_line_a, 1)
        pygame.draw.line(window, (0, 0, 50), pos_player_on_map, end_line_b, 1)
        pygame.draw.line(window, (0, 0, 50), pos_player_on_map, end_line_c, 1)

        # ay = int(player.y / cube_size) * cube_size + 64
        # bx = int(player.x / cube_size) * cube_size
        # print(ay)

    @classmethod
    def draw_screen(cls, dis_list):
        for dis in enumerate(dis_list):
            if dis[1] != 0:
                high_wall_on_screen = cube_size / dis[1] * distance_to_p_p
                pygame.draw.line(window, (0, 0, 0), [projection_plane[0] - dis[0], projection_plane[1] / 2 - high_wall_on_screen], [projection_plane[0] - dis[0], projection_plane[1] / 2 + high_wall_on_screen])
class Player:
    def __init__(self, x, y, degree, viewing_angle):
        self.x = x
        self.y = y
        self.degree = degree
        self.direction = convert_degree_in_vector2(self.degree)
        self.v_a = viewing_angle

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    def rotate(self, degree):
        self.direction = convert_degree_in_vector2(self.degree + degree)
        self.degree += degree
        if self.degree >= 360:
            self.degree -= 360
        if self.degree < 0:
            self.degree += 360


class Wall:
    def __init__(self, x, y, width, color):
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def collision(self, x, y):
        # print(self.x, self.y, x / cube_size, y / cube_size)
        if self.y == y / cube_size or self.y + 1 == y / cube_size:
            if self.x <= x / cube_size <= self.x + 1:
                return True
        else:
            return False

# class Rey:
#     def __init__(self, st_x, st_y, deviation):
#         self.collision = False
#         self.active = False
#         self.deviation = deviation
#         self.distance = 0
#         self.degree = 0
#         self.x = 0
#         self.y = 0
#         self.st_x = st_x
#         self.st_y = st_y
#
#     def update(self, direct, wall_l):
#         if self.active:
#             self.x += (direct[0] * 4)
#             self.y += (direct[1] * 4)
#             #print('rey x = ' + str(self.x))
#             #print('rey x = ' + str(self.x))
#             #print(direct)
#             self.distance = distance(self.st_x, self.st_y, self.x, self.y)
#             if self.distance > 100:
#                 self.collision = False
#                 self.active = False
#                 self.x = 0
#                 self.y = 0
#                 #print('distance more 50')
#             for wall in wall_l:
#                 if wall.collision([self.x, self.y]):
#                     self.collision = True
#                     self.active = False
#                     #print('wall collision. distance = ' + str(distance(self.st_x, self.st_y, self.x, self.y)) + ' wall x, y = ' + str([wall.x, wall.y]))
#                     #self.x = 0
#                     #self.y = 0
#
#     def draw(self):
#         pygame.draw.line(window, (0, 0, 0), [self.st_x, self.st_y], [self.x, self.y], 1)


def convert_degree_in_vector(degree):
    return [math.sin((degree * math.pi) / 180), math.cos((degree * math.pi) / 180)]


def convert_degree_in_vector2(degree):
    x = math.cos((degree * math.pi) / 180)
    y = math.sin((degree * math.pi) / 180)
    return [x, -y]


def distance(obj_1_x, obj_1_y, obj_2_x, obj_2_y):
    dis = math.sqrt(((obj_2_x - obj_1_x) ** 2) + ((obj_2_y - obj_1_y) ** 2))
    #print('distance between ' + str([obj_1_x, obj_1_y, obj_2_x, obj_2_y]) + ' = ' + str(dis))
    return dis


def wall_collision_h(w_list, x, y):
    for wall in w_list:
        if wall[1] == y / cube_size or wall[1] + 1 == y / cube_size:
            if wall[0] <= x / cube_size <= wall[0] + 1:
                return True
    return False


def wall_collision_v(w_list, x, y):
    for wall in w_list:
        if wall[0] == x / cube_size or wall[0] + 1 == x / cube_size:
            if wall[1] <= y / cube_size <= wall[1] + 1:
                return True
    return False


def revers_degree(degree):
    if degree >= 360:
        return degree - 360
    if degree < 0:
        return degree + 360
    if degree == 0:
        return 0
    else:
        return  degree

def horizontal_rey(xp, yp, degree):
    temporarily_dis = 0
    """пускаем луч по горезонталям"""
    # print('пускаем луч по горезонталям')
    go = True

    #  ищем значение к которому потом будем прибавлять первое пересечение (ya, xa)
    #  и ищем самою первою точку пересечения по горизонтали  (ax, ay)
    # print('ищем ya, xa, ax, ay')
    if 0 < degree < 180:
        ay = int(yp / cube_size) * cube_size
        ya = - cube_size
    else:
        ay = int(yp / cube_size) * cube_size + 64
        ya = cube_size
    tangens_degree = math.tan((degree * math.pi) / 180)
    if tangens_degree != 0:
        if 0 < degree < 180:
            xa = cube_size / tangens_degree
        else:
            xa = - cube_size / tangens_degree
        ax = xp + (yp - ay) / tangens_degree
    else:
        xa = 0
        ax = 0
    # print('xa, ya = ' + str(xa) + ' ' + str(ya))
    # testy = int((map_scale * ay) / (cube_size * number_cube))
    # testx = int((window_x - map_scale) + (map_scale * ax) / (cube_size * number_cube))
    # if -1000 > testx or testx > 1000:
    #     testx = 1000
    # # print(testx, testy)
    # pygame.draw.circle(window, (255, 255, 255), [testx, testy], 3, 3)

    #  проверка на наличие стенки на первой точке
    # print('проверка на наличие стенки на первой точке')
    if wall_collision_h(wall_list, ax, ay):
        dis = distance(xp, yp, ax, ay)
        return ax, ay, dis
    # for wall in wall_list:
    #     if wall.collision(ax, ay):
    #         # print('colission' + str(ax) + ' ' + str(ay))
    #         go = False
    #         return distance(xp, yp, ax, ay)
    #  если на первой точке нету стенки то идем дальше
    # print('на первой точке нету стенки, идем дальше')
    while go:
        ax += xa
        ay += ya
        # print('ax, ay = ' + str(ax) + ' ' + str(ay))
        # print(degree)
        if ax > real_map_size or ay > real_map_size or ax < 0 or ay < 0:
            print('луч вышел за граници карты')
            break
        # testy = int((map_scale * ay) / (cube_size * number_cube))
        # testx = int((window_x - map_scale) + (map_scale * ax) / (cube_size * number_cube))
        # if -1000 > testx or testx > 1000:
        #    testx = 1000
        # #print(testx, testy)
        # pygame.draw.circle(window, (255, 255, 255), [testx, testy], 3, 3)

        #  проверка на наличие стенки
        # print('проверка на наличие стенки')
        if wall_collision_h(wall_list, ax, ay):
            dis = distance(xp, yp, ax, ay)
            return ax, ay, dis
    return 0, 0, 1000


def vertical_rey(xp, yp, degree):
    temporarily_dis = 0
    """пускаем луч по вертикалям"""
    # print('пускаем луч по вертикалям')
    # print('degree' + str(degree))
    # print('xp ' + str(xp))
    # print('yp ' + str(yp))
    go = True

    #  ищем значение к которому потом будем прибавлять первое пересечение (ya, xa)
    #  и ищем самою первою точку пересечения по горизонтали  (bx, by)
    #print('ищем ya, xa, bx, by')
    if 90 < degree < 270:  # лево
        bx = int(xp / cube_size) * cube_size
        xa = - cube_size
    else:  # право
        bx = int(xp / cube_size) * cube_size + cube_size
        xa = cube_size
    tangens_degree = math.tan((degree * math.pi) / 180)
    if tangens_degree != 0:
        if 90 < degree < 270:
            ya = cube_size * tangens_degree
        else:
            ya = - cube_size * tangens_degree
        by = yp + (xp - bx) * tangens_degree
    else:
        ya = 0
        by = yp
    #  проверка на наличие стенки на первой точке
    #print('проверка на наличие стенки на первой точке')
    if wall_collision_v(wall_list, bx, by):
        dis = distance(xp, yp, bx, by)
        return bx, by, dis
    # testy = int((map_scale * by) / (cube_size * number_cube))
    # testx = int((window_x - map_scale) + (map_scale * bx) / (cube_size * number_cube))
    # if -1000 > testy or testy > 1000:
    #     testy = 1000
    #  # print(testx, testy)
    # pygame.draw.circle(window, (255, 255, 255), [testx, testy], 3, 3)

    #  если на первой точке нету стенки то идем дальше
    #print('на первой точке нету стенки, идем дальше')
    while go:
        bx += xa
        by += ya

        # testy = int((map_scale * by) / (cube_size * number_cube))
        # testx = int((window_x - map_scale) + (map_scale * bx) / (cube_size * number_cube))
        # if -1000 > testy or testy > 1000:
        #     testy = 1000
        # # print(testx, testy)
        # pygame.draw.circle(window, (255, 255, 255), [testx, testy], 3, 3)

        if bx > real_map_size or by > real_map_size or bx < 0 or by < 0:
            # print('луч вышел за граници карты')
            return 0, 0, 1000
        #  проверка на наличие стенки
        #print('проверка на наличие стенки')
        if wall_collision_v(wall_list, bx, by):
            dis = distance(xp, yp, bx, by)
            return bx, by, dis
    return 0, 0


def ray(x_p, y_p, degree):
    x_h, y_h, dis_h = horizontal_rey(x_p, y_p, degree)
    x_v, y_v, dis_v = vertical_rey(x_p, y_p, degree)
    if dis_h < dis_v:
        color = (255, 0, 0)
        return x_h, y_h, dis_h, color
    else:
        color = (255, 255, 0)
        return x_v, y_v, dis_v, color



for item in map_list:
    # print(item, end='')
    if item != '0' and item != '#':
        pass

player = Player(400, 400, 100, FOV)
# for number in range(int(-player.v_a / 2), 0, 5):
#     rey_list.append(Rey(player.x, player.y, number))

# for number in range(1, player.v_a + 1, 5):
#     rey_list.append(Rey(player.x, player.y, number))
gorey = True
fix = True

count_x = 0
count_y = 0
for item in map_list:  # рисование стени
    if count_x > number_cube:
        count_x = 0
        count_y += 1
    if item == '#':
        wall_list.append([count_x, count_y])
    count_x += 1

while run:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.MOUSEMOTION:
            player.rotate(- e.rel[0])
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            gorey = not gorey
        if e.type == pygame.KEYDOWN and e.key == pygame.K_t:
            fix = not fix
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x, y = convert_degree_in_vector2(player.degree - 90)
        player.x += x * 2
        player.y += y * 2
    if keys[pygame.K_a]:
        x, y = convert_degree_in_vector2(player.degree + 90)
        player.x += x * 2
        player.y += y * 2
    if keys[pygame.K_w]:
        player.x += player.direction[0] * 2
        player.y += player.direction[1] * 2
    if keys[pygame.K_s]:
        player.x -= player.direction[0] * 2
        player.y -= player.direction[1] * 2
        # for rey in rey_list:
        #     rey.st_x = player.x
        #     rey.st_y = player.y
        #     rey.active = True
        #     rey.x = rey.st_x
        #     rey.y = rey.st_y
    # if keys[pygame.K_r]:
    #     print(horizontal_rey(player.x, player.y, player.degree))
    window.fill((119, 136, 153))

    # for rey in rey_list:
    #     rey.draw()
    #     x, y = convert_degree_in_vector(rey.deviation + player.degree)
    #     rey.update([x, y], wall_list)
    #     if rey.collision:
    #         pygame.draw.rect(window, (0, 0, 0), [100 + rey.deviation, 300, 5, 100 - rey.distance])
    #         print(rey.distance)
    Game.draw_minimap()
    distance_list = []
    if gorey:
        col = 1
        go = True
        degree = player.degree - player.v_a / 2
        while go:
            col += 0.5
            degree += ray_degree
            x, y, dis, color = ray(player.x, player.y, revers_degree(int(degree)))
            if fix:
                dis *= math.cos((degree - player.degree) * math.pi / 180)
            distance_list.append(dis)
            testy = int((map_scale * y) / (cube_size * number_cube))
            testx = int((window_x - map_scale) + (map_scale * x) / (cube_size * number_cube))
            #print(testx1, testy1)
            if -1000 < testx or testx < 1000:
                pygame.draw.circle(window, color, [testx, testy], 3, 3)
            if degree == player.degree + player.v_a / 2:
                go = False
    Game.draw_screen(distance_list)
    #Game.draw_screen()
    pygame.display.update()
