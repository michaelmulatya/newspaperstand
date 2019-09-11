import requests
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
url = 'https://s3.us-east-2.amazonaws.com/wanderift/magz/CrossStitcher+%E2%80%93+March+2019.pdf'
r = requests.get(url, stream=True)

with open('crossstitcher.pdf', 'wb') as fd:
    for chunk in r.iter_content(2000):
        fd.write(chunk)
inputpdf = PdfFileReader(open("crossstitcher.pdf", "rb"))
output = PdfFileWriter()
outputStream= open("preview.pdf", "wb")
for i in range(4):
    output.addPage(inputpdf.getPage(i))
    output.write(outputStream)