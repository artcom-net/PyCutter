""" PfdFile class of the PyCutter.

This class implements the manipulation of PDF files.

"""


import sys

from PyPDF2 import PdfFileReader, PdfFileWriter


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


sys.setrecursionlimit(2000)


class PageNotExistError(Exception):

    def __init__(self, page):
        self.message = 'Page %d not exist' % page

    def __str__(self):
        return self.message


class PdfFile(PdfFileReader):

    def cut_pages(self, pages, cut_type):
        if cut_type == 'range':
            writer = PdfFileWriter()
            start, end = pages
            for page in range(start, end + 1):
                try:
                    writer.addPage(self.getPage(page))
                except IndexError:
                    raise PageNotExistError(page + 1)
            yield writer

        elif cut_type in ('multiple', 'each'):
            for page in pages:
                writer = PdfFileWriter()
                try:
                    writer.addPage(self.getPage(page))
                    yield writer
                except IndexError:
                    raise PageNotExistError(page + 1)
