from __future__ import unicode_literals

from django.contrib import admin
from question.models import Question, User, Tag, Answer

# Register your models here.

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Answer)
