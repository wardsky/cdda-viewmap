from pylib.tileset import connectivity_table

class MapView:

    def __init__(self, map_data, game_data, tileset):
        self.map_data = map_data
        self.game_data = game_data
        self.tileset = tileset

    def get_tile_for_id(self, id):
        # Not yet implemented:
        # - Seasonal variants
        # - "unknown-{category}-{subcategory}" and "unknown-{category}" fallbacks (though this is almost unused)
        # - ASCII fallbacks
        tried_ids = []
        while id and id not in tried_ids:
            if id in self.tileset.tiles:
                return self.tileset.tiles[id]
            tried_ids.append(id)
            if id in self.game_data.entries:
                entity_data = self.game_data.entries[id]
                id = entity_data.get('looks_like', None)
            else:
                print(f"Couldn't find {id} in game data")
                break
        return self.tileset.tiles.get('unknown', None)

    def get_connection_group(self, id):
        if id in self.game_data.entries:
            entity_data = self.game_data.entries[id]
            if 'connects_to' in entity_data:
                return entity_data['connects_to']
            if 'flags' in entity_data:
                if 'WALL' in entity_data['flags'] or 'CONNECT_TO_WALL' in entity_data['flags']:  # Deprecated flag
                    return 'WALL'
        return id

    def get_connectivity(self, layer, loc):
        (x, y) = loc
        conn_group = self.get_connection_group(self.map_data.layers[layer][x, y])
        adj_locs = (
            (x, y + 1),
            (x + 1, y),
            (x - 1, y),
            (x, y - 1),
        )
        code = 0
        for i, adj_loc in enumerate(adj_locs):
            if adj_loc in self.map_data.layers[layer]:
                adj_conn_group = self.get_connection_group(self.map_data.layers[layer][adj_loc])
                if adj_conn_group == conn_group:
                    code |= 1 << i
        return code

    def get_sprite(self, loc, layer):
        if loc in self.map_data.layers[layer]:
            tile = self.get_tile_for_id(self.map_data.layers[layer][loc])
            if tile is not None:
                sprites = tile['sprites']
                offset = (tile['offset_x'], tile['offset_y'])
                if len(sprites) == 0:
                    return (None, offset)
                connectivity_code = self.get_connectivity(layer, loc)
                if len(sprites) == len(connectivity_table):
                    return (sprites[connectivity_code], offset)
                (_, orientation) = connectivity_table[connectivity_code]
                return (sprites[orientation % len(sprites)], offset)
        return (None, (0, 0))
