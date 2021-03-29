from django.shortcuts import render
from .forms import EnvForm

def index(request):
    
    if request.method == 'POST':
        form = EnvForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EnvForm()

    return render(request,'index.html', {"form": form})
