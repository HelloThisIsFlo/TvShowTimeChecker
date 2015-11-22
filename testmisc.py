from tkinter import Tk
from tkinter.filedialog import askdirectory

""" Some random tests """

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = askdirectory()  # show an "Open" dialog box and return the path to the selected file
print(filename)
