import Tkinter as tk


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Hello World")

        text = tk.Label(self, text="This is your first GUI. (highfive)")
        text.pack()

        self.pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()

"""
The most basic Tkinter example.

There are a lot of ways around the web that show you how to init a basic Tkinter GUI. This combination of creating
the root Tkinter.Tk object from the main function and passing it into a class that sub-classes Tkinter.Frame is what
I have settled on personally. There are many ways to accomplish this for simple Tkinter GUIs.
"""
