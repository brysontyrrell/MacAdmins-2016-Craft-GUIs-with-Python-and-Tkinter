import Tkinter as tk
import tkSimpleDialog
import AppKit
import subprocess


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("")
        self.master.call('wm', 'attributes', '.', '-topmost', True)
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')
        self.master.protocol('WM_DELETE_WINDOW', self.click_cancel)
        self.master.bind('<Return>', self.click_ok)
        self.master.bind('<Escape>', self.click_cancel)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        message_frame = tk.Frame(self.master)
        message = tk.Message(
            message_frame,
            text="Please authenticate with your username and password before continuing.",
            font='System 14 bold',
            justify='left',
            width=300
        )
        message.pack()
        message_frame.pack(pady=(15, 0))

        dialog_frame = tk.Frame(self.master)
        user_label = tk.Label(dialog_frame, text='Username:')
        self.user_input = tk.Entry(dialog_frame, background='white', width=24)
        user_label.grid(row=0, column=0, sticky='w')
        self.user_input.grid(row=0, column=1, sticky='w')
        pass_label = tk.Label(dialog_frame, text='Password:')
        self.pass_input = tk.Entry(dialog_frame, background='white', width=24, show='*')
        pass_label.grid(row=1, column=0, sticky='w')
        self.pass_input.grid(row=1, column=1, sticky='w')
        dialog_frame.pack(padx=20, pady=15, anchor='w')

        button_frame = tk.Frame(self.master)
        ok = tk.Button(button_frame, text='OK', height=1, width=6, default='active', command=self.click_ok)
        cancel = tk.Button(button_frame, height=1, width=6, text='Cancel', command=self.click_cancel)
        ok.pack(side='right')
        cancel.pack(side='right', padx=10)
        button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        self.user_input.focus_set()
        self.pack()

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
    root.grab_set()
    root.focus_force()
    app.mainloop()

"""
Multiple inputs are an issue with using AppleScript. You must prompt a user with multiple windows in a row and write
error handling in the event a user skips past one window or enters an incorrect value and must be prompted again.

The Tkinter.EntryBox can be used to capture plain and protected text from a user. Using .focus_set() on a widget will
set it as the active element in the GUI.

Here frames are being used again using the grid method instead of the pack method. Grid allows for a defined layout of
the frames while the widgets can be packed within each frame.
"""
