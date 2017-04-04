from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UploadFileForm

from .models import Task,Slave
def index(request):
    return HttpResponse("Hello, world. You're at the style_transfer index.")


def login(request):
    return HttpResponse("You're at the login page.")

@login_required
def logout(request):
    logout(request)
    return HttpResponse("You have logged out")

@login_required
def upload(request):
    # return HttpResponse("You're at the upload page.")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES['content']
            style = request.FILES['style']
            print content,type(content)
            return HttpResponseRedirect('/tasks')
        else:
            print 'invalid form'
    else:
        form = UploadFileForm()
    return render(request, 'transfer/upload.html', {'form': form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    output = ', '.join([t.content for t in tasks])
    return HttpResponse(output)