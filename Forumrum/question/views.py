from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseForbidden as Http403, HttpResponse
from django.contrib.auth.decorators import login_required

from question.models import *


def sidebar(request):
    return {
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    }


def home(request):
    mapp = sidebar(request)
    mapp['page_objects'] = paginate(request, Question.objects.all())
    mapp['questions'] = paginate(request, Question.objects.all())
    return render(request, 'home.html', mapp)


def new(request):
    mapp = sidebar(request)
    mapp['page_objects'] = paginate(request, Question.objects.get_new())
    mapp['questions'] = paginate(request, Question.objects.get_new())
    return render(request, 'home.html', mapp)


def hot(request):
    mapp = sidebar(request)
    mapp['page_objects'] = paginate(request, Question.objects.get_hot())
    mapp['questions'] = paginate(request, Question.objects.get_hot())
    return render(request, 'home.html', mapp)


def tag(request, tag):
    mapp = sidebar(request)
    mapp['page_objects'] = paginate(request, Tag.objects.get_by_tag(tag_name=tag))
    mapp['questions'] = paginate(request, Tag.objects.get_by_tag(tag_name=tag))

    return render(request, 'home.html', mapp)


# @login_required
def ask(request):
    return render(request, 'new_question.html')


def ans(request, question_id):
    question = Question.objects.get_by_id(int(question_id)).first()
    if question is not None:
        answers = paginate(request, objects_list=Answer.objects.get_hot_for_answer(question.id))
        mapp = {'q': question, 'answers': answers, 'tags': paginate(request, Tag.objects.hottest()),
                'users': paginate(request, User.objects.by_rating())}
        return render(request, 'answers.html', mapp)
    else:
        raise Http404


def reg(request):
    return render(request, 'registration/registration.html')


def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})
    else:
        raise Http404


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
