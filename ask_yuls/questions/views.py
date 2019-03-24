from django.shortcuts import render

# Create your views here.

# from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden as Http403, HttpResponse, JsonResponse
import json
from django.utils import timezone


def index(request):
    return render(request, 'index.html')
