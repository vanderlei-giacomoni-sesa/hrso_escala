from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


@login_required
def inicio(request):

    return render(request, 'inicio.html')