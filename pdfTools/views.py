from copy import copy

from django.http import HttpResponse
from django.shortcuts import render
from PyPDF2 import PdfFileReader, PdfFileWriter

# Create your views here.
def makeHalfPagePDF(request):
    if "GET" == request.method:
        return render(request, 'pdfTools/makeHalfPagePDF.html', {})
    else:
        file = request.FILES["pdf_file"]
        with open('original_pdf', 'wb+') as pdfFileObj:
            for chunk in file.chunks():
                pdfFileObj.write(chunk)
            pdf_reader = PdfFileReader(pdfFileObj)

            pdf_writer = PdfFileWriter()
            for i in range(pdf_reader.numPages):
                page = pdf_reader.getPage(i)
                width = page.mediaBox.getUpperRight_x() - page.mediaBox.getUpperLeft_x()
                height = page.mediaBox.getUpperLeft_y() - page.mediaBox.getLowerLeft_y()

                # 왼쪽 반
                for_left = copy(page)
                for_left.cropBox.setLowerLeft((0, 0))
                for_left.cropBox.setUpperRight((width/2, height))
                pdf_writer.addPage(for_left)

                # 오른쪽 반
                for_right = copy(page)
                for_right.cropBox.setLowerLeft((width / 2, 0))
                for_right.cropBox.setUpperRight((width, height))
                pdf_writer.addPage(for_right)

            with open('result.pdf', 'wb') as pdfResultFile:
                pdf_writer.write(pdfResultFile)

            with open('result.pdf', 'rb') as pdfResult:
                response = HttpResponse(pdfResult.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=result.pdf'
                return response
