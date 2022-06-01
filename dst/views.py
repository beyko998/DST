from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ServiceOrProduct


def start_page(request):
    return render(request, 'home.html')


def products(request):
    serprod = ServiceOrProduct.objects.all()
    return render(request, 'dst/products.html', {'product': serprod},)
