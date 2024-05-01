import json
import os
from json import JSONDecodeError

import pandas as pd


class Ingredient:
    def __init__(self, args):
        self.name = args[0].title()
        self.count = args[1]
        self.units = args[2].lower()


class Pantry:
    def __init__(self):
        self.file = 'ingredients.json'

    def new_ingredient(self, args):
        item = Ingredient(args)
        ingredient = {
            item.name: {
                "quantity": item.count,
                "unit of measurement": item.units
                        }
        }

        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(ingredient, f, indent=4)
            else:
                data.update(ingredient)
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(ingredient, f, indent=4)

    def read_ingredients(self):
        output = ""
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                pass
            else:
                data = json.dumps(data)
                data = json.loads(data)
                output = pd.DataFrame(data).transpose()
            finally:
                return output

