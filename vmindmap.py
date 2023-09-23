from typing import Optional, Dict

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from vmind import VMind, DEL


class VMindMap(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("VMind")

        self.vmind: VMind = VMind()

        self.root.bind('<Escape>', self.shutdown)

        self.t_frame = tk.Frame(self.root)
        self.t_frame.pack(side=tk.TOP, fill=tk.X)
        self.b_frame = tk.Frame(self.root)
        self.b_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button_new = tk.Button(self.t_frame, text="new", command=self.cb_button_new)
        self.button_new.pack(side=tk.LEFT)
        self.button_load = tk.Button(self.t_frame, text="load", command=self.cb_button_load)
        self.button_load.pack(side=tk.LEFT)
        self.button_save = tk.Button(self.t_frame, text="save", command=self.cb_button_save)
        self.button_save.pack(side=tk.LEFT)

        self.var_vmind_folder = tk.StringVar()
        self.label_vmind_folder = tk.Label(self.t_frame, textvariable=self.var_vmind_folder)
        self.var_vmind_folder.set("  None  ")
        self.label_vmind_folder.pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self.b_frame)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # create frames
        self.tab = dict()
        self.tab['overview'] = dict()
        self.tab['overview']['tab'] = ttk.Frame(self.notebook)
        self.tab['overview']['tab'].pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.tab['overview']['tab'], text='overview')

    def main(self):
        self.root.mainloop()

    def cb_button_new(self):
        """Create template vmind and first commit."""
        folder_name = filedialog.askdirectory(mustexist=True) + DEL
        if len(folder_name) > 1:
            self.vmind.new(vmind_path=folder_name)
            self.var_vmind_folder.set(folder_name)
            self.create_overview()

    def cb_button_load(self):
        folder_name = filedialog.askdirectory(mustexist=True) + DEL
        self.vmind.load(load_path=folder_name)
        self.var_vmind_folder.set(folder_name)
        self.create_overview()

    def cb_button_save(self):
        # DEPRECATED
        pass

    def create_overview(self):
        tab = self.tab['overview']
        # tabula rasa on overview notebook tab
        tab['note-frame'] = {}
        tab['title-var'] = {}
        tab['title-entry'] = {}
        if 'frame' in tab:
            tab['frame'].destroy()
        tab['frame'] = tk.Frame(tab['tab'])
        tab['frame'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # build overview
        for note_id, note_spec in self.vmind.notes.items():
            note_sep = ttk.Separator(tab['frame'], orient='horizontal')
            note_sep.pack(fill=tk.X)
            # create note-frame
            note_frame = tk.Frame(tab['frame'])
            note_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
            title_entry_var = tk.StringVar(tab['frame'])
            title_entry_var.set(note_spec['title'])
            title_entry = tk.Entry(note_frame, textvariable=title_entry_var)
            title_entry.bind("<Return>", lambda event, this_note_id=note_id: self.tab_overview_title_entry(this_note_id))
            title_entry.pack(side=tk.TOP)
            tab['title-var'][note_id] = title_entry_var
            tab['title-entry'][note_id] = title_entry_var
            tab['note-frame'][note_id] = note_frame

    def tab_overview_title_entry(self, note_id):
        # update title
        new_title = self.tab['overview']['title-var'][note_id].get()
        self.vmind.edit_note_title(note_id=note_id, title=new_title)

    def shutdown(self, event):
        self.root.destroy()


def main():
    vmm = VMindMap()
    vmm.main()


if __name__ == "__main__":
    main()
