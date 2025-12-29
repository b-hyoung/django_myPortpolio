from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '노트 제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '여기에 노트를 작성하세요'}),
        }
