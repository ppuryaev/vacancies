from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from vacancy.forms import SubmitFrom
from vacancy.models import Specialty, Company, Vacancy, Application


# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.db import connection


# как брать сложные фильтры
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query


def main_view(request):
    # return HttpResponse("Главная. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['categories'] = Specialty.objects.all()
    context['companies'] = Company.objects.all()
    return render(request, 'vacancy/public/index.html', context=context)


def vacancy_list(request):
    # return HttpResponse("Список вакансий. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['vacancies'] = Vacancy.objects.all()
    return render(request, 'vacancy/public/vacancies.html', context=context)


def search(request):
    context = dict()
    if request.method == 'GET':
        if 'searchquery' not in request.GET.keys():
            context['vacancies'] = Vacancy.objects.all()
        else:
            search_string = request.GET['searchquery']
            context['vacancies'] = Vacancy.objects.filter(Q(title__icontains=search_string) |
                                                          Q(description__icontains=search_string))
            # просмотр запросов
            # print(Vacancy.objects.filter(Q(title__icontains=search_string) |
            #                              Q(description__icontains=search_string)).query)
    return render(request, 'vacancy/public/search.html', context=context)


def vacancy_cat_list(request, cat_slug):
    # return HttpResponse("Список вакансий по категориям. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['is_category'] = True
    try:
        context['category'] = Specialty.objects.get(code=cat_slug)
    except Specialty.DoesNotExist:
        raise Http404('Такой категории не существует!')
    context['vacancies'] = Vacancy.objects.filter(specialty_id__code=cat_slug)
    return render(request, 'vacancy/public/vacancies.html', context=context)


def company_info(request, company_id):
    # return HttpResponse("Карточка компании. Здесь будут все компании или здесь будет специализация")
    context = dict()
    try:
        context['company'] = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404('Такой компании не существует!')
    context['vacancies'] = Vacancy.objects.filter(company_id=company_id)
    return render(request, 'vacancy/public/company.html', context=context)


# LoginRequiredMixin
class VacancyInfo(FormMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/public/vacancy.html'
    context_object_name = 'vacancy'
    form_class = SubmitFrom
    # login_url = reverse_lazy('login')
    # raise_exception = True

    def get_success_url(self):
        return reverse('vacancy_send', kwargs={'pk': self.object.id})

    # https://stackoverflow.com/questions/45659986/django-implementing-a-form-within-a-generic-detailview
    def get_context_data(self, **kwargs):
        context = super(VacancyInfo, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if request.user.id is None:
            form.add_error(None, 'Для отправки формы необходимо авторизоваться!')
            return self.form_invalid(form)

        if form.is_valid():
            data = form.cleaned_data
            Application.objects.create(
                written_username=data['written_username'],
                written_phone=data['written_phone'],
                written_cover_letter=data['written_cover_letter'],
                vacancy=Vacancy.objects.get(pk=self.object.id),
                user=User.objects.get(pk=request.user.id)
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# def vacancy_info(request, vacancy_id):
#    # return HttpResponse("Карточка вакансии. Здесь будут все компании или здесь будет специализация")
#    context = dict()
#    try:
#        context['vacancy'] = Vacancy.objects.get(id=vacancy_id)
#    except Vacancy.DoesNotExist:
#        raise Http404('Вакансия не найдена!')
#    return render(request, 'vacancy/vacancy.html', context=context)


def vacancy_send(request, pk):
    vacancy_id = pk
    # – Отправка заявки /vacancies/<vacancy_id>/send/
    return render(request, 'vacancy/public/sent.html', context={'vacancy_id': vacancy_id})


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound("{} Выбери из существующих вариантов.".format(exception))


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
