from pyexpat import model
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    return render(request,'cats/index.html', { 'cats': cats})

# update this view function

@login_required
def cats_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  # instantiate FeedingForm to be rendered in the template
  feeding_form = FeedingForm()

  # displaying unassociated toys
  toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))

  return render(request, 'cats/detail.html', {
    # include the cat and feeding_form in the context
    'cat': cat,
    'feeding_form': feeding_form,
    'toys' : toys_cat_doesnt_have,
  })

@login_required
def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)

@login_required
def assoc_toy(request, cat_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
   Cat.objects.get(id=cat_id).toys.add(toy_id)
   return redirect('detail', cat_id=cat_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
     form = UserCreationForm(request.POST)
     if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
     else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)   

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # success_url = '/cats/' 

    # This inherited method is called when a
    # valid cat form is being submitted
    def form_valid(self, form):
    # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('breed', 'description', 'age')

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ('name', 'color')

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'