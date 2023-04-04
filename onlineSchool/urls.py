"""onlineSchool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from core import views
from onlineSchool import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('registration/', views.RegistrationView.as_view()),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('', views.IndexView.as_view()),
    path('courses', views.CourseByCategoryView.as_view()),
    path('course/<int:pk>/', views.CourseView.as_view()),
    path('homework/<int:pk_homework>/eval/', views.EvaluateHomeworkView.as_view()),
    path('course/<int:pk>/lecture/<int:pk_lecture>/', views.LectureView.as_view()),
    path('course/<int:pk>/lecture/<int:pk_lecture>/done/', views.LectureView.as_view()),
    path('course/<int:pk>/add-comment/', views.AddCommentView.as_view()),
    path('course/<int:pk>/students/', views.StudentsView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
