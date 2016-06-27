import Tkinter as tk
import AppKit
import subprocess
import tkFileDialog
import ttk
import time


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master.title("File Upload Assistant")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#e6e6e6')

        self.master.protocol('WM_DELETE_WINDOW', self.click_cancel)
        self.master.bind('<Escape>', self.click_cancel)

        self.grid(row=0, column=0)

        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        self.master.geometry("+{}+{}".format(x, y))

        self.master.config(menu=tk.Menu(self.master))

        self.selected_files = tuple()
        self.file_count = tk.StringVar(value='')

        file_frame = tk.Frame(self)
        file_frame.pack(padx=15, pady=(15, 0), anchor='w')

        self.file_button = tk.Button(file_frame, text='Select file(s)...', command=self.file_picker, anchor='w')
        self.file_button.pack(side='left')

        self.file_label = tk.Label(file_frame, textvariable=self.file_count, anchor='e')
        self.file_label.pack(side='right')

        tk.Label(self, text="Add a comment:").pack(padx=15, pady=(15, 0), anchor='w')

        text_frame = tk.Frame(self, borderwidth=1, relief='sunken')
        text_frame.pack(padx=15, pady=15)

        self.text = tk.Text(text_frame, width=30, height=4, highlightbackground='#ffffff', highlightcolor="#7baedc",
                            bg='#ffffff', wrap=tk.WORD, font=("System", 14))
        self.text.focus_set()
        self.text.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        self.submit_button = tk.Button(button_frame, text='Submit', default='active', command=self.click_submit)
        self.submit_button.pack(side='right')

        self.cancel_button = tk.Button(button_frame, text='Cancel', command=self.click_cancel)
        self.cancel_button.pack(side='right')

    def file_picker(self):
        self.selected_files = tkFileDialog.askopenfilenames(parent=self)
        self.file_count.set('{} file(s)'.format(len(self.selected_files)))

    def click_submit(self, event=None):
        print("The user clicked 'OK'")
        comment = self.text.get('1.0', 'end')

        if comment.rstrip():
            print('The user entered a comment:')
            print(comment.rstrip())

        if self.selected_files:
            loading = LoadingFrame(self.master, len(self.selected_files))
            self._toggle_state('disabled')
            print('The user has selected files:')
            for path in self.selected_files:
                loading.progress['value'] += 1
                self.update()
                print 'File {}/{}'.format(loading.progress['value'], loading.progress['maximum'])
                time.sleep(2)
                with open(path) as f:
                    print('Opened file: {}: {}'.format(path, f))

            print('Loading screen finished')
            loading.destroy()
            self._toggle_state('normal')

    def click_cancel(self, event=None):
        print("The user clicked 'Cancel'")
        self.master.destroy()

    def _toggle_state(self, state):
        state = state if state in ('normal', 'disabled') else 'normal'
        widgets = (self.file_button, self.file_label, self.text, self.submit_button, self.cancel_button)
        for widget in widgets:
            widget.configure(state=state)


class LoadingFrame(tk.Frame):
    def __init__(self, master, count):
        tk.Frame.__init__(self, master, borderwidth=5, relief='groove')
        self.grid(row=0, column=0)

        tk.Label(self, text="Your files are being uploaded").pack(padx=15, pady=10)

        self.progress = ttk.Progressbar(self, orient='horizontal', length=250, mode='determinate')
        self.progress.pack(padx=15, pady=10)
        self.progress['value'] = 0
        self.progress['maximum'] = count


if __name__ == '__main__':
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info['LSUIElement'] = True

    root = tk.Tk()
    app = App(root)
    subprocess.call(['/usr/bin/osascript', '-e', 'tell app "Finder" to set frontmost of process "Python" to true'])
    app.mainloop()

"""
The Tkinter framework comes with a number of standard dialogs that can be used on their own or with a Tkinter window.

Passing the main window as the 'parent' to the tkFileDialog causes it to render as a sheet on OS X. All of the dialogs
available as a part of tkFileDialog, tkColorChooser or tkMessageBox support this.

Widgets can be dynamically enabled and disabled to prevent a user from interacting with them while an action is being
processed. In this example when the LoadingFrame() is drawn on the screen the _toggle_state() function is disabling all
of the interactive widgets.

The progress bar in this example moves for each file that is being uploaded (an artificial 2 second delay is introduced
to simulate the wait during an upload). The frame is then destroyed after the last file progresses and the background
frame is restored for use again.
"""
