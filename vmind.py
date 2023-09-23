from typing import Optional, Dict

import os
import sys

# determine folder delimiter dependent on system platform
DEL = None
if sys.platform.startswith('win'):
    DEL = '/'
elif sys.platform.startswith('linux'):
    DEL = '\\'
else:
    raise ValueError('Unknown system platform: ' + str(sys.platform))


class VMind(object):
    def __init__(self):
        # path to vmind git folder
        self.vmind_path: Optional[str] = None

        # name of the vmind
        self.name: Optional[str] = None
        # dictionary of all notes
        self.notes: Dict[str: Dict] = {}

    def notes_folder(self) -> str:
        return self.vmind_path + 'notes' + DEL

    def note_folder(self, note_id: str) -> str:
        return self.notes_folder() + note_id + DEL

    def new(self, vmind_path: str):
        """Create empty, new vmind in given path and here."""

        # tabula rasa
        self.name = None
        self.notes = {}

        self.vmind_path = vmind_path

        # git init
        os.chdir(self.vmind_path)
        os.system('git init')

        # add name
        self.edit_name(name='empty vmind')
        # create notes folder
        if not os.path.exists(self.vmind_path + "notes" + DEL):
            os.makedirs(self.vmind_path + "notes" + DEL)
        # create an exemplar note
        self.new_note()
        # first commit
        self.commit(msg="new vmind")

    def commit(self, msg: str):
        """Commit current state with provided message."""
        os.chdir(self.vmind_path)
        os.system('git commit --all -m "' + str(msg) + '"')

    def load(self, load_path: str):
        """Load vmind from load_path."""

        # tabula rasa
        self.name = None
        self.notes = {}

        self.vmind_path = load_path

        # load name
        with open(self.vmind_path + 'name.txt', 'r') as name_file:
            self.name = name_file.readline()
        # load notes
        for note_id in os.listdir(self.notes_folder()):
            note_folder = self.note_folder(note_id=note_id)
            if os.path.isdir(note_folder):
                self.notes[note_id] = {}
                # load note title
                with open(note_folder + 'title.txt', 'r') as note_title_file:
                    self.notes[note_id]['title'] = note_title_file.read()

    def edit_name(self, name: str):
        self.name = name
        with open(self.vmind_path + 'name.txt', 'w') as name_file:
            name_file.write(self.name)
        os.chdir(self.vmind_path)
        os.system("git add name.txt")

    def new_note(self) -> str:
        # determine free note id
        new_note_id = None
        for note_idx in range(len(self.notes) + 1):
            if str(note_idx) not in self.notes:
                new_note_id = str(note_idx)
                break

        if new_note_id is not None:
            self.notes[new_note_id] = {}
            note_folder = self.note_folder(note_id=new_note_id)
            os.makedirs(note_folder)
            self.edit_note_title(note_id=new_note_id, title='new note')

        return new_note_id

    def edit_note_title(self, note_id: str, title: str):
        note_folder = self.note_folder(note_id=note_id)
        note_title_filename = note_folder + 'title.txt'
        self.notes[note_id]['title'] = title
        with open(note_title_filename, 'w') as note_title_file:
            note_title_file.write(title)
        os.chdir(self.vmind_path)
        os.system("git add " + note_title_filename)

    def remove_note(self, note_idx: int):
        pass