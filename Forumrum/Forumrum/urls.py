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

    path('hot', views.hot, name='hot'),

    path('accounts/login', vs.LoginView.as_view(), name='login'),

    path(r'^user/(?P<username>[a-zA-Zа-яА-Я_\-\.0-9]+?)$', views.profile, name='profile'),

    path(r'^tag/(?P<tag>.*)/$', views.tag, name='tag'),

    path('ask', views.ask, name='ask'),

    path(r'^question/(?P<question_id>[0-9]+)/$', views.ans, name='ans'),

    path('reg', views.reg, name='reg'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
