from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
import locale

from myblog.models import PostBlog, Category, Comment
from myblog.forms import PostForm, UpdateForm
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods


# Create your views here.
# ListView pour une liste de posts
class BlogView(ListView):
    # model utilise le modèle de base de donnée que l'on souhaite appeler
    model = PostBlog
    # cats = Category.objects.all()
    # template_name renvoie vers le template html que l'on souhaite appeler
    template_name = 'myblog/blog.html'
    ordering = ['-created_date_post', '-id']


# Détail d'un post en particulier sans serializer
class PostDetailView(DetailView):
    model = PostBlog
    template_name = 'myblog/post.html'


# Pour créer un nouveau post
# LoginRequiredMixin empêche les utilisateurs qui ne sont pas authentifiés d’accéder au formulaire.
# Si vous omettez ça, il sera de votre responsabilité de gérer les utilisateurs non autorisés dans form_valid().
class AddPostView(LoginRequiredMixin, CreateView):
    model = PostBlog
    form_class = PostForm
    template_name = 'myblog/post_create.html'
    # fields = ('title', 'page_title', 'author', 'text')
    # comme on utilise form_class et le formulaire de forms.py, nous n'avons plus besoin des fields

    # Permet de récupérer le user actuel
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Pour créer une nouvelle catégorie
class AddCategoryView(CreateView):
    model = Category
    template_name = 'myblog/category_create.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = PostBlog
    form_class = UpdateForm
    template_name = 'myblog/post_update.html'
    # fields = ['title', 'title_tag', 'title_description', 'text_post']


class DeletePostView(DeleteView):
    model = PostBlog
    template_name = 'myblog/post_delete.html'
    success_url = reverse_lazy('blog_home')


def category_view(request, cats):
    # Appel à la base de données, on récupère dans la table PostBlog les objets pour les catégories = notre liste
    # de catégories
    category_posts = PostBlog.objects.filter(category=str(cats).replace('-', ' '))
    return render(request, 'myblog/categories.html', {'cats': cats.title().replace('-', ' '),
                                                      'category_posts': category_posts})


# Cette vue permet de mettre à jour un like en base puis de renvoyer une réponse JSON
def like_post_view(request, slug):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # On récupère l'objet PostBlog actuel
        post = get_object_or_404(PostBlog, slug=slug)
        # print(request.POST.get('mylikeid'))
        # Si le user a déjà liké le post (si on retrouve l'id dans la liste des likes pour ce post)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return JsonResponse({'post_like_toggle': 'unlike'})
        else:
            post.likes.add(request.user)
            return JsonResponse({'post_like_toggle': 'like'})


@require_http_methods(["POST"])
def comment_post_view_create(request, slug):
    print("passe par la vue")
    # data_response = {}
    # on récupère le post sur lequel est posté le commentaire
    post = get_object_or_404(PostBlog, slug=slug)
    author_id = User(request.POST.get("author_id"))

    # on crée le nouveau commentaire
    new_comment = Comment(message=request.POST.get("txtAreaComment"), author=author_id, post=post)

    if not new_comment.message == '':
        print(new_comment)
        # on enregistre le commentaire en base
        new_comment.save()
        # On récupère l'élément que l'on vient de créer en base
        com = get_object_or_404(Comment, pk=new_comment.id)
        
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
        # com.date_created.strftime("%#d %B %Y") << Windows
        # com.date_created.strftime("%-d %B %Y") << Linux
        return JsonResponse({'com_text': com.message, 'com_author': com.author.username, 'com_date':
                            com.date_created.strftime("%#d %B %Y")})
    return JsonResponse({'None': 'Champ vide'})


def about_view(request):
    return render(request, 'myblog/about.html', {})
