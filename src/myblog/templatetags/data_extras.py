from django import template


register = template.Library()


# To filter queryset in the django template
@register.filter
def user_in_queryset(user, queryset):
    if user in queryset:
        return True
    return False

