UniteOCR
========

This script creates a merged PDF with an OCR layer from several separate files.
It is intended to partly automate this workflow:

1)  Scan multi-page document using XSane. This results in files like file_name_prefix-0008.pdf - one file for each page.
2)  Create one merged PDF: `pdfunite file_name_prefix* file_name_prefix.pdf`
3)  Add an OCR layer: `ocrmypdf file_name_prefix.pdf`
