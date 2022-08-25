from django import template


register = template.Library()


@register.filter(name='make_list_make_join')
def make_list_make_join(vacancy_object):
    skills_list = vacancy_object.split(', ')
    skills_row = (' • ').join(skills_list)
    return skills_row


@register.filter(name='human_number')
def human_number(int_number):
    number_to_view = '{:,}'.format(int_number).replace(',', ' ')
    return number_to_view


@register.filter(name='suffix_cnt_vacancy')
def suffix_cnt_vacancy(int_number):
    words_suffix = ['вакансия', 'вакансии', 'вакансий']
    ostatok_vac = int(int_number) % 100
    if ostatok_vac >= 10 and ostatok_vac <= 20:
        print_word = words_suffix[2]
    else:
        ostastok_last = ostatok_vac % 10
        if ostastok_last == 1:
            print_word = words_suffix[0]
        elif ostastok_last in [2, 3, 4]:
            print_word = words_suffix[1]
        else:
            print_word = words_suffix[2]
    return str(int_number)+' '+print_word


@register.filter(name='suffix_cnt_application')
def suffix_cnt_application(int_number):
    words_suffix = ['отклик', 'отклика', 'откликов']
    ostatok = int(int_number) % 100
    if ostatok >= 10 and ostatok <= 20:
        print_word = words_suffix[2]
    else:
        ostastok_last = ostatok % 10
        if ostastok_last == 1:
            print_word = words_suffix[0]
        elif ostastok_last in [2, 3, 4]:
            print_word = words_suffix[1]
        else:
            print_word = words_suffix[2]
    return str(int_number) + ' ' + print_word
