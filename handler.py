class Handler:
    def __init__(self, pantry, book):
        self.pantry = pantry
        self.book = book

    def get_pantry(self):
        data = self.pantry.read_ingredients()
        return data

    def get_recipes(self):
        data = self.book.read_recipes()
        return data

    def search_for_recipe(self, recipe):
        data = self.book.search_recipes(recipe)
        return data
