import json
from os import listdir, path

class GameData:

    def load_data(self, source):

        if path.isfile(source):

            with open(source) as f:

                    read_data = f.read()

                    for entry in json.loads(read_data):
                        if 'id' in entry:
                            if type(entry['id']) is str:
                                if entry['id'] in self.entries:
                                    print(f"Duplicate id: {entry['id']}")
                                self.entries[entry['id']] = entry
                            else:
                                print(f"Non-str id: {entry['id']}")
                        elif 'abstract' not in entry:
                            print('Entry has no id')
                            print(entry)
        
        elif path.isdir(source):

            for name in listdir(source):
                filename = path.join(source, name)
                self.load_data(filename)


    def __init__(self, data_dir):

        self.entries = {}

        for subdir in ['furniture_and_terrain', 'items']:
            dirname = path.join(data_dir, subdir)
            self.load_data(dirname)
                
