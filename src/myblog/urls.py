from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import about_view, BlogView, AddPostView, UpdatePostView, DeletePostView, \
    AddCategoryView, category_view, PostDetailView, like_post_view, comment_post_view_create

urlpatterns = [
    # path(url que l'on souhaite utiliser, la vue, le nom que l'on donne à notre vue)
    path('', BlogView.as_view(), name='blog_home'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/edit/<slug:slug>', UpdatePostView.as_view(), name='update_post'),
    path('post/<slug:slug>/remove/', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', category_view, name='category'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('about/', about_view, name='about'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    # path('like/<int:pk>/', like_view, name='post_like'),
    path('post/<slug:slug>/like/', like_post_view, name='post_like'),
    path('post/<slug:slug>/comment/', comment_post_view_create, name='comment'),

    # REST FRAMEWORK URLS
    # <int:pk> va renvoyer l'id du post (voir aussi get_absolute_url dans le models.py
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
