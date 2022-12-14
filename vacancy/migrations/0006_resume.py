# Generated by Django 4.1 on 2022-08-22 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vacancy', '0005_alter_company_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('status', models.CharField(choices=[('LR', 'Ищу работу'), ('NR', 'Не ищу работу'), ('WG', 'Рассматриваю предложения')], default='NR', max_length=2)),
                ('salary', models.IntegerField(verbose_name='Вознаграждение')),
                ('grade', models.CharField(choices=[('TE', 'Стажер'), ('JR', 'Джуниор'), ('ME', 'Миддл'), ('SR', 'Синьор'), ('LD', 'Лид')], default='TE', max_length=2)),
                ('education', models.TextField(max_length=255, verbose_name='Образование')),
                ('experience', models.TextField(max_length=255, verbose_name='Опыт работы')),
                ('portfolio', models.URLField(verbose_name='Портфолио')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialty', to='vacancy.specialty', verbose_name='Специализация')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
