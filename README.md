CDDA map viewer
===============

Mapfile viewer for [Cataclysm: Dark Days Ahead](https://cataclysmdda.org/).

Usage: `./viewmap sample_map/house.map`

You can try it with the sample mapfiles in the sample_maps directory or with any of the ones from your saved world.
These can be found under 'save/WORLD_NAME/maps/X.Y.Z/'.

This tool requires Python 3 with the pygame library installed. You may need to modify config.json to specify the paths
to your CDDA game data and tileset directories.

Yet to be implemented:

- Layers other than terrain and furniture.
- ASCII fallback and oversized sprites
- Seasonal tile variants
- Animated / randomised tiles
