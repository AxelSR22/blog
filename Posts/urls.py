from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<str:pk>/', views.post, name="post"),
    path('form_post/', views.formulario, name="formPost"),
    path('categorias/', views.categorias, name='categorias'),
    path('categoria/<int:pk>/', views.detalle_categoria, name='categoria_detalle'),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),
    path('update-post/<str:pk>/', views.updatePost, name="update-post"),
    path('about/', views.about, name='about'),
    path('contacto/', views.contacto, name='contacto'),
    path('agregar-post/', views.formulario, name='formPost'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('registro/', views.registro, name='registro'),
]
