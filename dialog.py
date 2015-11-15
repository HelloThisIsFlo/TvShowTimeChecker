from Tkinter import Tk, Label, Entry, Button


# Decorator to create a new instance of TK every time
def init_decorator(func):
    def inner_func(self, hint):
        # Create new Tk
        self.top = Tk()
        # Create the desired UI element
        func(self, hint)
        # Start main loop
        self.top.mainloop()

    return inner_func


class Dialog:
    def __init__(self):
        # Init the member variable variable
        self.top = None
        self.result = ""

    @init_decorator
    def make_input_dialog(self, hint):
        # Create the views
        entry = Entry(self.top)
        label = Label(self.top, text=hint)

        def print_entry():
            self.result = entry.get()
            self.top.quit()

        button = Button(self.top, command=print_entry, text="Ok")

        # Setup the views
        entry.grid(row=0, column=1)
        label.grid(row=0, column=0)
        button.grid(row=1, column=0)

    @init_decorator
    def make_ok_dialog(self, hint):
        # Create the views
        label = Label(self.top, text=hint)
        button = Button(self.top, command=self.top.quit, text="Ok")

        # Setup the views
        label.pack()
        button.pack()



