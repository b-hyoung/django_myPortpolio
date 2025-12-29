from django.shortcuts import render, get_object_or_404
from .models import Note # Import the Note model

def index(request):
    notes = Note.objects.all().order_by("-created_at") # Fetch all notes, ordered by creation date
    return render(request, 'notes/index.html', {'notes': notes}) # Pass notes to the template

def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})