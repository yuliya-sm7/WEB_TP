from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseForbidden as Http403, HttpResponse
from django.contrib.auth.decorators import login_required

from question.models import *


def home(request):
    return render(request, 'home.html', {
        'questions': paginate(request, Question.objects.all()),
        'page_objects': paginate(request, Question.objects.all()),
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    })


def new(request):
    return render(request, 'home.html', {
        'questions': paginate(request, Question.objects.get_new()),
        'page_objects': paginate(request, Question.objects.all()),
    })


def ask(request):
    return render(request, 'new_question.html')


def ans(request, question_id):
    question = Question.objects.get_by_id(int(question_id)).first()
    if question is not None:
        answers = paginate(request, objects_list=Answer.objects.get_hot_for_answer(question.id))
        return render(request, 'answers.html', {'q': question, 'answers': answers})
    else:
        raise Http404


def reg(request):
    return render(request, 'registration/registration.html')


@login_required
def tmp(request):
    return render(request, 'tmp.html')


def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})
    else:
        raise Http404


def tag(request, tag):
    return render(request, 'home.html', {
        'questions': paginate(request, Question.objects.get_by_tag(tag_name=tag)),
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    })


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 3)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return objects
