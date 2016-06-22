import Tkinter as tk
import AppKit
import subprocess


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')

        self.master.protocol('WM_DELETE_WINDOW', self.click_cancel)
        self.master.bind('<Return>', self.click_ok)
        self.master.bind('<Escape>', self.click_cancel)

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        self.master.geometry("+{}+{}".format(x, y))

        self.master.config(menu=tk.Menu(self))

        tk.Message(self, text="Please authenticate with your username and password before continuing.",
                   font='System 14 bold', justify='left', aspect=800).pack(pady=(15, 0))

        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20, pady=15, anchor='w')

        tk.Label(dialog_frame, text='Username:').grid(row=0, column=0, sticky='w')

        self.user_input = tk.Entry(dialog_frame, background='white', width=24)
        self.user_input.grid(row=0, column=1, sticky='w')
        self.user_input.focus_set()

        tk.Label(dialog_frame, text='Password:').grid(row=1, column=0, sticky='w')

        self.pass_input = tk.Entry(dialog_frame, background='white', width=24, show='*')
        self.pass_input.grid(row=1, column=1, sticky='w')

        button_frame = tk.Frame(self)
        button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        tk.Button(button_frame, text='OK', height=1, width=6, default='active', command=self.click_ok).pack(side='right')

        tk.Button(button_frame, text='Cancel', height=1, width=6, command=self.click_cancel).pack(side='right', padx=10)

    def click_ok(self, event=None):
        print("The user clicked 'OK':\nUsername: {}\nPassword: {}".format(self.user_input.get(), self.pass_input.get()))
        self.master.destroy()

    def click_cancel(self, event=None):
        print("The user clicked 'Cancel'")
        self.master.destroy()


if __name__ == '__main__':
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info['LSUIElement'] = True

    root = tk.Tk()
    app = App(root)
    subprocess.call(['/usr/bin/osascript', '-e', 'tell app "Finder" to set frontmost of process "Python" to true'])
    app.mainloop()

"""
Multiple inputs are an issue with using AppleScript. You must prompt a user with multiple windows in a row and write
error handling in the event a user skips past one window or enters an incorrect value and must be prompted again.

The Tkinter.EntryBox can be used to capture plain and protected text from a user. Using .focus_set() on a widget will
set it as the active element in the GUI.

Here frames are being used again using the grid method instead of the pack method. Grid allows for a defined layout of
the frames while the widgets can be packed within each frame.
"""
