from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def base(request):
    return render(request, 'base.html')


def profile(request):
    return render(request, 'profile.html')


def ask(request):
    return render(request, 'new_question.html')


@login_required
def tmp(request):
    return render(request, 'tmp.html')
