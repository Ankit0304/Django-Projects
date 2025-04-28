from django.shortcuts import render, get_object_or_404, redirect
from .models import Notes
from .forms import Notesform

# Create your views here.

def note_list(request):
    notes = Notes.objects.all()
    return render(request, 'note_list.html', {'notes': notes})

def note_detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    return render(request, 'note_detail.html', {'note': note})

def note_create(request):
    if request.method == 'POST':
        form = Notesform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = Notesform()
    return render(request, 'note_form.html', {'form': form})
    
def note_update(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    if request.method == 'POST':
        form = Notesform(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = Notesform(instance=note)
    return render(request, 'note_form.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

