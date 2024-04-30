import json
import os
import pandas as pd


class Ingredient:
    def __init__(self, ingredient, quantity):
        self.name = ingredient
        self.count = quantity


class Pantry:
    def __init__(self):
        self.file = 'ingredients.json'

    def new_ingredient(self, item):
        ingredient = {
            item.name: {"quantity": item.count}
        }
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.update(ingredient)

            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(ingredient, f, indent=4)

    def read_ingredients(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = json.dumps(data)
            data = json.loads(data)
            output = pd.DataFrame(data).transpose()
            return output