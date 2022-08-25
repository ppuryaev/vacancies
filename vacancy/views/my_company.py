from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from vacancy.forms import CompanyForm
from vacancy.models import Company


@login_required
def mycompany_letsstart(request):
    user = User.objects.get(pk=request.user.id)
    print('первая страница создания')
    try:
        Company.objects.get(owner=user).id
        return redirect('mycompany_info')
    except Company.DoesNotExist:
        return render(request, 'vacancy/my_company/company-create.html')


@login_required
def mycompany_create(request):
    user = User.objects.get(pk=request.user.id)
    left_menu = False
    try:
        Company.objects.get(owner=user).id
        return redirect('mycompany_info')
    except Company.DoesNotExist:
        form = CompanyForm()
        update = False

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            data = form.cleaned_data
            company = Company.objects.create(
                name=data['name'],
                location=data['location'],
                logo=data['logo'],
                description=data['description'],
                employee_count=data['employee_count'],
                owner=User.objects.get(pk=request.user.id)
            )
            request.session["mycompany_exist"] = company.id
            return redirect('mycompany_info')
    # – Моя компания (пустая форма) /mycompany/create/
    return render(request, 'vacancy/my_company/company-edit.html', context={
                                                                'form': form,
                                                                'update': update,
                                                                'left_menu': left_menu
                                                                })


@login_required
def mycompany_info(request):
    user = User.objects.get(pk=request.user.id)
    left_menu = True

    if 'mycompany_exist' in request.session.keys():
        update = True
        del request.session['mycompany_exist']
    else:
        update = False

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
            return render(request, 'vacancy/my_company/company-edit.html', context={
                                                                                    'form': form,
                                                                                    'company': company,
                                                                                    'update': update,
                                                                                    'left_menu': left_menu
                                                                                    })
    # – Моя компания (заполненная форма) /mycompany/
    return render(request, 'vacancy/my_company/company-edit.html', context={
                                                                            'form': form,
                                                                            'company': company,
                                                                            'update': update,
                                                                            'left_menu': left_menu
                                                                            })
