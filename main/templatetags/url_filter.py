from django import template
register = template.Library()

@register.filter
def urlFilter(url):
    if "sort" in url:
        print(url)
    return url