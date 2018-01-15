#!/usr/bin/python2.7

from pyPdf import PdfFileWriter, PdfFileReader
import os
import argparse

parser = argparse.ArgumentParser(description='Reorder a PDF file to be able \
        print four pages on a single piece of paper in "booklet" order.')
parser.add_argument('inputpdf', type=str, help='PDF file to reorder.')
parser.add_argument('-o', '--outputfile', metavar='-o', type=str, \
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

# TODO: Smarts go here
# TODO: Need to split up PDF into "chunks" of 10 page each (make
# configurable?)
# TODO: Need to specify how to print out to make a "booklet", right now have
# to print "two pages per sheet".
# TODO: Make it output two pages per sheet automatically
output.addPage(input1.getPage(0).rotateCounterClockwise(180))
output.addPage(input1.getPage(9).rotateCounterClockwise(180))
output.addPage(input1.getPage(1))
output.addPage(input1.getPage(8))
output.addPage(input1.getPage(2).rotateCounterClockwise(180))
output.addPage(input1.getPage(7).rotateCounterClockwise(180))
output.addPage(input1.getPage(3))
output.addPage(input1.getPage(6))
output.addPage(input1.getPage(4).rotateCounterClockwise(180))
output.addPage(input1.getPage(5).rotateCounterClockwise(180))



# Write "output" to document-output.pdf
print("Writing reordered page to PDF file '" + outputFile + "'...")
outputStream = file(outputFile, "wb")
output.write(outputStream)
outputStream.close()
print("All done! :-)")
