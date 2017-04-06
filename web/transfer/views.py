from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UploadFileForm,OutputUpload
from .handlers import handle_upload_file,handle_output_file
import yaml
from .models import Task,Slave
def index(request):
    return HttpResponse("Hello, world. You're at the style_transfer index.")


def login(request):
    return HttpResponse("You're at the login page.")

@login_required
def logout_view(request):
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
            handle_upload_file(request,content,style)
            return HttpResponseRedirect('/tasks')
            # return HttpResponse('Upload output successfully.')
        else:
            return HttpResponse('Invalid form.')
    else:
        form = UploadFileForm()
    return render(request, 'transfer/upload.html', {'form': form})

def output(request):
    if request.method == 'POST':
        form = OutputUpload(request.POST, request.FILES)
        if form.is_valid():
            args = yaml.safe_load(request.POST['args'])
            output = request.FILES['output']
            handle_output_file(args,output)
            return HttpResponse('Upload output successfully.')
        else:
            return HttpResponse('Invalid form.')
    else:
        form = OutputUpload()
    return render(request, 'transfer/output.html', {'form': form})



@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    output = ', '.join([t.output for t in tasks])
    return HttpResponse(output)