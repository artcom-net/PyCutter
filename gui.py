"""GUI class of the PyCutter.

This class is the graphical part of the application and is managed from
the wrapper class - MainApp.

"""


from tkinter import ttk
from tkinter.filedialog import *
from tkinter import messagebox as msg


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


class GuiApp(object):

    DIALOG_CONF = {
        'input': {
            'title': 'Open',
            'defaultextension': '.pdf',
            'filetypes': [('PDF (*.pdf)', '.pdf')],
            'initialdir': os.path.expanduser('~')
        },
        'save': {
            'title': 'Save',
            'initialdir': os.path.expanduser('~')
        }
    }
    
    def __init__(self, master):
        """Initialize an instance.
        
        :param master: Tk instance.
         
        """
        self.master = master
        self.master.title('PyCutter')
        self.master.resizable(0, 0)
        self.option_choice = StringVar(value='range')
        self.option_save = BooleanVar(value=False)
        self.input_path = None
        self.save_path = None
        self.f_input = ttk.LabelFrame(
            self.master,
            text='PDF File',
            width=250,
            height=100
        )
        self.f_options = ttk.LabelFrame(self.master, text='Split Options')
        self.f_output = ttk.LabelFrame(self.master, text='Output Path')
        self.f_bottom = Frame(self.master)
        self.e_path = Entry(
            self.f_input,
            width=40,
            state='readonly'
        )
        self.b_open = Button(
            self.f_input,
            text='Open',
            width=10
        )
        self.rb_range = Radiobutton(
            self.f_options,
            text='Extract range',
            variable=self.option_choice,
            value='range',
            command=self.switch_cut_option,
            state=DISABLED
        )
        self.rb_multiple = Radiobutton(
            self.f_options,
            text='Extract multiple',
            variable=self.option_choice,
            value='multiple',
            command=self.switch_cut_option,
            state=DISABLED
        )
        self.rb_each = Radiobutton(
            self.f_options,
            text='Extract each page',
            variable=self.option_choice,
            value='each',
            command=self.switch_cut_option,
            state=DISABLED
        )
        self.l_start_page = Label(
            self.f_options,
            text='Start page',
            state=DISABLED
        )
        self.l_end_page = Label(
            self.f_options,
            text='End page',
            state=DISABLED
        )
        self.e_start_page = Entry(self.f_options, width=6, state=DISABLED)
        self.e_end_page = Entry(self.f_options, width=6, state=DISABLED)
        self.l_multiple = Label(self.f_options, text='Pages', state=DISABLED)
        self.e_multiple = Entry(self.f_options, width=17, state=DISABLED)
        self.l_multiple_exp = Label(
            self.f_options,
            text='(example: 5, 11, 23, 54)',
            state=DISABLED
        )
        self.e_output = Entry(self.f_output, width=40, state='readonly')
        self.b_save = Button(
            self.f_output,
            text='Path',
            width=10,
            state=DISABLED,
            command=lambda dialog_type='save': self.open_dialog(dialog_type)
        )
        self.b_cut = Button(
            self.f_bottom,
            text='Cut',
            width=10,
            state=DISABLED,
        )
        self.b_exit = Button(
            self.f_bottom,
            text='Exit',
            width=10,
        )
        self.cb_save = Checkbutton(
            self.master,
            text='Specific save path',
            variable=self.option_save,
            onvalue=True,
            offvalue=False,
            anchor=W,
            command=self.switch_save_option,
            state=DISABLED
        )
        self.l_status = Label(
            self.master,
            text='Ready..',
            bd=1,
            relief=SUNKEN,
            anchor=W
        )
        self.widget_dict = {
            'buttons': [self.b_open, self.b_cut, self.b_exit],
            'opt_buttons': [
                self.rb_range,
                self.rb_multiple,
                self.rb_each,
                self.cb_save
            ],
            'options': {
                'range': [
                    self.l_start_page,
                    self.l_end_page,
                    self.e_start_page,
                    self.e_end_page
                ],
                'multiple': [self.l_multiple, self.e_multiple]
            },
            'save': [self.e_output, self.b_save]
        }
        # Geometry
        self.f_input.pack(fill=X, padx=20, pady=(15, 0))
        self.f_options.pack(fill=X, padx=20, pady=10)
        self.e_path.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=(15, 10),
            pady=(15, 20)
        )
        self.b_open.grid(row=0, column=4, padx=(0, 15), pady=(0, 5))
        self.rb_range.grid(row=0, column=0, pady=(15, 5))
        self.l_start_page.grid(row=1, column=0, sticky=E)
        self.e_start_page.grid(row=1, column=1)
        self.l_end_page.grid(row=1, column=2)
        self.e_end_page.grid(row=1, column=3)
        self.rb_multiple.grid(row=2, column=0, padx=(4, 0), pady=(10, 5))
        self.l_multiple.grid(row=3, column=0, sticky=E)
        self.e_multiple.grid(row=3, column=1, columnspan=2)
        self.l_multiple_exp.grid(row=3, column=3)
        self.rb_each.grid(row=4, column=0, padx=(12, 0), pady=(10, 20))
        self.cb_save.pack(fill=X, padx=(15, 0), pady=(0, 10))
        self.f_output.pack(fill=X, padx=20)
        self.e_output.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=(15, 10),
            pady=(15, 20)
        )
        self.b_save.grid(row=0, column=4, pady=(0, 5))
        self.f_bottom.pack()
        self.b_cut.grid(row=0, column=0, padx=(0, 30), pady=10)
        self.b_exit.grid(row=0, column=1)
        self.l_status.pack(side=BOTTOM, fill=X)

    def open_dialog(self, dialog_type):
        """Opens a dialog to select a file or save path.

        :param dialog_type: input/save;

        """
        func = askopenfilename if dialog_type == 'input' else askdirectory
        setattr(
            self,
            '%s_path' % dialog_type,
            func(**GuiApp.DIALOG_CONF[dialog_type])
        )
        self._insert_path(target=dialog_type)

    @staticmethod
    def show_message(**kwargs):
        """Displays error messages and information.

        :param kwargs
            'msg_type': message type ('error'/'info');
            'message': message text.
        
        """
        func = msg.showerror if kwargs['msg_type'] == 'error' else msg.showinfo
        func(kwargs['msg_type'].capitalize(), kwargs['message'])

    def change_wdg_state(self, state, keys, exclude=None):
        """Changes the state of the group widgets from NORMAL to DISABLED 
        and conversely. Widgets collected in the widget_dict. 
        
        :param state: ENABLE/DISABLE;
        :param keys: tuple with keys dict or '*' for all;
        :param exclude: tuple with widget objects.
        
        """
        wdg_list = []
        keys = self.widget_dict.keys() if keys == '*' else keys
        for key in keys:
            if isinstance(self.widget_dict[key], dict):
                for lst in self.widget_dict[key].values():
                    wdg_list += lst
            else:
                wdg_list += self.widget_dict[key]
        if exclude:
            wdg_list = list(filter(lambda wdg: wdg not in exclude, wdg_list))
        self._change_state(state, wdg_list)

    def switch_cut_option(self):
        """Changes the state of the widgets when switch the radio buttons."""
        
        if self.option_choice.get() == 'each':
            for opt in self.widget_dict['options']:
                self._change_state(
                    'disabled',
                    self.widget_dict['options'][opt]
                )
        else:
            for opt in self.widget_dict['options']:
                state = 'normal' if opt == self.option_choice.get() \
                    else 'disabled'
                self._change_state(state, self.widget_dict['options'][opt])
    
    @staticmethod
    def _change_state(state, wdg_list):
        """Changes the state of the widgets.
        
        :param state: ENABLE/DISABLE;
        :param wdg_list: the list of widgets.
        
        """
        for wdg in wdg_list:
            wdg['state'] = state

    def switch_save_option(self):
        """Switches the state of save section."""
        
        self.b_save['state'] = NORMAL if self.option_save.get() else DISABLED
        self.e_output['state'] = 'readonly' if self.option_save.get() \
            else DISABLED

    def _insert_path(self, target):
        """Inserts the value of a file path or save location in entry widget.
        
        :param target: string specifies a entry widget ('input'/'save').
        
        """
        attr_name = '%s_path' % target
        entry, path = (self.e_path, self.input_path) if target == 'input' \
            else (self.e_output, self.save_path)
        if path:
            entry['state'] = NORMAL
            entry.delete(0, END)
            entry.insert(END, os.path.normpath(path))
            entry['state'] = 'readonly' if path else DISABLED
        else:
            setattr(self, attr_name, entry.get())
    
    def clear_entry_path(self):
        """Remove path from entry."""
        
        self.input_path = None
        self.e_path['state'] = NORMAL
        self.e_path.delete(0, END)
        self.e_path['state'] = 'readonly'

    def change_status(self, status):
        """Changes the status of the application.
        
        :param status: string value.
        
        """
        self.l_status['text'] = status
        self.l_status.update()
