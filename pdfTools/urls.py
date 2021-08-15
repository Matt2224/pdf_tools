from django.urls import path

from pdfTools import views

urlpatterns = [
    path('', views.makeHalfPagePDF, name='makeHalfPagePDF'),
]