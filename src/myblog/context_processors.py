from myblog.models import Category


# context processor
# Use to display on all templates
def cat_list_view(request):
    cat_list = [str(i).title() for i in Category.objects.all()]
    return {'cat_list': cat_list}
