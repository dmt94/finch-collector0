from django.shortcuts import render

finches = [
  {'name': 'Leo', 'breed': 'finch1', 'description': 'fun bird'},
  {'name': 'Luna', 'breed': 'finch2', 'description': 'chill bird'},
  ]

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# Add new view
def finch_index(request):
  # We pass data to a template very much like we did in Express!
  return render(request, 'finch/index.html', {
    'finches': finches
  })
