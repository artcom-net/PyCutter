"""Wrapper class of the PyCutter.

This class manages the other instances of classes: GuiApp, PdfFile.

"""


import os
import threading
from tkinter import Entry, NORMAL, DISABLED

from PyPDF2.utils import PdfReadError
from pdf import PdfFile, PageNotExistError


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


class MainApp(object):

    MESSAGES = {
        'value_error': {'msg_type': 'error', 'message': 'Option value error'},
        'enter_pages': {'msg_type': 'info', 'message': 'Enter page numbers'},
        'complete': {'msg_type': 'info', 'message': 'Successfully completed'}
        }

    def __init__(self, gui_app):
        """Initialize an instance.

        :param gui_app: GuiApp instance.

        """
        self._gui = gui_app
        self._pdf = None
        self._writer = None
        self._cut_mode = None
        self._cut_pages = None
        self._input_file = None
        self._pages_list = []
        self._gui.b_exit['command'] = self._exit_app
        self._gui.b_cut['command'] = self._run_cutter
        self._gui.b_open['command'] = self._get_input_file
        self._gui.master.protocol('WM_DELETE_WINDOW', self._exit_app)
        self._gui.master.withdraw()
        self._gui.master.iconbitmap('images/logo.ico')

    def start_app(self):
        """Shows the main window."""

        self._gui.master.deiconify()

    def _get_input_file(self):
        """Shows a dialog to select a file."""

        self._gui.open_dialog('input')
        if self._gui.input_path and self._check_file():
            self._gui.change_wdg_state(
                state=NORMAL,
                keys=('buttons', 'opt_buttons')
            )
            self._gui.switch_cut_option()

    def _check_file(self):
        """Checks input file."""

        try:
            self._input_file = open(self._gui.input_path, 'rb')
            return True
        except IOError as error:
            self._close_file()
            self._gui.show_message(msg_type='error', message=error)

    def _run_cutter(self):
        """Runs cutter in another thread."""

        threading.Thread(target=self._cutter).start()

    def _cutter(self):
        """Main cutter method."""

        self._pdf = self._get_pdf_instance()
        self._cut_mode = self._gui.option_choice.get()
        self._cut_pages = self._get_options()
        if self._cut_pages:
            self._gui.change_status('Cut process..')
            self._gui.change_wdg_state(state=DISABLED, keys='*')
            self._writer = self._pdf.cut_pages(
                self._cut_pages,
                cut_type=self._cut_mode
            )
            if self._save_file():
                self._gui.show_message(**MainApp.MESSAGES['complete'])
            self._gui.change_wdg_state(
                state=NORMAL,
                keys=('buttons', 'opt_buttons', 'options')
            )
            self._gui.switch_cut_option()
            self._gui.switch_save_option()
            self._gui.change_status('Ready..')

    def _get_pdf_instance(self):
        """Returns PdfFile instance, or displays an error message."""

        try:
            return PdfFile(self._input_file)
        except PdfReadError as error:
            self._gui.show_message(msg_type='error', message=error)
            self._close_file()
            self._gui.clear_entry_path()
            self._gui.change_wdg_state(
                state=DISABLED,
                keys='*',
                exclude=(self._gui.b_open, self._gui.b_exit)
            )

    def _get_options(self):
        """Gets page numbers from entry widget.

        Returns the list of pages for the mode range and multiple and
        the range object if selected each.

        """
        # option_choice = self._gui.option_choice.get()
        if self._cut_mode != 'each':
            pages = []
            for wdg in self._gui.widget_dict['options'][self._cut_mode]:
                if isinstance(wdg, Entry):
                    pages.append(wdg.get())
            return self._check_options(pages)
        else:
            return range(self._pdf.numPages)

    def _check_options(self, pages):
        """Check the values entered.

        Returns list of pages.

        :param pages: list of strings.

        """
        if all(pages) and self._check_negative(pages):
            if len(pages) == 2:
                if int(pages[0]) > int(pages[1]):
                    self._show_value_error()
                    return
            else:
                pages = pages[0].split(',')
            return [int(page.strip()) - 1 for page in pages]
        else:
            if any(pages):
                self._show_value_error()
            else:
                self._gui.show_message(**MainApp.MESSAGES['enter_pages'])

    @staticmethod
    def _check_negative(pages):
        """Check the list of values.
        All values must be greater than 0.

        :param pages: list of strings.

        """
        numbers = pages if len(pages) == 2 else pages[0].split(',')
        try:
            neg_num = list(filter(lambda num: int(num) <= 0, numbers))
        except ValueError:
            return False
        return False if len(neg_num) else True

    def _show_value_error(self):
        """Shows error message."""

        self._gui.show_message(**MainApp.MESSAGES['value_error'])

    def _save_file(self):
        save_path = self._get_save_path()
        try:
            for writer, path in zip(self._writer, save_path):
                with open(path, 'wb') as file:
                    writer.write(file)
            return True
        except PageNotExistError as error:
            self._gui.show_message(msg_type='error', message=error)

    def _get_save_path(self):
        """Save path generator."""

        if self._gui.option_save.get() and self._gui.save_path:
            save_path = self._gui.save_path
        else:
            save_path = os.path.split(self._gui.input_path)[0]
        filename = os.path.split(self._gui.input_path)[1].split('.')[0]
        if self._cut_mode == 'range':
            yield os.path.join(
                save_path, '%s_%s-%s.pdf' % (
                    filename, self._cut_pages[0] + 1, self._cut_pages[1] + 1
                )
            )
        else:
            for page in self._cut_pages:
                yield os.path.join(
                    save_path, '%s_%s.pdf' % (filename, page + 1)
                )

    def _close_file(self):
        """Closes input file."""

        if self._input_file and not self._input_file.closed:
            self._input_file.close()
            self._input_file = None

    def _exit_app(self):
        """Closes application."""

        if self._input_file:
            self._close_file()
        self._gui.master.destroy()
