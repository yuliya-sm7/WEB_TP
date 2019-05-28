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

    path('accounts/logout', vs.LogoutView.as_view(), name='logout'),

    path('user/<str:username>', views.profile, name='profile'),

    path('user/<str:username>/edit', views.profile_edit, name='profile_edit'),

    path('tag/<str:tag>', views.tag, name='tag'),

    path('ask', views.ask, name='ask'),

    path('question/<int:question_id>/', views.ans, name='ans'),

    path('reg', views.reg, name='reg'),

    path('like_question/', views.like_question, name='like_question'),

    path('like_answer/', views.like_answer, name='like_answer'),

    path('approve_answer/', views.approve_answer, name='approve_answer'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
