import Tkinter as tk
import subprocess


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Hello World")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        dialog_frame = tk.Frame(self.master)
        text = tk.Label(dialog_frame, text="This is your first GUI. (highfive)")
        text.pack()
        dialog_frame.pack(padx=20, pady=15)

        button_frame = tk.Frame(self.master)
        ok = tk.Button(button_frame, text='OK', default='active', command=self.click_ok)
        cancel = tk.Button(button_frame, text='Cancel', command=self.click_cancel)
        ok.pack(side='right')
        cancel.pack(side='right')
        button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        self.pack()

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
Packing widgets one on top of another, even with using the 'side' argument, only gets us GUIs that are structured
top-down and not very flexible. Tkinter uses the Tkinter.Frame object to organize widgets together. By using frames a
GUI can be given a more sophisticated layout without complicating code and uniform spacing around groups of widgets.
"""
