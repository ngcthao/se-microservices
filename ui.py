from tkinter import *
from PIL import Image, ImageTk
from handler import Handler
from time import sleep
THEME_COLOR = "#375362"
WHITE = "#FFFFFF"


def nav_grid(buttons):
    i = 0
    j = 3
    for button in buttons:
        button.grid(column=i, row=j)
        i += 1


class UserInterface:
    """
    Handles the graphical interface of the pantry application.
    """
    def __init__(self, handler: Handler):
        self.handler = handler
        self.window = Tk()
        self.window.title("Pantry Application")
        self.window.config(padx=20, pady=20, bg=WHITE)
        self.window.geometry("440x540")
        self.bg_image = ImageTk.PhotoImage(Image.open("./img/polkadot.jpg")) # Image by juicy_fisha on Freepik

        self.home()
        self.window.mainloop()

    def home(self):
        for i in self.window.winfo_children():
            i.destroy()
        frame = Frame(self.window, width=400, height=500, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        button1 = Button(text="Fridge", command=lambda: self.ingredients())
        button2 = Button(text="Recipe Book", command=lambda: self.recipes())
        button3 = Button(text="Shopping Cart")
        button1.grid(column=0, row=0, columnspan=4, sticky='NSEW', pady=10)
        button2.grid(column=0, row=1, columnspan=4, sticky='NSEW', pady=10)
        button3.grid(column=0, row=2, columnspan=4, sticky='NSEW', pady=10)

        buttons = [
            Button(text="Add"),
            Button(text="Edit"),
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
        nav_grid(buttons)

    def ingredients(self):
        for i in self.window.winfo_children():
            i.destroy()
        frame = Frame(self.window, width=400, height=500, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        display = Text(self.window)
        display.grid(column=0, row=0, rowspan=3, columnspan=4)
        items = self.handler.get_pantry()
        display.insert(END, items)

        buttons = [
            Button(text="Add", command=lambda: self.new_ingredient_popup()),
            Button(text="Edit"),
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
        nav_grid(buttons)

    def recipes(self):
        for i in self.window.winfo_children():
            i.destroy()
        frame = Frame(self.window, width=400, height=500, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        row = 0
        col = 0
        button_list = [[0 for j in range(4)] for i in range(3)]
        for recipe in self.handler.get_recipes():
            button_list[row][col] = Button(text=recipe, command=lambda x=recipe: self.recipe_popup(x))
            button_list[row][col].grid(column=col, row=row, sticky='NSEW')
            if row <= 3:
                col += 1
                row = 0
            else:
                row += 1

        buttons = [
            Button(text="Add", command=lambda: self.new_recipe_popup()),
            Button(text="Edit"),
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
        nav_grid(buttons)

    def recipe_popup(self, recipe):
        self.handler.search_for_recipe(recipe)
        top = Toplevel(self.window)
        top.geometry("200x200")
        top.title("Recipe")

    def new_recipe_popup(self):
        pass

    def new_ingredient_popup(self):
        pass
