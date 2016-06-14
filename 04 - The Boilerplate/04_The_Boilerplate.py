import Tkinter as tk
import AppKit
import subprocess


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("Hello World")
        # self.master.call('wm', 'attributes', '.', '-topmost', True)
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#ececec')
        self.master.protocol('WM_DELETE_WINDOW', self.click_cancel)
        self.master.bind('<Return>', self.click_ok)
        self.master.bind('<Escape>', self.click_cancel)

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

    def click_ok(self, event=None):
        print("The user clicked 'OK'")

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
There are a few items left to address before we have a working GUI that matches the standard macOS dialogs. When running
a Python app using Tkinter the Python launcher's icon will appear in the Dock. This can be dynamically flagged to run
without the Dock icon by loading and manupulating the launcher's 'Info.plist' before the main window has been created.
'AppKit' will be used in our main function to do this.

Lastly, to allow the user to control the window as they would any other macOS dialog, we will bind the '<Return>' and
'<Escape>' keys to our 'OK' and 'Cancel' methods. We will also override the function of the close button on the GUI
window to point to our 'Cancel' method to keep control of the teardown.

Because we are now using alternative triggers for these funtions we must add an 'event' parameter to accept the callback
that is passed by the binding. The default value is set to 'None' for when the buttons are used.
"""
