from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from question.forms import *
from question.models import *
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.http import require_POST


def sidebar(request):
    tags = Tag.objects.hottest()[:10]
    users = User.objects.by_rating()[:10]
    return {'tags': tags,
            'users': users}


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


@login_required(login_url='login')
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            qu = Question.objects.create(author=request.user,
                                         date=timezone.now(),
                                         is_active=True,
                                         title=form.cleaned_data['title'],
                                         text=form.cleaned_data['text'])
            qu.save()

            for tagTitle in form.cleaned_data['tags'].split():
                tag = Tag.objects.get_or_create(name=tagTitle)[0]
                qu.tags.add(tag)
                qu.save()
            # return question(request, ques.id)
            return redirect('/question/{}/'.format(qu.id))
    else:
        form = AskForm()
    return render(request, 'new_question.html', {
        'form': form,
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    })


def ans(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answeredQuestion = get_object_or_404(Question, pk=question_id)
            answer = Answer.objects.create(author=request.user,
                                           date=timezone.now(),
                                           text=form.cleaned_data['text'],
                                           question=answeredQuestion)
            answer.save()
            return redirect('/question/{}/'.format(question_id))
    else:
        form = AnswerForm()

    question = Question.objects.get_by_id(int(question_id)).first()
    if question is not None:
        answers = paginate(request, objects_list=Answer.objects.get_hot_for_answer(question.id))
        mapp = {'q': question,
                'form': form,
                'answers': answers,
                'page_objects' : answers,
                'tags': paginate(request, Tag.objects.hottest()),
                'users': paginate(request, User.objects.by_rating())}
        return render(request, 'answers.html', mapp)
    else:
        raise Http404


def reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(user.upload)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
        logout(request)
    return render(request, 'registration/registration.html', {
        'form': form,
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    })


def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
                # return redirect(request.GET.get('next') )
    else:
        form = UserLoginForm()
        logout(request)
    return render(request, 'registration/login.html', {
        'form': form,
        'tags': paginate(request, Tag.objects.hottest()),
        'users': paginate(request, User.objects.by_rating()),
    })


def profile(request, username):
    user = User.objects.by_username(username)
    if user is not None:
        return render(request, 'profile.html', {'profile': user})
    else:
        raise Http404


def profile_edit(request, username):
    user = get_object_or_404(User, username=request.user)
    form = UserRegistrationForm()
    return render(request, 'profile_edit.html', {'user': user, 'form': form})


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


@require_POST
@login_required(login_url='login')
def like_question(request):
    question_id = request.POST.get('question_id', '')
    like_type = request.POST.get('like_type', '')
    question = get_object_or_404(Question, pk=question_id)
    if not question:
        return JsonResponse({"status": "error"})

    if (like_type == 'like'):
        question.rating += 1
    elif (like_type == 'dislike'):
        question.rating -= 1
    question.save()

    return JsonResponse({"status": "ok"})


@require_POST
@login_required(login_url='login')
def like_answer(request):
    answer_id = request.POST.get('answer_id', '')
    like_type = request.POST.get('like_type', '')
    answer =get_object_or_404(Answer, pk=answer_id)
    if not answer:
        return JsonResponse({"status": "error"})

    if (like_type == 'like'):
        answer.rating += 1
    elif (like_type == 'dislike'):
        answer.rating -= 1
    answer.save()

    return JsonResponse({"status": "ok"})


@require_POST
@login_required(login_url='login')
def approve_answer(request):
    answer_id = request.POST.get('answer_id', '')
    answer =get_object_or_404(Answer, pk=answer_id)
    if not answer:
        return JsonResponse({"status": "error"})

    answer.approved = not answer.approved
    answer.save()

    return JsonResponse({"status": "ok"})