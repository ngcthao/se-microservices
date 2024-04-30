from pantry_ms import Pantry
from book_ms import RecipeBook, Recipe
from handler import Handler
from ui import UserInterface

recipe = Recipe("cake", "cake stuff?", "disaster...")

pantry = Pantry()
book = RecipeBook()
handler = Handler(pantry, book)
book.new_recipe(recipe)
pantry_ui = UserInterface(handler)