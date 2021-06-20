'''Merge and OCR PDF files.'''

import argparse
from typing import Iterable
from PyPDF2 import PdfFileMerger
from ocrmypdf import ocr
from logging import info as log, basicConfig, INFO


def get_files(file_prefix) -> Iterable[str]:
    '''Return the files matching file_prefix in an alphabetical order.'''
    from glob import glob
    return sorted(
        filter(
            lambda file_name:
                str(file_name).lower().endswith('.pdf'),
            glob(f'{file_prefix}*')))


def get_merged_file(files: Iterable[str]) -> PdfFileMerger:
    '''Merge the list of PDF files provided in its argument.
    Returns the merged file.

    See also: https://github.com/tkmru/im2pdf/blob/master/im2pdf.py#L30
    '''
    output_pdf: PdfFileMerger = PdfFileMerger()

    for file in files:
        output_pdf.append(file)

    return output_pdf


def get_output_file(file_prefix: str) -> str:
    '''Generate an output file name from the provided file_prefix'''

    if '**' in file_prefix:
        raise NameError('File pattern cannot be recursive.')

    from re import sub
    return sub(pattern=r'(-0*)?\*?$', repl='.pdf', string=file_prefix)


def write_merged_file(pdf_object: PdfFileMerger, target_path: str) -> None:
    '''Output the merged PDF into a file.'''
    pdf_object.write(target_path)


def uniteocr():
    '''Entry point of the module'''

    file_prefix, languages = get_args()

    basicConfig(level=INFO)

    files_to_merge: Iterable[str] = get_files(file_prefix)
    merged_file: PdfFileMerger = get_merged_file(files_to_merge)

    target_location = get_output_file(file_prefix)

    choice = input(f'Write to target location \'{target_location}\'? (y/n) ')

    if choice == 'y':
        write_merged_file(merged_file, target_location)
        log('merged PDF written, doing OCR')
        ocr(
            input_file=target_location,
            output_file=target_location,
            language=languages,
            skip_text=True)
        log('all done, enjoy your file.')

    else:
        log('This ain\'t a yes, not merging, okay.')


def get_args():
    parser = argparse.ArgumentParser(description='Merge and OCR PDF files.')
    parser.add_argument(
        'file_prefix',
        help='''Set the file nane and path prefix matching all the PDF files.
            An asterisk (*) is implied at the end.''')
    parser.add_argument(
        'languages',
        default='hun+eng',
        help='''Set the languages of the documents. E.g. hun+eng.
            Find available languages like `tesseract --list-langs`''')
    
    args = parser.parse_args()
    file_prefix: str = args.file_prefix
    languages: str = args.languages

    return (file_prefix, languages)


if __name__ == '__main__':
    uniteocr()
