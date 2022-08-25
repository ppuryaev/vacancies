from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from vacancy.forms import VacancyForm
from vacancy.models import Company, Vacancy, Application


@login_required
def myvacancy_list(request):
    user_id = User.objects.get(pk=request.user.id)
    company = Company.objects.get(owner=user_id)
    vacancies = Vacancy.objects.filter(company=company)
    if vacancies.count() == 0:
        print('нет вакансий')
        no_vacancies = True
    else:
        no_vacancies = False
        print('есть вакансии')
    print(vacancies.count())

    # – Мои вакансии (список) /mycompany/vacancies/
    return render(request, 'vacancy/my_vacancy/vacancy-list.html', context={
                                                                'no_vacancies': no_vacancies,
                                                                'vacancies': vacancies
                                                                })


@login_required
def myvacancy_blank_form(request):
    # – Мои вакансии (пустая форма) /mycompany/vacancies/create/
    company = Company.objects.get(owner=User.objects.get(pk=request.user.id))
    form = VacancyForm()
    update = False

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        update = True
        if form.is_valid():
            form.save(commit=False)
            data = form.cleaned_data
            Vacancy.objects.create(
                title=data['title'],
                specialty=data['specialty'],
                company=company,
                skills=data['skills'],
                description=data['description'],
                salary_min=data['salary_min'],
                salary_max=data['salary_max']
            )
            return render(request, 'vacancy/my_vacancy/vacancy-edit.html', context={
                                                                        'form': form,
                                                                        'update': update
                                                                        })

    return render(request, 'vacancy/my_vacancy/vacancy-edit.html', context={
                                                                'form': form,
                                                                'update': update
                                                                })


@login_required
def myvacancy_info(request, vacancy_id):

    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = VacancyForm(instance=vacancy)
    except Vacancy.DoesNotExist:
        raise Http404('Такой вакансии не существует!')
    update = False
    feedback = Application.objects.filter(vacancy_id=vacancy_id)

    if request.method == 'POST':
        update = True
        form = VacancyForm(request.POST)

        if form.is_valid():
            print('Данные валидны')
            data = form.cleaned_data
            current_vacancy = vacancy
            current_vacancy.title = data['title']
            current_vacancy.specialty = data['specialty']
            current_vacancy.skills = data['skills']
            current_vacancy.description = data['description']
            current_vacancy.salary_min = data['salary_min']
            current_vacancy.salary_max = data['salary_max']
            current_vacancy.save()
            # проверка SQL запросов
            # from django.db import connection
            # print(connection.queries)
            # print(form.cleaned_data)
            form = VacancyForm(instance=current_vacancy)
            return render(request, 'vacancy/my_vacancy/vacancy-edit.html', context={
                                                                        'form': form,
                                                                        'update': update,
                                                                        'feedback': feedback
                                                                        })
    # – Одна моя вакансия (заполненная форма)  /mycompany/vacancies/<vacancy_id>
    return render(request, 'vacancy/my_vacancy/vacancy-edit.html', context={
                                                                'form': form,
                                                                'update': update,
                                                                'feedback': feedback
                                                                })
