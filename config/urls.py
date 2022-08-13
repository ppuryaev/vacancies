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

from vacancy.views import custom_handler404, custom_handler500
from vacancy.views import main_view, vacancy_list, vacancy_cat_list, company_info, vacancy_info

handler404 = custom_handler404
handler500 = custom_handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_page'),
    path('vacancies/', vacancy_list, name='vacancy_list'),
    path('vacancies/cat/<slug:cat_slug>/', vacancy_cat_list, name='vacancy_cat_list'),
    path('companies/<int:company_id>', company_info, name='company_page'),
    path('vacancies/<int:vacancy_id>', vacancy_info, name='vacancy_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
