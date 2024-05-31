# Referenced Code:
# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid/49681192#49681192

from tkinter import *
from idlelib.tooltip import Hovertip
import socket
WHITE = "#FFFFFF"
win_width = 400
win_height = 500
SERVER_IP = "127.0.0.1"
RECIPE_PORT = 8100
PANTRY_PORT = 8400
WELCOME_PORT = 8300
COLOR_PORT = 8500


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
    def __init__(self):
        self.window = Tk()
        self.window.title("Pantry Application")
        self.window.config(padx=20, pady=20, bg=WHITE)
        self.window.geometry("440x540")
        self.welcome = True
        self.home()
        self.window.mainloop()

    def get_theme_color(self):
        # Connect to color socket
        color_socket.send("get".encode("utf-8")[:1024])
        return color_socket.recv(1024).decode("utf-8")

    def home(self):
        """
        UI for the home screen
        """
        for i in self.window.winfo_children():
            i.destroy()

        self.window.grid_columnconfigure(0, weight=1, uniform="column")
        self.window.grid_columnconfigure(1, weight=1, uniform="column")
        self.window.grid_columnconfigure(2, weight=1, uniform="column")
        self.window.grid_columnconfigure(3, weight=1, uniform="column")
        self.window.grid_rowconfigure(0, weight=1, uniform="row", minsize=100)
        self.window.grid_rowconfigure(1, weight=1, uniform="row", minsize=100)
        self.window.grid_rowconfigure(2, weight=1, uniform="row", minsize=100)
        frame = Frame(self.window, width=win_width, height=win_height, bg=self.get_theme_color())
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
        Hovertip(button3, 'View the welcome page.', hover_delay=1000)

        buttons = [
            Button(text="Add", command=lambda: self.add_popup()),
            Button(text="Edit", command=lambda: self.edit_popup()),
            Button(text="Delete", command=lambda: self.delete_popup()),
            Button(text="Settings", command=lambda: self.settings_popup())]
        Hovertip(buttons[0], 'Add new ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[1], 'Edit existing ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[2], 'Delete existing ingredient, recipe or shopping item.', hover_delay=1000)
        Hovertip(buttons[3], 'Edit the background color.', hover_delay=1000)
        nav_grid(buttons, 3)

        # Connect to socket
        welcome_socket.send("getskip".encode("utf-8")[:1024])
        response = welcome_socket.recv(1024).decode("utf-8")

        if response == "0" and self.welcome:
            self.welcome_popup()
            self.welcome = False

    def add_popup(self):
        top = Toplevel(self.window)
        top.title("Add")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=200, height=100)
        frame.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(0, minsize=100)
        frame.grid_columnconfigure(1, minsize=100)

        top.geometry(f'+{main_x}+{main_y}')

        add_label = Label(frame, text='Add a new')
        add_label.grid(column=0, row=0, columnspan=2)

        new_ingredient = Button(frame, text="Ingredient", command=lambda: self.new_ingredient_popup())
        new_ingredient.grid(column=0, row=2, sticky='EW')

        new_recipe = Button(frame, text="Recipe", command=lambda: self.new_recipe_popup())
        new_recipe.grid(column=1, row=2, sticky='EW')

    def edit_popup(self):
        top = Toplevel(self.window)
        top.title("Edit")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=200, height=100)
        frame.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(0, minsize=100)
        frame.grid_columnconfigure(1, minsize=100)

        top.geometry(f'+{main_x}+{main_y}')

        add_label = Label(frame, text='Edit an existing')
        add_label.grid(column=0, row=0, columnspan=2)

        new_ingredient = Button(frame, text="Ingredient", command=lambda: self.edit_ingredient_popup())
        new_ingredient.grid(column=0, row=2, sticky='EW')

        new_recipe = Button(frame, text="Recipe", command=lambda: self.edit_recipe_popup())
        new_recipe.grid(column=1, row=2, sticky='EW')

    def delete_popup(self):
        top = Toplevel(self.window)
        top.title("Delete")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=200, height=100)
        frame.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(0, minsize=100)
        frame.grid_columnconfigure(1, minsize=100)

        top.geometry(f'+{main_x}+{main_y}')

        add_label = Label(frame, text='Delete an existing')
        add_label.grid(column=0, row=0, columnspan=2)

        new_ingredient = Button(frame, text="Ingredient", command=lambda: self.delete_ingredient_popup())
        new_ingredient.grid(column=0, row=2, sticky='EW')

        new_recipe = Button(frame, text="Recipe", command=lambda: self.delete_recipe_popup())
        new_recipe.grid(column=1, row=2, sticky='EW')

    def settings_popup(self):
        top = Toplevel(self.window)
        top.title("Settings")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=200, height=100)
        frame.grid(column=0, row=0, columnspan=2, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(1, minsize=100)

        top.geometry(f'+{main_x}+{main_y}')

        bg_label = Label(frame, text='BG Color')
        bg_label.grid(column=0, row=0)

        # Connect to color socket
        color_socket.send("display".encode("utf-8")[:1024])
        response = color_socket.recv(1024).decode("utf-8")
        options = response.split("`")

        bg_color = StringVar()
        color = OptionMenu(frame, bg_color, *options)
        color.grid(column=1, row=0, sticky="ew")

        # Connect to welcome socket
        welcome_socket.send("getskip".encode("utf-8")[:1024])
        check = welcome_socket.recv(1024).decode("utf-8")

        welcome_label = Label(frame, text='Skip Welcome Page')
        welcome_label.grid(column=0, row=1)

        check_skip = IntVar()
        check_skip.set(check)
        skip_button = Checkbutton(frame, variable=check_skip, onvalue=1, offvalue=0)
        skip_button.grid(column=1, row=1)

        submit = Button(frame, text="Save Settings", command=lambda: self.save_settings(top, bg_color, check_skip))
        submit.grid(column=0, row=2, columnspan=2)

    def save_settings(self, window, color, skip):
        if color.get() != "":
            # Connect to color socket
            color_args = ["save", color.get()]
            color_socket.send("`".join(color_args).encode("utf-8")[:1024])
            response1 = color_socket.recv(1024).decode("utf-8")

        # Connect to welcome socket
        skip_args = ["editskip", str(skip.get())]
        welcome_socket.send("`".join(skip_args).encode("utf-8")[:1024])
        response2 = welcome_socket.recv(1024).decode("utf-8").split("`")
        window.destroy()
        self.home()

    def welcome_popup(self):
        """
        UI to present information to user
        """
        top = Toplevel(self.window)
        top.title("Welcome Page")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        top.geometry(f'+{main_x}+{main_y}')

        display = Text(top)
        display.grid(column=0, row=0, columnspan=2, sticky='NSEW')

        # Connect to socket
        welcome_socket.send("read".encode("utf-8")[:1024])
        response = welcome_socket.recv(1024).decode("utf-8")

        display.insert(END, response)
        display.config(state=DISABLED)

        submit = Button(top, text="Skip on Next Opening", command=lambda: self.skip_welcome(top))
        submit.grid(column=0, row=1, columnspan=2)

    def skip_welcome(self, window):
        """
        Skip welcome page on next opening
        """
        # Connect to socket
        args = ["editskip", "1"]
        welcome_socket.send("`".join(args).encode("utf-8")[:1024])
        response = welcome_socket.recv(1024).decode("utf-8").split("`")
        window.destroy()

    def ingredients(self):
        """
        UI for the Pantry page
        """
        for i in self.window.winfo_children():
            i.destroy()
        self.window.grid_columnconfigure(0, weight=1, uniform="column")
        self.window.grid_columnconfigure(1, weight=1, uniform="column")
        self.window.grid_columnconfigure(2, weight=1, uniform="column")
        self.window.grid_columnconfigure(3, weight=1, uniform="column")
        self.window.grid_rowconfigure(0, weight=1, uniform="row", minsize=100)
        self.window.grid_rowconfigure(1, weight=1, uniform="row", minsize=100)
        self.window.grid_rowconfigure(2, weight=1, uniform="row", minsize=100)
        frame = Frame(self.window, width=win_width, height=win_height, bg=self.get_theme_color())
        frame.grid(column=0, row=0, columnspan=4, rowspan=4, sticky='NSEW')

        display = Text(self.window)
        display.grid(column=0, row=0, rowspan=3, columnspan=4, sticky='NSEW')

        # Connect to socket
        pantry_socket.send("read".encode("utf-8")[:1024])
        response = pantry_socket.recv(1024).decode("utf-8")

        display.insert(END, response)
        display.config(state=DISABLED)

        buttons = [
            Button(text="Add", command=lambda: self.new_ingredient_popup()),
            Button(text="Edit", command=lambda: self.edit_ingredient_popup()),
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

        submit = Button(top, text="Confirm", command=lambda: self.new_submit(top, args, self.ingredients))
        submit.grid(column=0, row=2, columnspan=2)

    def edit_ingredient_popup(self):
        """
        UI to edit an existing ingredient into the Pantry
        """
        top = Toplevel(self.window)
        top.title("New Ingredient")
        main_x = self.window.winfo_rootx() + win_width//4
        main_y = self.window.winfo_rooty() + win_height//3

        top.geometry(f'+{main_x}+{main_y}')

        # Connect to socket
        pantry_socket.send("dropdown".encode("utf-8")[:1024])
        response = pantry_socket.recv(1024).decode("utf-8").split("`")

        edit_item = StringVar()
        dropdown_options = OptionMenu(top, edit_item, *response)
        dropdown_options.grid(column=0, row=0)

        name_label = Label(top, text="Item Name")
        name_label.grid(column=0, row=1)
        name = Entry(top)
        name.grid(column=1, row=1)

        count_label = Label(top, text="Quantity")
        count_label.grid(column=0, row=2)
        count = Entry(top)
        count.grid(column=1, row=2)

        options = ["boxes", "units", "cans", "trays", "bags"]
        unit = StringVar()
        unit.set("units")

        units = OptionMenu(top, unit, *options)
        units.grid(column=2, row=2)

        args = ["ingredient", edit_item, name, count, unit]

        submit = Button(top, text="Confirm", command=lambda: self.edit_submit(top, args, self.ingredients))
        submit.grid(column=0, row=3, columnspan=2)

    def delete_ingredient_popup(self):
        """
            UI to delete ingredient
        """
        top = Toplevel(self.window)
        top.title("Delete Ingredient")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=300, height=100)
        frame.grid(column=0, row=0, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(0, minsize=300)

        top.geometry(f'+{main_x}+{main_y}')

        name_label = Label(frame, text="!! All deletions are permanent !!")
        name_label.grid(column=0, row=0)

        # Connect to socket
        pantry_socket.send("dropdown".encode("utf-8")[:1024])
        response = pantry_socket.recv(1024).decode("utf-8").split("`")

        clicked = StringVar()
        dropdown_options = OptionMenu(frame, clicked, *response)
        dropdown_options.grid(column=0, row=1)

        args = ["ingredient", clicked]

        submit = Button(frame, text="Confirm", command=lambda: self.delete_submit(top, args, self.ingredients))
        submit.grid(column=0, row=2)

    def recipes(self):
        """
        UI for the Recipe book page
        """
        for i in self.window.winfo_children():
            i.destroy()
        # Main Frame
        master_frame = Frame(self.window, width=win_width, height=win_height, bg=self.get_theme_color())
        master_frame.grid(column=0, row=0, columnspan=5, rowspan=4, sticky='NSEW')
        master_frame.grid_columnconfigure(0, weight=2, uniform="column")
        master_frame.grid_columnconfigure(1, weight=2, uniform="column")
        master_frame.grid_columnconfigure(2, weight=2, uniform="column")
        master_frame.grid_columnconfigure(3, weight=2, uniform="column")
        master_frame.grid_rowconfigure(0, weight=2, uniform="row")
        master_frame.grid_rowconfigure(1, weight=2, uniform="row")
        master_frame.grid_rowconfigure(2, weight=2, uniform="row")
        # Inner Frame to hold buttons and scroll bar
        inner_frame = Frame(master_frame, bg='Red')
        inner_frame.grid(row=0, column=0, columnspan=5, rowspan=3, sticky='NSEW')
        inner_frame.grid_columnconfigure(0, weight=2, uniform="column")
        inner_frame.grid_columnconfigure(1, weight=2, uniform="column")
        inner_frame.grid_columnconfigure(2, weight=2, uniform="column")
        inner_frame.grid_columnconfigure(3, weight=2, uniform="column")
        inner_frame.grid_rowconfigure(0, weight=2, uniform="row")
        inner_frame.grid_rowconfigure(1, weight=2, uniform="row")
        inner_frame.grid_rowconfigure(2, weight=2, uniform="row")
        # Canvas inside inner frame
        canvas = Canvas(inner_frame, bg=self.get_theme_color())
        canvas.grid(row=0, column=0, columnspan=5, rowspan=3, sticky='NSEW')
        # Scroll bar linked to canvas
        scroll = Scrollbar(inner_frame, orient=VERTICAL, command=canvas.yview)
        scroll.grid(row=0, column=4, rowspan=3, sticky='NS')
        canvas.configure(yscrollcommand=scroll.set)
        # Frame to contain buttons grid
        buttons_frame = Frame(canvas, bg=self.get_theme_color())
        buttons_frame.grid(row=0, column=0, sticky='NSEW')

        row = 0
        col = 0
        button_list = [[0 for j in range(20)] for i in range(20)]

        # Connect to socket
        recipe_socket.send("read".encode("utf-8")[:1024])
        response = recipe_socket.recv(1024).decode("utf-8").split("`")

        for recipe in response:
            button_list[row][col] = Button(buttons_frame, text=recipe, command=lambda x=recipe: self.recipe_popup(x))
            button_list[row][col].grid(column=col, row=row, sticky='NSEW')
            if col < 3:
                col += 1
            else:
                col = 0
                row += 1

        buttons_frame.grid_columnconfigure(0, weight=19, uniform="column")
        buttons_frame.grid_columnconfigure(1, weight=19, uniform="column")
        buttons_frame.grid_columnconfigure(2, weight=19, uniform="column")
        buttons_frame.grid_columnconfigure(3, weight=19, uniform="column")
        for row_num in range(buttons_frame.grid_size()[1]):
            buttons_frame.grid_rowconfigure(row_num, weight=1, uniform="row", minsize=100)

        canvas.create_window((0, 0), window=buttons_frame)
        buttons_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        buttons = [
            Button(master_frame, text="Add", command=lambda: self.new_recipe_popup()),
            Button(master_frame, text="Edit", command=lambda: self.edit_recipe_popup()),
            Button(master_frame, text="Delete", command=lambda: self.delete_recipe_popup()),
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
        # Connect to socket
        recipe_socket.send(f"search`{recipe}".encode("utf-8")[:1024])
        response = recipe_socket.recv(1024).decode("utf-8").split("`")

        top = Toplevel(self.window)
        top.title("View Recipe")
        name_label = Label(top, text="Recipe Name")
        name_label.grid(column=0, row=0)
        name = Entry(top)
        name.insert(0, response[0])
        name.grid(column=1, row=0)
        name.configure(state='disabled')

        info_label = Label(top, text="Description")
        info_label.grid(column=0, row=1)
        info = Text(top)
        info.insert('end', response[1])
        info.grid(column=1, row=1)
        info.configure(state='disabled')

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

        submit = Button(top, text="Confirm", command=lambda: self.new_submit(top, args, self.recipes))
        submit.grid(column=0, row=2, columnspan=2)

    def edit_recipe_popup(self):
        """
        UI to edit an existing recipe in the Recipe book
        """
        top = Toplevel(self.window)
        top.title("New Recipe")

        # Connect to socket
        recipe_socket.send("dropdown".encode("utf-8")[:1024])
        dropdown_response = recipe_socket.recv(1024).decode("utf-8").split("`")

        edit_item = StringVar()
        dropdown_options = OptionMenu(top, edit_item, *dropdown_response)
        dropdown_options.grid(column=0, row=0)

        name_label = Label(top, text="Recipe Name")
        name_label.grid(column=0, row=1)
        name = Entry(top)
        name.grid(column=1, row=1)

        info_label = Label(top, text="Description")
        info_label.grid(column=0, row=2)
        info = Text(top)
        info.grid(column=1, row=2)

        args = ["recipe", edit_item, name, info]

        submit = Button(top, text="Confirm", command=lambda: self.edit_submit(top, args, self.recipes))
        submit.grid(column=0, row=3, columnspan=2)

    def delete_recipe_popup(self):
        """
            UI to delete a recipe
        """
        top = Toplevel(self.window)
        top.title("Delete Recipe")
        main_x = self.window.winfo_rootx() + win_width // 4
        main_y = self.window.winfo_rooty() + win_height // 3

        frame = Frame(top, width=300, height=100)
        frame.grid(column=0, row=0, rowspan=3, sticky='NSEW')
        frame.grid_columnconfigure(0, minsize=300)

        top.geometry(f'+{main_x}+{main_y}')

        name_label = Label(frame, text="!! All deletions are permanent !!")
        name_label.grid(column=0, row=0)

        # Connect to socket
        recipe_socket.send("dropdown".encode("utf-8")[:1024])
        response = recipe_socket.recv(1024).decode("utf-8").split("`")

        clicked = StringVar()
        dropdown_options = OptionMenu(frame, clicked, *response)
        dropdown_options.grid(column=0, row=1)

        args = ["recipe", clicked]

        submit = Button(frame, text="Confirm", command=lambda: self.delete_submit(top, args, self.recipes))
        submit.grid(column=0, row=2)

    def new_submit(self, window, args, reload):
        """
        Submits user inputs and refreshes the page
        :param window: window to be closed
        :param args: arguments to be sent to the microservice
        :param reload: window to be refreshed
        """
        if args[0] == "ingredient":
            # Connect to socket
            args = ["new", args[1].get(), args[2].get(), args[3].get()]
            pantry_socket.send("`".join(args).encode("utf-8")[:1024])
            response = pantry_socket.recv(1024).decode("utf-8").split("`")
        elif args[0] == "recipe":
            # Connect to socket
            args = ["new", args[1].get(), args[2].get(1.0, "end-1c")]
            recipe_socket.send("`".join(args).encode("utf-8")[:1024])
            response = recipe_socket.recv(1024).decode("utf-8").split("`")
        else:
            pass
        window.destroy()
        reload()

    def edit_submit(self, window, args, reload):
        """
        Submits user inputs and refreshes the page
        :param window: window to be closed
        :param args: arguments to be sent to the microservice
        :param reload: window to be refreshed
        """
        if args[0] == "ingredient":
            # Connect to socket
            args = ["edit", args[1].get(), args[2].get(), args[3].get(), args[4].get()]
            pantry_socket.send("`".join(args).encode("utf-8")[:1024])
            response = pantry_socket.recv(1024).decode("utf-8").split("`")
        elif args[0] == "recipe":

            print(f"This is the thing {type(args[1].get())}.")
            # Connect to socket
            args = ["edit", args[1].get(), args[2].get(), args[3].get(1.0, "end-1c")]
            recipe_socket.send("`".join(args).encode("utf-8")[:1024])
            response = recipe_socket.recv(1024).decode("utf-8").split("`")
        else:
            pass
        window.destroy()
        reload()

    def delete_submit(self, window, args, reload):
        """
        Submits user inputs and refreshes the page
        :param window: window to be closed
        :param args: arguments to be sent to the microservice
        :param reload: window to be refreshed
        """
        if args[0] == "ingredient":
            # Connect to socket
            args = ["delete", args[1].get()]
            pantry_socket.send("`".join(args).encode("utf-8")[:1024])
            response = pantry_socket.recv(1024).decode("utf-8").split("`")
        elif args[0] == "recipe":
            # Connect to socket
            args = ["delete", args[1].get()]
            recipe_socket.send("`".join(args).encode("utf-8")[:1024])
            response = recipe_socket.recv(1024).decode("utf-8").split("`")
        else:
            pass
        window.destroy()
        reload()


recipe_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recipe_socket.connect((SERVER_IP, RECIPE_PORT))

pantry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pantry_socket.connect((SERVER_IP, PANTRY_PORT))

welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_socket.connect((SERVER_IP, WELCOME_PORT))

color_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
color_socket.connect((SERVER_IP, COLOR_PORT))

pantry_ui = UserInterface()
