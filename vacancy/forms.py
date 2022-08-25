from django import forms

from vacancy.models import Application, Company, Vacancy, Specialty, Resume


class SubmitFrom(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']
        widgets = {
            'written_username': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': '',
                'id': 'userName'
            }),
            'written_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'placeholder': 'Введите номер телефона в формате +7 (999) 999-99-99',
                'id': 'userPhone'
            }),
            'written_cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '8',
                'placeholder': '',
                'id': 'userMsg'
            }),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'employee_count', 'location', 'logo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'companyName'
            }),
            'employee_count': forms.TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'id': "companyTeam"
            }),
            'location': forms.TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'id': "companyLocation"
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "4",
                'style': "color:#000;",
                'id': "companyInfo"
            }),
            'logo': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            })

        }


# Страшная реализация через костомную функцию - не позволяет в форме показывать элемент из базы,
# по факту всегда в форме стоял выбор - фронтенд
# class SpecialtiesModelChoiceField(forms.ModelChoiceField):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.empty_label = None
#    def label_from_instance(self, obj):
#        return obj.title
#    def widget_attrs(self, widget):
#        return {'class': 'custom-select mr-sm-2'}


class VacancyForm(forms.ModelForm):
    # specialties = forms.ModelChoiceField(queryset=Specialty.objects.values('title').distinct())
    # specialties = SpecialtiesModelChoiceField(queryset=Specialty.objects.all())
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(),
                                       empty_label=None,
                                       widget=forms.Select(attrs={
                                           'class': 'custom-select mr-sm-2'
                                       })
                                       )

    class Meta:
        model = Vacancy
        fields = ['title', 'skills', 'description', 'salary_min', 'salary_max', 'specialty']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'salary_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Разделяйте навыки с помощью запятой - ", "'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '13'
            })
        }


class ResumeForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(),
                                       empty_label=None,
                                       widget=forms.Select(attrs={
                                           'class': 'custom-select mr-sm-2'
                                       })
                                       )

    class Meta:
        model = Resume
        fields = ['name', 'surname', 'status', 'salary', 'specialty', 'grade',
                  'education', 'experience', 'portfolio']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'status': forms.Select(attrs={
                'class': 'custom-select mr-sm-2'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'grade': forms.Select(attrs={
                'class': 'custom-select mr-sm-2'
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control text-uppercase',
                'rows': '4',
                'style': 'color:#000;'
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'style': 'color:#000;'
            }),
            'portfolio': forms.URLInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'http://anylink.github.io'
            })
        }
