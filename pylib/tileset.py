import json
from os import path
from pygame import Rect, Surface, image, transform
from pygame.locals import SRCALPHA

# These are the (connectedness, orientation) values for each of the 16 possible patterns of connected tiles.
# Orientation: 0 means the tile appears exactly as it does in the tileset; other values indicate 90/180/270deg rotation.
# See get_connectivity() in map_view.py for how the index into this list is calculated.
connectivity_table = (
    ('unconnected', 0),
    ('end_piece', 0),
    ('end_piece', 1),
    ('corner', 0),
    ('end_piece', 3),
    ('corner', 3),
    ('edge', 1),
    ('t_connection', 0),
    ('end_piece', 2),
    ('edge', 0),
    ('corner', 1),
    ('t_connection', 1),
    ('corner', 2),
    ('t_connection', 3),
    ('t_connection', 2),
    ('center', 0),
)

def get_tile_sprites(sprites, spec, rotate=False):
    # Sprite specifier 'spec' can have different forms:
    # 1. Single value
    # 2. List of 1/2/4 values (rotations)
    # 3. A weighted list of (1) or (2) (Not currently implemented -- just use the first variation)
    # A valid spec will always return a 1-, 2-, or 4-element list of sprites. corresponding to possible orientations.
    # Setting 'rotate' will generate all four orientations by rotating the sprites, if a single sprite is specified.
    if type(spec) is list:
        if len(spec) == 0:
            return None
        if type(spec[0]) is dict:
            return get_tile_sprites(sprites, spec[0]['sprite'])
        return [sprites[i] for i in spec]
    if spec in range(len(sprites)):
        if rotate:
            return [transform.rotate(sprites[spec], angle) for angle in (0, 90, 180, 270)]
        return [sprites[spec]]

def compose_tile_sprites(sprites, tile_size, tile_info):

    result = []

    if tile_info.get('multitile', False):

        multitile_sprites = [{} for _ in connectivity_table]
        for key in ('bg', 'fg'):
            if key in tile_info:
                sprite_list = get_tile_sprites(sprites, tile_info[key], key == 'fg')
                if sprite_list is not None:
                    for i, (_, orientation) in enumerate(connectivity_table):
                        multitile_sprites[i][key] = sprite_list[orientation % len(sprite_list)]
        if 'additional_tiles' in tile_info:
            for add_tile_info in tile_info['additional_tiles']:
                for i, (connectedness, orientation) in enumerate(connectivity_table):
                    if add_tile_info['id'] == connectedness:
                        for key in ('bg', 'fg'):
                            if key in add_tile_info:
                                sprite_list = get_tile_sprites(sprites, add_tile_info[key], key == 'fg')
                                multitile_sprites[i][key] = sprite_list[orientation % len(sprite_list)]

        for entry in multitile_sprites:
            sprite = Surface(tile_size, SRCALPHA)
            for key in ('bg', 'fg'):
                if key in entry:
                    sprite.blit(entry[key], (0, 0))
            result.append(sprite)

    else:

        tile_sprites = {}
        rotates = tile_info.get('rotates', False)
        count = 0
        for key in ('bg', 'fg'):
            if key in tile_info:
                sprite_list = get_tile_sprites(sprites, tile_info[key], rotates and key == 'fg')
                if sprite_list is not None:
                    tile_sprites[key] = sprite_list
                    count = max(count, len(sprite_list))
        for i in range(count):
            sprite = Surface(tile_size, SRCALPHA)
            for key in ('bg', 'fg'):
                if key in tile_sprites:
                    sprite.blit(tile_sprites[key][i % len(tile_sprites[key])], (0, 0))
            result.append(sprite)

    return result

class Tileset:

    def __init__(self, tile_config_file, game_data):

        with open(tile_config_file) as f:

            read_data = f.read()
            tile_config = json.loads(read_data)

            tile_info = tile_config['tile_info'][0]
            self.tile_width = tile_width = tile_info['width']
            self.tile_height = tile_height = tile_info['height']
            self.pixelscale = tile_info.get('pixelscale', 1)
            self.iso = tile_info.get('iso', False)

            self.game_data = game_data

            tileset_dir = path.dirname(tile_config_file)

            self.tiles = {}
            for spritesheet_info in tile_config['tiles-new']:

                filename = path.join(tileset_dir, spritesheet_info['file'])

                spritesheet = image.load(filename)
                spritesheet_width = spritesheet.get_width()
                spritesheet_height = spritesheet.get_height()

                sprites = []
                for y in range(0, spritesheet_height, tile_height):
                    for x in range(0, spritesheet_width, tile_width):
                        rect = Rect(x, y, tile_width, tile_height)
                        sprites.append(spritesheet.subsurface(rect))

                for tile_info in spritesheet_info['tiles']:
                    tile = {}
                    tile['height_3d'] = tile_info.get('height_3d', 0)
                    tile['sprites'] = compose_tile_sprites(sprites, (tile_width, tile_height), tile_info)

                    ids = tile_info['id'] if type(tile_info['id']) is list else [tile_info['id']]
                    for id in ids:
                        self.tiles[id] = tile

                break  # TODO: Handle spritesheets beyond the first (Seem to be more complex, e.g., larger sprites)
