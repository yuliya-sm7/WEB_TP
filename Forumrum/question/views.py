from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home(request):
    return render(request, 'home.html')


def base(request):
    objects = ['john', 'paul', 'george', 'ringo']
    p = Paginator(objects, 2)
    return render(request, 'base.html', {
        'page_objects': Paginator(request, objects),
    })


def ask(request):
    return render(request, 'new_question.html')


def ans(request):
    return render(request, 'answers.html')


def reg(request):
    return render(request, 'registration/registration.html')


@login_required
def tmp(request):
    return render(request, 'tmp.html')


def profile(request):
    return render(request, 'profile.html')
