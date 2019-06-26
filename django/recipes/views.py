from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "recipes/home.html")

def vis(request):
    return render(request, "recipes/vis.html")