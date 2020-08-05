from pylib.map_data import MapData

class PlanGridView:

    def __init__(self, options):
        self.tile_width = options['tile_width']
        self.tile_height = options['tile_height']
        self.map_cols = options['map_cols']
        self.map_rows = options['map_rows']

    def size(self, scale=1):
        return (
            scale * self.tile_width * self.map_cols,
            scale * self.tile_height * self.map_rows,
        )

    def get_tile_offset(self, col, row, scale=1):
        return (
            scale * self.tile_width * col,
            scale * self.tile_height * row,
        )

    def get_tile_location(self, x, y, scale=1):
        return (x // (scale * self.tile_width), y // (scale * self.tile_height))

class IsoGridView:

    # Iso -- North is towards the top-left

    def __init__(self, options):
        self.tile_width = options['tile_width']
        self.tile_height = options['tile_height']
        # 'depth' is height of tile footprint, which is always half its width (per the CDDA code)
        self.tile_depth = self.tile_width // 2
        # 'elev' is the amount the tile sticks up above its footprint
        self.tile_elev = self.tile_height - self.tile_depth
        self.map_cols = options['map_cols']
        self.map_rows = options['map_rows']

    def size(self, scale=1):
        return (
            scale * self.tile_width * (self.map_cols + self.map_rows) // 2,
            scale * (self.tile_depth * (self.map_cols + self.map_rows) // 2 + self.tile_elev),
        )

    def get_tile_offset(self, col, row, scale=1):
        return (
            scale * self.tile_width * (row + self.map_rows + col - self.map_cols) // 2,
            scale * (self.tile_depth * (self.map_cols - col - 1 + row) // 2),
        )

    def get_tile_location(self, x, y, scale=1):
        vertical_offset = self.tile_elev + self.tile_depth * (self.map_cols + self.map_rows) // 4
        u = (x // scale) * self.tile_depth
        v = ((y // scale) - vertical_offset) * self.tile_width
        w = self.tile_width * self.tile_depth
        return ((u - v) // w, (u + v) // w)

def make_grid_view(tileset):
    options = {
        'tile_width': tileset.tile_width,
        'tile_height': tileset.tile_height,
        'map_cols': MapData.WIDTH,
        'map_rows': MapData.HEIGHT,
    }
    GridView = IsoGridView if tileset.iso else PlanGridView
    return GridView(options)
