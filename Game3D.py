import pygame

run = True

map_scale = 150
map_lenght = 10
wall_lenght = map_scale / map_lenght
map_background_color = 47, 79, 79
map_list = '''##########
#00##0000#
#000#0000#
#000###00#
#000000#0#
#0##00000#
#000#0000#
#00000000#
#00000000#
##########'''


class Game:
    window_x = 600
    window_y = 600
    window = pygame.display.set_mode((window_x, window_y))

    @classmethod
    def draw_minimap(cls, map_color, map_scale):
        count_x = 0
        count_y = 0
        pygame.draw.rect(Game.window, map_color, (Game.window_x - map_scale, 0, map_scale, map_scale))
        for item in map_list:
            if count_x > map_lenght:
                count_x = 0
                count_y += 1
            if item == '#':
                pygame.draw.rect(Game.window, (0, 0, 0), (count_x * wall_lenght + Game.window_x - map_scale, count_y * wall_lenght, wall_lenght, wall_lenght))
            count_x += 1


for item in map_list:
    print(item, end='')
    if item != '0' and item != '#':
        pass
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    Game.window.fill((119, 136, 153))
    Game.draw_minimap(map_background_color, map_scale)
    pygame.display.update()
