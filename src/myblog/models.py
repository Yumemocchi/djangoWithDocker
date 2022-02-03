from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify


# Chaque class qui hérite de models.Model va créer une table en base avec les champs correspondants
class PostBlog(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    title_tag = models.CharField(max_length=255, blank="True")
    slug = models.SlugField(null=False, unique=True)
    post_description = models.CharField(max_length=500, default='Description')
    text_post = models.TextField(blank=True, verbose_name="Contenu")
    created_date_post = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=100, default='devlog')
    pusblished = models.BooleanField(default=False, verbose_name="Publié")
    picture = models.ImageField(upload_to='post_img', default='None')
    # Many likes to Many posts
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='likes', default=[0])

    # Permet d'afficher Article
    class Meta:
        ordering = ['-created_date_post']
        verbose_name = "Article"

    # property permet de pouvoir faire l'appel comme une propriété et non plus comme une méthode
    @property
    def total_likes(self):
        return self.likes.count()

    # Modifie l'affichage sous forme d'une chaine de caractère des instances d'une classe
    def __str__(self):
        return str(self.title) + ' | ' + str(self.author)

    # va permettre d'ajouter automatiquement un slug à partir du titre
    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)
        except:
            raise ValueError("This title already exist !")

    # Permet de calculer automatiquement l'id de l'url pour afficher le détail du post
    # self représente l'instance de notre classe
    def get_absolute_url(self):
        # return reverse('post_detail', kwargs={'slug': self.slug_title})
        try:
            return reverse('post_detail', args=[self.slug])
            # return reverse('post_detail', args=[str(self.id)])
        except NoReverseMatch:
            print('NoReverseMatch')
            return reverse('blog_home')


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Catégorie"

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('blog_home')


# La foreignKey vers PostBlog va nous permettre de faire l'appel aux commentaires directement via la vue
# PostDetailView
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(PostBlog, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now_add=True)
    upvote = models.ManyToManyField(get_user_model(), blank=True, related_name='upvote', default=[0])
    downvote = models.ManyToManyField(get_user_model(), blank=True, related_name='downvote', default=[0])

    def __str__(self):
        return '%s' % self.post.title

    @property
    def total_upvote(self):
        return self.upvote.count()

    @property
    def total_downvote(self):
        return self.downvote.count()

    def get_username(self):
        return self.author_id
