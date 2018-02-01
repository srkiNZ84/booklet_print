#!/usr/bin/python2.7

from pyPdf import PdfFileWriter, PdfFileReader
import os
import argparse

parser = argparse.ArgumentParser(description='Reorder a PDF file to be able \
        print four pages on a single piece of paper in "booklet" order.')
parser.add_argument('inputpdf', type=str, help='PDF file to reorder.')
parser.add_argument('-o', '--outputfile', type=str, \
        help='Name of the file to output the reordered manifest to. \
        Defaults to the "[ORIGINAL_FILENAME]-reodered.pdf"')
args = parser.parse_args()

inputPDF = args.inputpdf
outputFile = args.inputpdf + "-reordered.pdf"
if args.outputfile:
    outputFile = args.outputfile

output = PdfFileWriter()
print("Reading PDF file '" + inputPDF + "'...")
input1 = PdfFileReader(file(inputPDF, "rb"))


def addBookletToOutput(inputFile, basePage, bookletSize,fileToWriteTo):
    print("basepage %s, size %s" % (basePage, bookletSize))
    for pages in range(bookletSize/2):
        #print("processing page set %s" % pages)

        lastPage = basePage + bookletSize
        #print("last page is %s" % lastPage)

        firstPage = basePage + pages
        secondPage = lastPage - pages - 1

        if(pages % 2 == 0):
            print("processing pages %s and %s, going to flip them" % \
                    (firstPage, secondPage))
            fileToWriteTo.addPage(inputFile.getPage(firstPage).rotateCounterClockwise(180))
            fileToWriteTo.addPage(inputFile.getPage(secondPage).rotateCounterClockwise(180))
        else:
            print("processing pages %s and %s" % \
                    (firstPage, secondPage))
            fileToWriteTo.addPage(inputFile.getPage(firstPage))
            fileToWriteTo.addPage(inputFile.getPage(secondPage))

# TODO: Make the number of pages per booklet configurable
# TODO: Make it output two pages per sheet automatically

# Get the number of pages
print("document %s has %s pages." % (inputPDF, input1.getNumPages()))
totalPages = input1.getNumPages()
# NOTE: As we're printing four pages per sheet of paper, the below needs to be
# a multiple of four
numPagesBooklet = 12
numBooklets = (totalPages + numPagesBooklet - 1)/numPagesBooklet

print("Going to have %s booklets" % numBooklets)
print("Going to have %s pages per booket" % numPagesBooklet)
lastBookletPages = totalPages % numPagesBooklet
print("Last booklet is going to have %s pages" % lastBookletPages)

for bookletCounter in range(numBooklets):
    basePage = bookletCounter * numPagesBooklet

    bookletSize = numPagesBooklet
    if(bookletCounter == numBooklets - 1 and totalPages % numPagesBooklet > 0 ):
        bookletSize = totalPages % numPagesBooklet

    addBookletToOutput(input1, basePage, bookletSize, output)

#output.addPage(input1.getPage(0).rotateCounterClockwise(180))
#output.addPage(input1.getPage(9).rotateCounterClockwise(180))
#output.addPage(input1.getPage(1))
#output.addPage(input1.getPage(8))
#output.addPage(input1.getPage(2).rotateCounterClockwise(180))
#output.addPage(input1.getPage(7).rotateCounterClockwise(180))
#output.addPage(input1.getPage(3))
#output.addPage(input1.getPage(6))
#output.addPage(input1.getPage(4).rotateCounterClockwise(180))
#output.addPage(input1.getPage(5).rotateCounterClockwise(180))

# Write "output" to document-output.pdf
print("Writing reordered page to PDF file '" + outputFile + "'...")
outputStream = file(outputFile, "wb")
output.write(outputStream)
outputStream.close()
print("All done! :-)")
