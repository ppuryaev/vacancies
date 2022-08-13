import vacancy.data as vacancy_data
from vacancy.models import Vacancy, Specialty, Company


def insert_jobs(jobs):
    for job in jobs:
        Vacancy.objects.create(
            title=job.get('title'),
            specialty=Specialty.objects.get(code=job.get('specialty')),
            company=Company.objects.get(id=job.get('company')),
            skills=job.get('skills'),
            description=job.get('description'),
            salary_min=job.get('salary_from'),
            salary_max=job.get('salary_to'),
            published_at=job.get('posted')
        )
    return


def insert_speciality(specialities):
    for speciality in specialities:
        Specialty.objects.create(
            code=speciality.get('code'),
            title=speciality.get('title')
        )
    return


def insert_company(companies):
    for company in companies:
        Company.objects.create(
            name=company.get('title'),
            location=company.get('location'),
            logo=company.get('logo'),
            description=company.get('description'),
            employee_count=company.get('employee_count')
        )
    return


def main():
    insert_speciality(vacancy_data.specialties)
    insert_company(vacancy_data.companies)
    insert_jobs(vacancy_data.jobs)


if __name__ == '__main__':
    main()
