import Tkinter as tk
import ttk


class LabelApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, text="This is a label").pack()


class MessageApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut " \
                      "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                      "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                      "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat " \
                      "cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        tk.Label(self, text="This is a message (under a label)").pack()

        tk.Message(self, text=lorem_ipsum, justify='left').pack(pady=(10, 10))


class ButtonApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, text="This is a button").pack()

        tk.Button(self, text='OK', command=self.ok).pack()

    def ok(self):
        print('OK')


class EntryApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, text="This is a normal text entry box").pack()

        self.entry = tk.Entry(self, bg='white')
        self.entry.pack()

        tk.Label(self, text="This is a secret text entry box for passwords").pack()

        self.secret_entry = tk.Entry(self, show='*', bg='white')
        self.secret_entry.pack()

        tk.Button(self, text='OK', command=self.ok).pack()

    def ok(self):
        print('Text box: {}\nSecret box: {}'.format(self.entry.get(), self.secret_entry.get()))


class ListApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, text="This is a listbox").pack()

        list_items = ["This is a listbox!", 'Item 1', 'Item 2', 'Item 3', 'etc.']

        self.listbox = tk.Listbox(self, selectmode='extended', bg='white')
        self.listbox.pack(padx=10, pady=10)

        for l in list_items:
            self.listbox.insert('end', l)

        tk.Button(self, text='OK', command=self.ok).pack()

    def ok(self):
        selection = self.listbox.curselection()
        value = ', '.join(self.listbox.get(x) for x in selection)
        print('Listbox Selection: {} "{}"'.format(selection, value))


class TextApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        tk.Label(self, text="This is a text box").pack()

        text_frame = tk.Frame(self, borderwidth=1, relief='sunken')
        text_frame.pack(padx=10, pady=10)

        self.text = tk.Text(text_frame, width=30, height=4, wrap=tk.WORD)
        self.text.pack()

        tk.Button(self, text='OK', command=self.ok).pack()

    def ok(self):
        print('Text box:\n{}'.format(self.text.get('1.0', 'end').rstrip()))


class CheckbuttonApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()

        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()

        tk.Label(self, text="These are checkbuttons").pack()

        tk.Checkbutton(self, text='Pick me!', variable=self.var1, command=self.checked).pack()

        tk.Checkbutton(self, text='Or pick me!', variable=self.var2, command=self.checked).pack()

        tk.Button(self, text='OK', command=self.ok).pack()

    def checked(self):
        print('A checkbutton was toggled')

    def ok(self):
        print('Checkbutton 1: {}\nCheckbutton 2: {}'.format(self.var1.get(), self.var2.get()))


class RadiobuttonApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(padx=20, pady=20)

        self.master = master

        self.selection = tk.StringVar()
        self.selection.set('white')

        tk.Label(self, text="These are radiobuttons").pack()

        tk.Radiobutton(self, text='White', value='white', variable=self.selection, command=self.set_color).pack(anchor='w')

        tk.Radiobutton(self, text='Red', value='red', variable=self.selection, command=self.set_color).pack(anchor='w')

        tk.Radiobutton(self, text='Green', value='green', variable=self.selection, command=self.set_color).pack(anchor='w')

        tk.Radiobutton(self, text='Blue', value='blue', variable=self.selection, command=self.set_color).pack(anchor='w')

    def set_color(self):
        new_color = self.selection.get()
        print('New selected color: {}'.format(new_color))
        self.master.configure(background=new_color)


class OptionMenuApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(padx=20, pady=20)

        self.master = master

        options = ['white', 'red', 'green', 'blue']

        self.selection = tk.StringVar()
        self.selection.set('White')

        tk.Label(self, text="This is an optionmenu").pack()

        tk.OptionMenu(self, self.selection, *[x.capitalize() for x in options], command=self.set_color).pack()

    def set_color(self, event):
        new_color = self.selection.get()
        print('New selected color: {}'.format(new_color))
        self.master.configure(background=new_color)


class ProgressBarApp(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        ttk.Label(self, text="This is an 'indeterminate' progress bar").pack(padx=20, pady=10)

        progress1 = ttk.Progressbar(self, orient='horizontal', length=500, mode='indeterminate')
        progress1.pack(padx=20, pady=10)

        ttk.Label(self, text="This is a 'determinate' progress bar").pack(padx=20, pady=10)

        progress2 = ttk.Progressbar(self, orient='horizontal', length=500, mode='determinate')
        progress2.pack(padx=20, pady=10)

        progress1.start()
        progress2.start()


class ComboboxApp(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        options = ['Minneapolis', 'Eau Claire', 'Cupertino', 'New York', 'Amsterdam', 'Sydney', 'Hong Kong']

        ttk.Label(self, text="This is a combobox").pack(pady=10)

        self.combo = ttk.Combobox(self, values=options, state='readonly')
        self.combo.current(0)
        self.combo.pack(padx=15)

        ttk.Button(self, text='OK', command=self.ok).pack(side='right', padx=15, pady=10)

    def ok(self):
        print('Selection: {}'.format(self.combo.get()))


class Voltron(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(padx=15, pady=15)
        self.master.title("Voltron")
        self.master.resizable(False, False)
        self.master.tk_setPalette(background='#e6e6e6')

        frame1 = tk.Frame(self)
        frame1.grid(row=0, column=0, columnspan=2)

        ProgressBarApp(frame1)

        frame2 = tk.Frame(self)
        frame2.grid(row=1, column=0)

        EntryApp(frame2)

        frame3 = tk.Frame(self)
        frame3.grid(row=1, column=1)

        ComboboxApp(frame3)

        frame4 = tk.Frame(self)
        frame4.grid(row=2, column=0, rowspan=2)

        ListApp(frame4)

        frame5 = tk.Frame(self)
        frame5.grid(row=2, column=1)

        OptionMenuApp(frame5)

        frame6 = tk.Frame(self)
        frame6.grid(row=3, column=1)

        RadiobuttonApp(frame6)


if __name__ == '__main__':
    root = tk.Tk()

    tk.Message(
        root, text='Close this window when you are done looking at the example pop-ups.'
    ).pack(
        anchor='center', padx=100, pady=100
    )

    top1 = tk.Toplevel(root)
    LabelApp(top1)

    top2 = tk.Toplevel(root)
    MessageApp(top2)

    top3 = tk.Toplevel(root)
    ButtonApp(top3)

    top4 = tk.Toplevel(root)
    EntryApp(top4)

    top5 = tk.Toplevel(root)
    ListApp(top5)

    top6 = tk.Toplevel(root)
    RadiobuttonApp(top6)

    top7 = tk.Toplevel(root)
    OptionMenuApp(top7)

    top8 = tk.Toplevel(root)
    ProgressBarApp(top8)

    top9 = tk.Toplevel(root)
    ComboboxApp(top9)

    top10 = tk.Toplevel(root)
    Voltron(top10)

    root.mainloop()