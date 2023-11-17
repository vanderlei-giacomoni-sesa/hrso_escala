from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect

def inicio(request):
    return render(request, 'inicio.html')
