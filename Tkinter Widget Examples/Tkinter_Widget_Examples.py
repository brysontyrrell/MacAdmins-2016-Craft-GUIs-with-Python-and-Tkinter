import Tkinter as tk


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

        self.entry = tk.Entry(self)
        self.entry.pack()

        tk.Label(self, text="This is a secret text entry box for passwords").pack()

        self.secret_entry = tk.Entry(self, show='*')
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

        self.listbox = tk.Listbox(self, selectmode='extended')
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

    root.mainloop()