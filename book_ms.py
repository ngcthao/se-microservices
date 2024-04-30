import json
import os
import pandas as pd


class Recipe:
    def __init__(self, name, ingredients, description):
        self.name = name
        self.ingredients = ingredients
        self.description = description


class RecipeBook:
    def __init__(self):
        self.file = 'recipes.json'

    def new_recipe(self, item):
        recipe = {
            item.name: {
                "ingredients": item.ingredients,
                "description": item.description
            }
        }
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.update(recipe)

            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        else:
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(recipe, f, indent=4)

    def read_recipes(self):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = json.dumps(data)
            data = json.loads(data)
            dframe = pd.DataFrame(data)
            output = []
            for col in dframe.columns:
                output.append(col)
            return output

    def search_recipes(self, name):
        if os.path.exists(self.file):
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = json.dumps(data)
            data = json.loads(data)
            print(data[name])