import json

class MapData:

    WIDTH = 24
    HEIGHT = 24

    def __init__(self, mapfile):

        with open(mapfile) as f:

            read_data = f.read()
            map_data = json.loads(read_data)

            terrain_buf = []
            for submap in map_data:
                for val in submap['terrain']:
                    if type(val) is str:
                        terrain_buf.append(val)
                    if type(val) is list:
                        terrain_buf.extend([val[0]] * val[1])

            self.layers = {}

            self.layers['terrain'] = terrain = {}
            half_width = MapData.WIDTH // 2
            for i in range(len(terrain_buf)):
                (x, y) = (i % MapData.WIDTH, i // MapData.WIDTH)
                (u, v) = (x, y) if x < half_width else (x - half_width, y + MapData.HEIGHT)
                j = v * half_width + u
                terrain[x, y] = terrain_buf[j]

            self.layers['furniture'] = furniture = {}
            for i, submap in enumerate(map_data):
                for (x, y, id) in submap['furniture']:
                    if i == 2 or i == 3:
                        x += MapData.WIDTH // 2
                    if i == 1 or i == 3:
                        y += MapData.HEIGHT // 2
                    furniture[x, y] = id
