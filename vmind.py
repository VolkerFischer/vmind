from typing import Optional, Dict

import tkinter as tk
from tkinter import filedialog

import yaml


class VMind(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")
        self.root.title("VMind")

        self.vmind_filename: Optional[str] = None
        self.vmind: Optional[Dict] = None

        self.t_frame = tk.Frame(self.root)
        self.t_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.b_frame = tk.Frame(self.root)
        self.b_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.button_load = tk.Button(self.t_frame, text="load", command=self.cb_button_load)
        self.button_load.pack(side=tk.LEFT)
        self.button_save = tk.Button(self.t_frame, text="save", command=self.cb_button_save)
        self.button_save.pack(side=tk.LEFT)

        self.var_vmind_filename = tk.StringVar()
        self.label_vmind_filename = tk.Label(self.t_frame, textvariable=self.var_vmind_filename)
        self.var_vmind_filename.set("  None  ")
        self.label_vmind_filename.pack(side=tk.LEFT)

    def main(self):
        self.root.mainloop()

    def cb_button_load(self):
        filename = filedialog.askopenfile(mode='r')
        self.vmind_filename = filename.name
        with open(self.vmind_filename, 'r') as vmind_file:
            self.vmind = yaml.safe_load(vmind_file)

    def cb_button_save(self):
        filename = filedialog.asksaveasfile(
            initialfile='my_vmind.yml',
            defaultextension=".yml",
            filetypes=[("All Files", "*.*"), ("YML Documents", "*.yml")],
        )
        if self.vmind is not None:
            self.vmind_filename = filename.name
            with open(self.vmind_filename, 'w') as vmind_file:
                yaml.safe_dump(self.vmind, vmind_file)


def main():
    vmind = VMind()
    vmind.main()


if __name__ == "__main__":
    main()
