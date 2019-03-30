from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    return render(request, 'index.html')


def base(request):
    return render(request, 'base.html')


def tmp(request):
    return render(request, 'tmp.html')
