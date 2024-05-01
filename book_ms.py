import json
import os
from json import JSONDecodeError

import pandas as pd


class Recipe:
    def __init__(self, args):
        self.name = args[0].title()
        self.description = args[1]


class RecipeBook:
    def __init__(self):
        self.file = 'recipes.json'

    def new_recipe(self, args):
        item = Recipe(args)
        recipe = {
            item.name: {
                "description": item.description
            }
        }
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except JSONDecodeError:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, indent=4)
            else:
                data.update(recipe)
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, sort_keys=True)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(recipe, f, indent=4)

    def read_recipes(self):
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
                dframe = pd.DataFrame(data)
                output = []
                for col in dframe.columns:
                    output.append(col)
            finally:
                return output

    def search_recipes(self, name):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = json.dumps(data)
            data = json.loads(data)
            print(data[name])
