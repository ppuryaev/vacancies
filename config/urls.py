"""config URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import LoginUser, RegisterUser, logout_view
from vacancy.views.my_company import mycompany_letsstart, mycompany_create, mycompany_info
from vacancy.views.my_cv import myresume_letsstart, myresume_create, myresume_info
from vacancy.views.my_vacancy import myvacancy_list, myvacancy_blank_form, myvacancy_info
from vacancy.views.public import VacancyInfo
from vacancy.views.public import custom_handler404, custom_handler500
from vacancy.views.public import main_view, vacancy_list, vacancy_cat_list, company_info, vacancy_send
from vacancy.views.public import search

handler404 = custom_handler404
handler500 = custom_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_page'),
    path('vacancies/', vacancy_list, name='vacancy_list'),
    path('vacancies/cat/<slug:cat_slug>/', vacancy_cat_list, name='vacancy_cat_list'),
    path('companies/<int:company_id>', company_info, name='company_page'),
    path('vacancies/<pk>', VacancyInfo.as_view(), name='vacancy_page'),
    path('vacancies/<int:pk>/send/', vacancy_send, name='vacancy_send'),
    path('mycompany/letsstart/', mycompany_letsstart, name='mycompany_letsstart'),
    path('mycompany/create/', mycompany_create, name='mycompany_create'),
    path('mycompany/', mycompany_info, name='mycompany_info'),
    path('mycompany/vacancies/', myvacancy_list, name='myvacancy_list'),
    path('mycompany/vacancies/create/', myvacancy_blank_form, name='myvacancy_blank_form'),
    path('mycompany/vacancies/<int:vacancy_id>', myvacancy_info, name='myvacancy_info'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_view, name='logout_view'),
    path('myresume/letsstart', myresume_letsstart, name='myresume_letsstart'),
    path('myresume/create/', myresume_create, name='myresume_create'),
    path('myresume/', myresume_info, name='myresume_info'),
    path('search/', search, name='search_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
