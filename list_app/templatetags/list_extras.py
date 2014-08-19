from django import template

register = template.Library()

def format_expire_date(list_entry):
    return list_entry.expire_date.strftime("%Y-%m-%d")

def format_create_date(list_entry):
    return list_entry.create_date.strftime("%Y-%m-%d")

register.filter('format_expire_date', format_expire_date)
register.filter('format_create_date', format_create_date)