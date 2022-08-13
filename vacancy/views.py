from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404

from vacancy.models import Vacancy, Company, Specialty


# Create your views here.


def main_view(request):
    # return HttpResponse("Главная. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['categories'] = Specialty.objects.all()
    context['companies'] = Company.objects.all()
    # context['cat_vac_count'] =

    return render(request, 'vacancy/index.html', context=context)


def vacancy_list(request):
    # return HttpResponse("Список вакансий. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['vacancies'] = Vacancy.objects.all()
    return render(request, 'vacancy/vacancies.html', context=context)


def vacancy_cat_list(request, cat_slug):
    # return HttpResponse("Список вакансий по категориям. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['is_category'] = True
    try:
        context['category'] = Specialty.objects.get(code=cat_slug)
    except Specialty.DoesNotExist:
        raise Http404('Такой категории не существует!')
    context['vacancies'] = Vacancy.objects.filter(specialty_id__code=cat_slug)
    return render(request, 'vacancy/vacancies.html', context=context)


def company_info(request, company_id):
    # return HttpResponse("Карточка компании. Здесь будут все компании или здесь будет специализация")
    context = dict()
    try:
        context['company'] = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404('Такой компании не существует!')
    context['vacancies'] = Vacancy.objects.filter(company_id=company_id)
    return render(request, 'vacancy/company.html', context=context)


def vacancy_info(request, vacancy_id):
    # return HttpResponse("Карточка вакансии. Здесь будут все компании или здесь будет специализация")
    context = dict()
    try:
        context['vacancy'] = Vacancy.objects.get(id=vacancy_id)
    except Vacancy.DoesNotExist:
        raise Http404('Вакансия не найдена!')
    return render(request, 'vacancy/vacancy.html', context=context)


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound("{} Выбери из существующих вариантов.".format(exception))


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
