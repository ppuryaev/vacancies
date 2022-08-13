from django.db import models

# Create your models here.


class Vacancy(models.Model):

    title = models.CharField(max_length=100, verbose_name="Название вакансии")
    specialty = models.ForeignKey('Specialty',
                                  on_delete=models.CASCADE,
                                  related_name="vacancies",
                                  verbose_name="Специализация")
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="vacancies", verbose_name="Компания")
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Текст')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(auto_now_add=True, verbose_name='Опубликовано')
    # – Название вакансии(title)
    # – Специализация(specialty) – связь с Specialty, укажите related_name = "vacancies"
    # – Компания(company) – связь с Company, укажите related_name = "vacancies"
    # – Навыки(skills)
    # – Текст(description)
    # – Зарплата от(salary_min)
    # – Зарплата до(salary_max)
    # – Опубликовано(published_at)


class Company(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название")
    location = models.CharField(max_length=100, verbose_name="Город")
    logo = models.URLField(default='https://place-hold.it/100x60', verbose_name="Логотипчик")
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество сотрудников')
    # – Название(name)
    # – Город(location)
    # – Логотипчик(logo)(URLField(default='https://place-hold.it/100x60'))
    # – Информация о компании(description)
    # – Количество сотрудников(employee_count)


class Specialty(models.Model):

    code = models.SlugField(max_length=255, unique=True, verbose_name="Код")
    title = models.CharField(max_length=100, verbose_name="Название")
    picture = models.URLField(default='https://place-hold.it/100x60', verbose_name="Картинка")
    # – Код(code) например, testing, gamedev
    # – Название(title)
    # – Картинка(picture)(URLField(default='https://place-hold.it/100x60'))
