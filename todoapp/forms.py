from django.forms import ModelForm
from .models import Todo

class CreateTodo(ModelForm):
    class Meta:
        model = Todo
        fields = ['title','details', 'important']
