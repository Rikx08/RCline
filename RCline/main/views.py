from django.shortcuts import render
from .models import Tovars

def index(request):
    if request.method == "POST":
        tovar = Tovars()
        if request.POST.get('name'):
            tovar.name = request.POST.get('name')
        else:
            tovar.name = "none"
        if request.POST.get('desc'):
            tovar.description = request.POST.get('desc')
        else:
            tovar.description = "none"
        tovar.save()
        return render(request, "main/main.html")
    else:
        return render(request,"main/main.html")







