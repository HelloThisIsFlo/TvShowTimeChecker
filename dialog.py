from Tkinter import Tk, Label, Entry, Button


class Dialog:
    def __init__(self, hint="Input : "):
        self.top = Tk()

        # Create the views
        self.E1 = Entry(self.top)
        self.L1 = Label(self.top, text=hint)
        self.B1 = Button(self.top, command=self.print_entry, text="Ok")

        # Setup the views
        self.E1.grid(row=0, column=1)
        self.L1.grid(row=0, column=0)
        self.B1.grid(row=1, column=0)

    def print_entry(self):
        print "Search text = {text}".format(text=self.E1.get())
        self.top.quit()

    def show(self):
        self.top.mainloop()
