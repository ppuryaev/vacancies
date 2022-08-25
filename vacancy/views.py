from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from vacancy.forms import SubmitFrom, CompanyForm, VacancyForm, ResumeForm
from vacancy.models import Vacancy, Company, Specialty, Application, Resume


# from django.db import connection

# как брать сложные фильтры
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query


def main_view(request):
    # return HttpResponse("Главная. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['categories'] = Specialty.objects.all()
    context['companies'] = Company.objects.all()
    return render(request, 'vacancy/index.html', context=context)


def vacancy_list(request):
    # return HttpResponse("Список вакансий. Здесь будут все компании или здесь будет специализация")
    context = dict()
    context['vacancies'] = Vacancy.objects.all()
    return render(request, 'vacancy/vacancies.html', context=context)


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
    return render(request, 'vacancy/search.html', context=context)


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


# LoginRequiredMixin
class VacancyInfo(FormMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy/vacancy.html'
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
    return render(request, 'vacancy/sent.html', context={'vacancy_id': vacancy_id})


@login_required
def mycompany_letsstart(request):
    user = User.objects.get(pk=request.user.id)
    print('первая страница создания')
    try:
        company_id = Company.objects.get(owner=user).id
        request.session["mycompany_exist"] = company_id
        return redirect('mycompany_info')
    except Company.DoesNotExist:
        return render(request, 'vacancy/company-create.html')


@login_required
def mycompany_create(request):
    user = User.objects.get(pk=request.user.id)
    left_menu = False
    try:
        company_id = Company.objects.get(owner=user).id
        request.session["mycompany_exist"] = company_id
        return redirect('mycompany_info')
    except Company.DoesNotExist:
        form = CompanyForm()
        update = False

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            update = True
            form.save(commit=False)
            data = form.cleaned_data
            Company.objects.create(
                name=data['name'],
                location=data['location'],
                logo=data['logo'],
                description=data['description'],
                employee_count=data['employee_count'],
                owner=User.objects.get(pk=request.user.id)
            )
            return redirect('mycompany_info')
    # – Моя компания (пустая форма) /mycompany/create/
    return render(request, 'vacancy/company-edit.html', context={'form': form,
                                                                 'update': update,
                                                                 'left_menu': left_menu})


@login_required
def mycompany_info(request):
    user = User.objects.get(pk=request.user.id)
    left_menu = True
    update = True if 'mycompany' in request.session.keys() else False

    try:
        company = Company.objects.get(owner=user)
        company_id = company.pk
    except Company.DoesNotExist:
        return redirect('mycompany_letsstart')

    form = CompanyForm(instance=company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            update = True
            data = form.cleaned_data
            current_company = Company.objects.get(pk=company_id)
            current_company.name = data['name']
            current_company.location = data['location']
            current_company.logo = data['logo'] if data['logo'] is not None else current_company.logo
            current_company.description = data['description']
            current_company.employee_count = data['employee_count']
            current_company.save()
            form = CompanyForm(instance=Company.objects.get(pk=company_id))
            company = Company.objects.get(id=company_id)
            return render(request, 'vacancy/company-edit.html', context={'form': form,
                                                                         'company': company,
                                                                         'update': update,
                                                                         'left_menu': left_menu})
    # – Моя компания (заполненная форма) /mycompany/
    return render(request, 'vacancy/company-edit.html', context={'form': form,
                                                                 'company': company,
                                                                 'update': update,
                                                                 'left_menu': left_menu})


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
    return render(request, 'vacancy/vacancy-list.html', context={'no_vacancies': no_vacancies,
                                                                 'vacancies': vacancies})


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
            return render(request, 'vacancy/vacancy-edit.html', context={'form': form,
                                                                         'update': update})

    return render(request, 'vacancy/vacancy-edit.html', context={'form': form,
                                                                 'update': update})


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
            return render(request, 'vacancy/vacancy-edit.html', context={'form': form,
                                                                         'update': update,
                                                                         'feedback': feedback})
    # – Одна моя вакансия (заполненная форма)  /mycompany/vacancies/<vacancy_id>
    return render(request, 'vacancy/vacancy-edit.html', context={'form': form,
                                                                 'update': update,
                                                                 'feedback': feedback})


@login_required
def myresume_letsstart(request):
    user = User.objects.get(pk=request.user.id)
    try:
        resume_id = Resume.objects.get(user=user).id
        request.session["myresume_exist"] = resume_id
        return redirect('myresume_info')
    except Resume.DoesNotExist:
        return render(request, 'vacancy/resume-create.html')


@login_required
def myresume_create(request):
    user = User.objects.get(pk=request.user.id)
    try:
        resume_id = Resume.objects.get(user_id=user).id
        request.session["myresume_exist"] = resume_id
        return redirect('myresume_info')
    except Resume.DoesNotExist:
        form = ResumeForm()
        form.initial['name'] = user.first_name
        form.initial['surname'] = user.last_name
        update = False

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            update = True
            form.save(commit=False)
            data = form.cleaned_data
            Resume.objects.create(
                user=user,
                name=data['name'],
                surname=data['surname'],
                status=data['status'],
                salary=data['salary'],
                specialty=data['specialty'],
                grade=data['grade'],
                education=data['education'],
                experience=data['experience'],
                portfolio=data['portfolio']
            )
            return redirect('myresume_info')

    return render(request, 'vacancy/resume-edit.html', context={'form': form,
                                                                'update': update})


@login_required
def myresume_info(request):
    user = User.objects.get(pk=request.user.id)
    update = True if 'myresume_exist' in request.session.keys() else False

    try:
        resume = Resume.objects.get(user=user)
        resume_id = resume.pk
    except Resume.DoesNotExist:
        return redirect('myresume_letsstart')

    form = ResumeForm(instance=resume)

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            update = True
            data = form.cleaned_data
            current_resume = Resume.objects.get(pk=resume_id)
            current_resume.name = data['name']
            current_resume.surname = data['surname']
            current_resume.status = data['status']
            current_resume.salary = data['salary']
            current_resume.specialty = data['specialty']
            current_resume.grade = data['grade']
            current_resume.education = data['education']
            current_resume.experience = data['experience']
            current_resume.portfolio = data['portfolio']
            current_resume.save()
            form = ResumeForm(instance=Resume.objects.get(pk=resume_id))
            return render(request, 'vacancy/resume-edit.html', context={'form': form,
                                                                        'update': update})
    return render(request, 'vacancy/resume-edit.html', context={'form': form,
                                                                'update': update})


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound("{} Выбери из существующих вариантов.".format(exception))


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
