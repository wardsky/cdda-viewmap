import json
from os import listdir, path

class GameData:

    def __init__(self, data_dir):

        self.entries = entries = {}

        for subdir in ['furniture_and_terrain']:

            dirname = path.join(data_dir, subdir)

            for basename in listdir(dirname):

                filename = path.join(dirname, basename)

                with open(filename) as f:

                    read_data = f.read()

                    for entry in json.loads(read_data):

                        if 'id' in entry:
                            if entry['id'] in entries:
                                print('Duplicate id: ' + entry['id'])
                            entries[entry['id']] = entry
                        else:
                            print('Entry has no id')
                            print(entry)
