from pantry_ms import Pantry
from book_ms import RecipeBook, Recipe
from handler import Handler
from ui import UserInterface

pantry = Pantry()
book = RecipeBook()
handler = Handler(pantry, book)
pantry_ui = UserInterface(handler)