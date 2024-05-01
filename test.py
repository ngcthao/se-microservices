import tkinter as tk

LABEL_BG = 'light grey'
ROWS, COLS = 10, 6  # Size of grid.
ROWS_DISP = 3  # Number of rows to display.
COLS_DISP = 4  # Number of columns to display.


class HoverButton(tk.Button):
    """ Button that changes color to activebackground when mouse is over it. """

    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.default_Background = self.cget('background')
        self.hover_Background = self.cget('activebackground')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(background=self.hover_Background)

    def on_leave(self, e):
        self.config(background=self.default_Background)


class MyApp(tk.Tk):
    def __init__(self, title='Sample App', *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title(title)
        self.configure(background='Gray')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        master_frame = tk.Frame(self, bg='Light Blue', bd=3, relief=tk.RIDGE)
        master_frame.grid(sticky=tk.NSEW)
        master_frame.columnconfigure(0, weight=1)

        # Create a frame for the canvas and scrollbar(s).
        frame2 = tk.Frame(master_frame, bg='Red', bd=2, relief=tk.FLAT)
        frame2.grid(row=3, column=0, sticky=tk.NW)

        # Add a canvas in that frame.
        canvas = tk.Canvas(frame2, bg='Yellow')
        canvas.grid(row=0, column=0)

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)

        # Add the buttons to the frame.
        for i in range(1, ROWS+1):
            for j in range(1, COLS+1):
                button = HoverButton(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                     activebackground= 'orange', text='[%d, %d]' % (i, j))
                button.grid(row=i, column=j, sticky='news')

        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)


if __name__ == '__main__':
    app = MyApp('Scrollable Canvas')
    app.mainloop()
