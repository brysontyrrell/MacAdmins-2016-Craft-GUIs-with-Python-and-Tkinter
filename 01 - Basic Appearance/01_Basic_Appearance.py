import Tkinter as tk


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Hello World")
        self.master.call('wm', 'attributes', '.', '-topmost', True)
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')  # '#ececec' is the standard gray background of El Capitain

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        text = tk.Label(self, text="This is your first GUI. (highfive)")
        text.pack()

        self.pack()


if __name__ == '__main__':
    """When launched the GUI is placed behind our active application window, has a white background and can be re-sized
    by the user. The three lines added below the title correct these elements to force the window on top of all other
    windows, prevent resizing of the window and set the background color to match the default for macOS.

    Our GUI will also load with a default menubar selection. This can be suppressed by creating an instance of
    Tkinter.Menu without any items and then adding it to our GUI's root configuration."""
    root = tk.Tk()
    app = App(root)
    app.mainloop()
