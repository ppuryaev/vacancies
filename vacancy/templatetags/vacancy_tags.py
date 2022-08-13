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
