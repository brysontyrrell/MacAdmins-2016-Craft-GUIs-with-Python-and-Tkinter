import Tkinter as tk
import subprocess


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Hello World")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        self.master.geometry("+{}+{}".format(x, y))

        self.master.config(menu=tk.Menu(self.master))

        tk.Label(self, text="This is your first GUI. (highfive)").pack()

        tk.Button(self, text='OK', default='active', command=self.click_ok).pack(side='right')

        tk.Button(self, text='Cancel', command=self.click_cancel).pack(side='right')

    def click_ok(self):
        print("The user clicked 'OK'")

    def click_cancel(self):
        print("The user clicked 'Cancel'")
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    subprocess.call(['/usr/bin/osascript', '-e', 'tell app "Finder" to set frontmost of process "Python" to true'])
    app.mainloop()

"""
Dialogs aren't useful without interaction, so our first add-on to our basic dialog modal will be a couple of standard
'OK' / 'Cancel' buttons. Notice that we've passed an key value of 'default="active"' to the OK button to make it
highlighted when the window is active.

The way these buttons are being packed stacks them, in order of which is packed first, from the right to the left on the
window. 'OK' is first to it is against the right side of the GUI window. 'Cancel' is second so it stacks right up
against 'OK'.

Clicking 'OK' right now will only display a message in STDOUT. Clicking 'Cancel' will close the GUI by calling the
'destroy()' method of the parent (our root Tkinter.Tk object).
"""
