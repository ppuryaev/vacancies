from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from vacancy.forms import ResumeForm
from vacancy.models import Resume


@login_required
def myresume_letsstart(request):
    user = User.objects.get(pk=request.user.id)
    try:
        Resume.objects.get(user=user).id
        return redirect('myresume_info')
    except Resume.DoesNotExist:
        return render(request, 'vacancy/my_cv/resume-create.html')


@login_required
def myresume_create(request):
    user = User.objects.get(pk=request.user.id)
    try:
        Resume.objects.get(user_id=user).id
        return redirect('myresume_info')
    except Resume.DoesNotExist:
        form = ResumeForm()
        form.initial['name'] = user.first_name
        form.initial['surname'] = user.last_name
        update = False

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            data = form.cleaned_data
            resume = Resume.objects.create(
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
            request.session["myresume_exist"] = resume.id
            return redirect('myresume_info')

    return render(request, 'vacancy/my_cv/resume-edit.html', context={
                                                                'form': form,
                                                                'update': update
                                                                })


@login_required
def myresume_info(request):
    user = User.objects.get(pk=request.user.id)

    if 'myresume_exist' in request.session.keys():
        update = True
        del request.session['myresume_exist']
    else:
        update = False

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
            return render(request, 'vacancy/my_cv/resume-edit.html', context={
                                                                        'form': form,
                                                                        'update': update
                                                                        })
    return render(request, 'vacancy/my_cv/resume-edit.html', context={
                                                                'form': form,
                                                                'update': update
                                                                })
