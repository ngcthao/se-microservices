# Referenced Code:
# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid/49681192#49681192

from tkinter import *
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
from handler import Handler
THEME_COLOR = "#375362"
WHITE = "#FFFFFF"
win_width = 400
win_height = 500


def nav_grid(buttons, row):
    i = 0
    j = row
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
        # self.bg_image = ImageTk.PhotoImage(Image.open("./img/polkadot.jpg")) # Image by juicy_fisha on Freepik
        self.welcome = True;
        self.home()

        self.window.mainloop()

    def home(self):
        """
        UI for the home screen
        """
        for i in self.window.winfo_children():
            i.destroy()

        self.window.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="column")
        self.window.grid_rowconfigure((0, 1, 2), weight=1, uniform="row", minsize=100)
        frame = Frame(self.window, width=win_width, height=win_height, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        # Displays the Home page options
        button1 = Button(text="Pantry", command=lambda: self.ingredients())
        button2 = Button(text="Recipe Book", command=lambda: self.recipes())
        button3 = Button(text="Welcome Page", command=lambda: self.welcome_popup())
        button1.grid(column=0, row=0, columnspan=4, sticky='NSEW', pady=10)
        button2.grid(column=0, row=1, columnspan=4, sticky='NSEW', pady=10)
        button3.grid(column=0, row=2, columnspan=4, sticky='NSEW', pady=10)

        Hovertip(button1, 'View all ingredients in the pantry.', hover_delay=1000)
        Hovertip(button2, 'View all saved recipes.', hover_delay=1000)
        Hovertip(button3, 'View items in the shopping cart.', hover_delay=1000)

        buttons = [
            Button(text="Add"),
            Button(text="Edit"),
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
        Hovertip(buttons[0], 'Add new ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[1], 'Edit existing ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[2], 'Delete existing ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[3], 'Go to homepage.', hover_delay=1000)
        nav_grid(buttons, 3)

        if self.welcome:
            self.welcome_popup()

    def welcome_popup(self):
        """
                UI to submit new ingredient into the Pantry
                """
        top = Toplevel(self.window)
        top.title("Welcome Page")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        top.geometry(f'+{main_x}+{main_y}')

        display = Text(top)
        display.grid(column=0, row=0, columnspan=2, sticky='NSEW')
        items = "Welcome to the Foodie App!\n\n" \
                "Selecting add/edit/delete on the Home Page will allow you to make changes to the Pantry and/or Recipe Book.\n" \
                "Selecting Pantry will allow you to view and add/edit/delete ingredients only.\n" \
                "Selecting Recipe Book will allow you to view and add/edit/delete recipes only.\n" \
                "Selecting Welcome Page will reopen this text box.\n" \
                "Selecting Home on any page will bring you back to the Home Page.\n\n" \
                "FAQ:\n" \
                "Can I recover a deleted item?\n" \
                "No, all deletions are permanent.\n\n" \
                "How do I add a new ingredient?\n" \
                "To add a new ingredient, please select Pantry -> Add. " \
                "Alternatively, you may select Add -> Ingredient on the Homepage.\n"
        display.insert(END, items)
        display.config(state=DISABLED)

        submit = Button(top, text="Skip on Next Opening")
        submit.grid(column=0, row=1, columnspan=2)

    def ingredients(self):
        """
        UI for the Pantry page
        """
        for i in self.window.winfo_children():
            i.destroy()
        self.window.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="column")
        self.window.grid_rowconfigure((0, 1, 2), weight=1, uniform="row", minsize=100)
        frame = Frame(self.window, width=win_width, height=win_height, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        display = Text(self.window)
        display.grid(column=0, row=0, rowspan=3, columnspan=4, sticky='NSEW')
        items = self.handler.get_pantry()
        display.insert(END, items)
        display.config(state=DISABLED)

        buttons = [
            Button(text="Add", command=lambda: self.new_ingredient_popup()),
            Button(text="Edit"),
            Button(text="Delete", command=lambda: self.delete_ingredient_popup()),
            Button(text="Home", command=lambda: self.home())]
        Hovertip(buttons[0], 'Add new ingredient.', hover_delay=1000)
        Hovertip(buttons[1], 'Edit existing ingredient.', hover_delay=1000)
        Hovertip(buttons[2], 'Delete existing ingredient.', hover_delay=1000)
        Hovertip(buttons[3], 'Go to homepage.', hover_delay=1000)
        nav_grid(buttons, 3)

    def new_ingredient_popup(self):
        """
        UI to submit new ingredient into the Pantry
        """
        top = Toplevel(self.window)
        top.title("New Ingredient")
        main_x = self.window.winfo_rootx() + win_width//4
        main_y = self.window.winfo_rooty() + win_height//3

        top.geometry(f'+{main_x}+{main_y}')

        name_label = Label(top, text="Item Name")
        name_label.grid(column=0, row=0)
        name = Entry(top)
        name.grid(column=1, row=0)

        count_label = Label(top, text="Quantity")
        count_label.grid(column=0, row=1)
        count = Entry(top)
        count.grid(column=1, row=1)

        options = ["boxes", "units", "cans", "trays", "bags"]
        clicked = StringVar()
        clicked.set("units")

        units = OptionMenu(top, clicked, *options)
        units.grid(column=2, row=1)

        args = ["ingredient", name, count, clicked]

        submit = Button(top, text="Confirm", command=lambda: self.submit(top, args, self.ingredients))
        submit.grid(column=0, row=2, columnspan=2)

    def delete_ingredient_popup(self):
        """
            UI to delete ingredient
        """
        top = Toplevel(self.window)
        top.title("Delete Ingredient")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3
        print(main_x)

        top.geometry(f'+{main_x}+{main_y}')

        name_label = Label(top, text="!!All deletions are permanent!!")
        name_label.grid(column=0, row=0)

        submit = Button(top, text="Confirm")
        submit.grid(column=0, row=1, columnspan=2)

    def recipes(self):
        """
        UI for the Recipe book page
        """
        for i in self.window.winfo_children():
            i.destroy()
        # Main Frame
        master_frame = Frame(self.window, width=win_width, height=win_height, bg=THEME_COLOR)
        master_frame.grid(column=0, row=0, columnspan=5, rowspan=4, sticky='NSEW')
        master_frame.grid_columnconfigure((0, 1, 2, 3), weight=2, uniform="column")
        master_frame.grid_rowconfigure((0, 1, 2), weight=2, uniform="row")
        # Inner Frame to hold buttons and scroll bar
        inner_frame = Frame(master_frame, bg='Red')
        inner_frame.grid(row=0, column=0, columnspan=5, rowspan=3, sticky='NSEW')
        inner_frame.grid_columnconfigure((0, 1, 2, 3), weight=2, uniform="column")
        inner_frame.grid_rowconfigure((0, 1, 2), weight=2, uniform="row")
        # Canvas inside inner frame
        canvas = Canvas(inner_frame, bg='Yellow')
        canvas.grid(row=0, column=0, columnspan=5, rowspan=3, sticky='NSEW')
        # Scroll bar linked to canvas
        scroll = Scrollbar(inner_frame, orient=VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=4, rowspan=3, sticky='NS')
        canvas.configure(yscrollcommand=scroll.set)
        # Frame to contain buttons grid
        buttons_frame = Frame(canvas, bg='blue')
        buttons_frame.grid(row=0, column=0, sticky='NSEW')

        row = 0
        col = 0
        button_list = [[0 for j in range(20)] for i in range(20)]
        for recipe in self.handler.get_recipes():
            button_list[row][col] = Button(buttons_frame, text=recipe, command=lambda x=recipe: self.recipe_popup(x))
            button_list[row][col].grid(column=col, row=row, sticky='NSEW')
            if col < 3:
                col += 1
            else:
                col = 0
                row += 1

        buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=19, uniform="column")
        for row_num in range(buttons_frame.grid_size()[1]):
            buttons_frame.grid_rowconfigure(row_num, weight=1, uniform="row", minsize=50)

        canvas.create_window((0, 0), window=buttons_frame)
        buttons_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        buttons = [
            Button(master_frame, text="Add", command=lambda: self.new_recipe_popup()),
            Button(master_frame, text="Edit"),
            Button(master_frame, text="Delete"),
            Button(master_frame, text="Home", command=lambda: self.home())]
        Hovertip(buttons[0], 'Add new recipe.', hover_delay=1000)
        Hovertip(buttons[1], 'Edit existing recipe.', hover_delay=1000)
        Hovertip(buttons[2], 'Delete existing recipe.', hover_delay=1000)
        Hovertip(buttons[3], 'Go to homepage.', hover_delay=1000)
        nav_grid(buttons, 3)

    def recipe_popup(self, recipe):
        """
        UI to view selected recipe
        :param recipe: name of desired recipe
        """
        self.handler.search_for_recipe(recipe)
        top = Toplevel(self.window)
        top.geometry("200x200")
        top.title("Recipe")

    def new_recipe_popup(self):
        """
        UI to add a new recipe to the Recipe book
        """
        top = Toplevel(self.window)
        top.title("New Recipe")
        name_label = Label(top, text="Recipe Name")
        name_label.grid(column=0, row=0)
        name = Entry(top)
        name.grid(column=1, row=0)

        info_label = Label(top, text="Description")
        info_label.grid(column=0, row=1)
        info = Text(top)
        info.grid(column=1, row=1)

        args = ["recipe", name, info]

        submit = Button(top, text="Confirm", command=lambda: self.submit(top, args, self.recipes))
        submit.grid(column=0, row=2, columnspan=2)

    def add_redirect(self):


    def submit(self, window, args, reload):
        """
        Submits user inputs and refreshes the page
        :param window: window to be closed
        :param args: arguments to be sent to the handler
        :param reload: window to be refreshed
        """
        if args[0] == "ingredient":
            self.handler.new_ingredient(args=[args[1].get(), int(args[2].get()), args[3].get()])
        elif args[0] == "recipe":
            self.handler.new_recipe(args=[args[1].get(), args[2].get(1.0, "end-1c")])
        else:
            pass

        window.destroy()
        reload()

