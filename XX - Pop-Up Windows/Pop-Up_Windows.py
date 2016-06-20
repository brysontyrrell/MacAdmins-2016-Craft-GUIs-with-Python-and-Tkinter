class Popup(tk.Toplevel):
    def __init__(self, parent, message):
        tk.Toplevel.__init__(self, parent, padx=15, pady=15)
        self.transient(parent)
        self.overrideredirect(True)
        self.parent = parent
        body = tk.Frame(self)
        tk.Label(body, text=message).pack()
        tk.Button(body, text='OK', height=1, width=6, default='active', command=self.ok).pack(anchor='e')
        h = body.winfo_height()
        body.pack()

        self.focus_force()
        self.grab_set()
        self.geometry("{}x{}+{}+{}".format(
            int(parent.winfo_width() * .67), int(parent.winfo_height() / 2),
            parent.winfo_rootx() + (parent.winfo_width() / 6), parent.winfo_rooty() + (parent.winfo_height() / 4)
        ))
        self.wait_window(self)

    def ok(self):
        self.parent.focus_set()
        self.destroy()