import os

from weasyprint import HTML, CSS

from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.generic import NameObject, createStringObject

name = "pdfkit"

def camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def pdf_metadata_load(pdf_file):
    with open(pdf_file, 'rb') as fin:
        pdf_in = PdfFileReader(fin)
        writer = PdfFileWriter()

        for page in range(pdf_in.getNumPages()):
            writer.addPage(pdf_in.getPage(page))

        infoDict = writer._info.getObject()

    return pdf_in.documentInfo

def pdf_metadata_save(pdf_file, metadata, substitute_all_metadata = False, make_backup = True):
    if type(make_backup) is str:
        bak_file = make_backup
    else:
        bak_file = os.path.splitext(pdf_file)[0] + ".bak"
    os.rename(pdf_file, bak_file)

    with open(bak_file, 'rb') as fin:
        pdf_in = PdfFileReader(fin)
        writer = PdfFileWriter()

        for page in range(pdf_in.getNumPages()):
            writer.addPage(pdf_in.getPage(page))

        infoDict = writer._info.getObject()

        info = pdf_in.documentInfo
        if not substitute_all_metadata:
            for key in info:
                #infoDict.update({NameObject(key): createStringObject(info[key])})
                infoDict.update({key: info[key]})

        for key in metadata:
            infoDict.update({NameObject('/' + key): createStringObject(str(metadata[key]))})

        with open(pdf_file, 'wb') as fout:
            writer.write(fout)

        if make_backup == False:
            os.unlink(bak_file)


def method(args, article):
    item_id = article["item_id"]
    url = article["given_url"]
    save_file = os.path.join(args.output_dir, item_id + ".pdf")
    if not os.path.isfile(save_file):
        print("Saving article %s at %s" % (item_id, save_file))
        try:
            pdfkit.from_url(url, save_file, options)
            HTML(url).write_pdf(save_file)
        except Exception as e:
            print("  * error saving article %s: %s" % (item_id, str(e)))
            pass
    else:
        print("Skipping article %s because it does already exist at %s" % (item_id, save_file))

    try:
        metadata = {}
        for key in article:
            metadata[camel_case(key)] = article[key]
        pdf_metadata_save(save_file, metadata, False, False)
    except FileNotFoundError:
        print("File %s not generated" % save_file)
