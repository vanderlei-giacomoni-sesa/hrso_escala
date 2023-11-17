from django.shortcuts import redirect, render


def inicio(request):
    return render(request, 'inicio.html')