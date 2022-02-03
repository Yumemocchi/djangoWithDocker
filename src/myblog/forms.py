from django import forms

from .models import PostBlog, Category


cats = Category.objects.all().values_list('name', 'name')
cat_liste = []

for item in cats:
    cat_liste.append(item)


# On crée le formulaire de création de post avec les champs qui nous intéressent
# On importe donc le modèle que l'on souhaite alimenter via le formulaire
class PostForm(forms.ModelForm):

    class Meta:
        model = PostBlog
        fields = ('category', 'title', 'title_tag', 'post_description', 'text_post')

        widgets = {
            # 'author': forms.TextInput(attrs={'class': 'form-control', 'value': 'user_id', 'id': 'author_id',
            #                                  'disabled': 'disabled'}),
            'category': forms.Select(choices=cat_liste, attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'post_description': forms.TextInput(attrs={'class': 'form-control'}),
            'text_post': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = PostBlog
        fields = ('category', 'title', 'title_tag', 'post_description', 'text_post')

        widgets = {
            # 'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=cat_liste, attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'post_description': forms.TextInput(attrs={'class': 'form-control'}),
            'text_post': forms.Textarea(attrs={'class': 'form-control'})
        }

