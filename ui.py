from tkinter import *
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
        self.window.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="column")
        self.window.grid_rowconfigure((0, 1, 2), weight=1, uniform="row", minsize=100)
        # self.bg_image = ImageTk.PhotoImage(Image.open("./img/polkadot.jpg")) # Image by juicy_fisha on Freepik

        self.home()
        self.window.mainloop()

    def home(self):
        """
        UI for the home screen
        """
        for i in self.window.winfo_children():
            i.destroy()
        frame = Frame(self.window, width=win_width, height=win_height, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        # Displays the Home page options
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
        nav_grid(buttons, 3)

    def ingredients(self):
        """
        UI for the Pantry page
        """
        for i in self.window.winfo_children():
            i.destroy()
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
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
        nav_grid(buttons, 3)

    def new_ingredient_popup(self):
        """
        UI to submit new ingredient into the Pantry
        """
        top = Toplevel(self.window)
        top.title("New Ingredient")
        main_x = self.window.winfo_rootx() + win_width//4
        main_y = self.window.winfo_rooty() + win_height//3
        print(main_x)

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

    def recipes(self):
        """
        UI for the Recipe book page
        """
        for i in self.window.winfo_children():
            i.destroy()

        frame = Frame(self.window, width=win_width, height=win_height, bg=THEME_COLOR)
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        canvas = Canvas(frame, bg='Yellow')
        canvas.grid(row=0, column=0)

        scroll = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=3, sticky='NS')
        canvas.configure(yscrollcommand=scroll.set)

        buttons_frame = Frame(canvas)
        buttons_frame.grid(column=0, row=0, columnspan=4, rowspan=3, sticky='NSEW')

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

        canvas.create_window((0, 0), window=buttons_frame, anchor='nw')
        buttons_frame.update_idletasks()
        bbox = canvas.bbox(ALL)

        w, h = bbox[2] - bbox[1], bbox[3] - bbox[1]
        dw, dh = int((w / 4) * 4), int((h / 4) * 3)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)

        buttons = [
            Button(text="Add", command=lambda: self.new_recipe_popup()),
            Button(text="Edit"),
            Button(text="Delete"),
            Button(text="Home", command=lambda: self.home())]
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

