import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Finch, Toy, Photo
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
  # Get the toys the finch doesn't have...
  # First, create a list of the toy ids that the finch DOES have
  id_list = finch.toys.all().values_list('id')
  # Now we can query for toys whose ids are not in the list using exclude
  toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
  
  #instantiate FeedingForm to be rendered in detail.html
  feeding_form = FeedingForm()
  #"context" is what the dict -> template to be rendered
  return render(request, 'finch/detail.html', {
    'finch': finch,
    'feeding_form': feeding_form,
    # Add the toys to be displayed
    'toys': toys_cat_doesnt_have
  })

class FinchCreate(CreateView):
  model = Finch
  fields = ['name', 'breed', 'description']

class FinchUpdate(UpdateView):
  model = Finch
  #able to limit which fields you can actually update/edit
  fields = ['name', 'breed', 'description']

class FinchDelete(DeleteView):
  model = Finch
  success_url = '/finches'
  fields = ['name', 'breed', 'description']

def add_feeding(request, finch_id):
  # create a ModelForm instance using the data tht was submitted in the form
  form = FeedingForm(request.POST)
  #validate the form
  if form.is_valid():
    # we want a model instance, but
    # we cant save to the db bc we have not assigned the finch_id FK
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys'

def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)

def add_photo(request, finch_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, finch_id=finch_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', finch_id=finch_id)