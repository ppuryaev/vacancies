from django.shortcuts import render

from vacancy.models import *


from django.http import HttpResponse

# Create your views here.


def main_view(request):
    # return HttpResponse("Главная. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['categories'] = Specialty.objects.all()
    context['companies'] = Company.objects.all()
    # context['cat_vac_count'] =

    return render(request, 'vacancy/index.html', context=context)


def vacancy_list(request):
    #return HttpResponse("Список вакансий. Здесь будут все компании или здесь будет специализация")
    return render(request, 'vacancy/vacancies.html')


def vacancy_cat_list(request, cat_slug):
    # return HttpResponse("Список вакансий по категориям. Здесь будут все компании или здесь будет специализация")
    return render(request, 'vacancy/vacancies.html')


def company_info(request, company_id):
    # return HttpResponse("Карточка компании. Здесь будут все компании или здесь будет специализация")
    return render(request, 'vacancy/company.html')


def vacancy_info(request, vacancy_id):
    # return HttpResponse("Карточка вакансии. Здесь будут все компании или здесь будет специализация")
    return render(request, 'vacancy/vacancy.html')

