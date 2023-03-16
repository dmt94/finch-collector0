from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# Add new view
def finch_index(request):
  # We pass data to a template very much like we did in Express!
  finches = Finch.objects.all()
  return render(request, 'finch/index.html', {
    'finches': finches
  })

def finch_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  #instantiate FeedingForm to be rendered in detail.html
  feeding_form = FeedingForm()
  #"context" is what the dict -> template to be rendered
  return render(request, 'finch/detail.html', {
    'finch': finch,
    'feeding_form': feeding_form
  })

class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'

class FinchUpdate(UpdateView):
  model = Finch
  #able to limit which fields you can actually update/edit
  fields = ['name', 'breed', 'description']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'
  fields = ['name', 'breed', 'description']
