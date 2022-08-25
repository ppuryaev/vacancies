from django.contrib.auth.models import User
from django.db import models

from config.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR


# Create your models here.


class Vacancy(models.Model):

    title = models.CharField(max_length=100, verbose_name="Название вакансии")
    specialty = models.ForeignKey('Specialty',
                                  on_delete=models.CASCADE,
                                  related_name="vacancies",
                                  verbose_name="Специализация")
    company = models.ForeignKey('Company',
                                on_delete=models.CASCADE,
                                related_name="vacancies",
                                verbose_name="Компания")
    skills = models.TextField(verbose_name='Навыки')
    description = models.TextField(verbose_name='Текст')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(auto_now_add=True, verbose_name='Опубликовано')


class Company(models.Model):

    name = models.CharField(max_length=100, verbose_name="Название")
    location = models.CharField(max_length=100, verbose_name="Город")
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, null=True, blank=True, verbose_name="Логотипчик")
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество сотрудников')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class Specialty(models.Model):

    code = models.SlugField(max_length=255, unique=True, verbose_name="Код")
    title = models.CharField(max_length=100, verbose_name="Название")
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, verbose_name="Картинка")

    def __str__(self):
        return self.title


class Application(models.Model):

    written_username = models.CharField(max_length=255, verbose_name="Имя")
    written_phone = models.CharField(max_length=255, verbose_name="Телефон")
    # PhoneField(verbose_name="Телефон")
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications", verbose_name="Вакансия")
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name="applications",
                             verbose_name="Пользователь")


class Status(models.TextChoices):
    LOOKING_FOR = "LR", "Ищу работу"
    NOT_LOOKING_FOR = "NR", "Не ищу работу"
    WATCHING = "WG", "Рассматриваю предложения"


class Grade(models.TextChoices):
    TRAINEE = "TE", "Стажер"
    JUNIOR = "JR", "Джуниор"
    MIDDLE = "ME", "Миддл"
    SENIOR = "SR", "Синьор"
    LEAD = "LD", "Лид"


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Имя")
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NOT_LOOKING_FOR
    )
    salary = models.IntegerField(verbose_name='Вознаграждение')
    specialty = models.ForeignKey('Specialty',
                                  on_delete=models.CASCADE,
                                  related_name="specialty",
                                  verbose_name="Специализация")
    grade = models.CharField(
        max_length=2,
        choices=Grade.choices,
        default=Grade.TRAINEE
    )
    education = models.TextField(max_length=255, verbose_name="Образование")
    experience = models.TextField(max_length=255, verbose_name="Опыт работы")
    portfolio = models.URLField(verbose_name='Портфолио')
