from django.forms import ModelForm
from .models import Posts
from django import forms
from .models import Comment



class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
    
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['subtitulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen_portada'].widget.attrs.update({'class': 'form-control'})

class ContactoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    apellido = forms.CharField(label='Apellido', max_length=100)
    email = forms.EmailField(label='Correo electrónico', max_length=100)
    consulta = forms.CharField(label='Consulta', widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']