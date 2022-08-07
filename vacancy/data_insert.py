import vacancy.data as vacancy_data
from vacancy.models import Vacancy, Specialty, Company


def insert_jobs(jobs):
    for job in jobs:
        row = Vacancy.objects.create(
            title=job.get('title'),
            specialty=Specialty.objects.get(code=job.get('specialty')),
            company=Company.objects.get(id=job.get('company')),
            skills=job.get('skills'),
            description=job.get('description'),
            salary_min=job.get('salary_from'),
            salary_max=job.get('salary_to'),
            published_at=job.get('posted')
        )


def insert_speciality(specialities):
    for speciality in specialities:
        row = Specialty.objects.create(
            code=speciality.get('code'),
            title=speciality.get('title')
        )


def insert_company(companies):
    for company in companies:
        row = Company.objects.create(
            name=company.get('title'),
            location=company.get('location'),
            logo=company.get('logo'),
            description=company.get('description'),
            employee_count=company.get('employee_count')
        )


def main():
    insert_speciality(vacancy_data.specialties)
    insert_company(vacancy_data.companies)
    insert_jobs(vacancy_data.jobs)
