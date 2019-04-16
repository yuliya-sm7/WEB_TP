from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from question import views
from django.contrib.auth import views as vs
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('new', views.new, name='new'),

    path('accounts/login', vs.LoginView.as_view(), name='login'),

    path('tmp', views.tmp, name='tmp'),

    url(r'^user/(?P<username>[a-zA-Zа-яА-Я_\-\.0-9]+?)$', views.profile, name='profile'),

    url(r'^tag/(?P<tag>.*)/$', views.tag, name='tag'),

    path('ask', views.ask, name='ask'),

    url(r'^question/(?P<question_id>[0-9]+)/$', views.ans, name='ans'),

    path('reg', views.reg, name='reg'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
