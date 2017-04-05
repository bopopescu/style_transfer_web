#encoding=utf8
from django.conf import settings
from django.utils import timezone
from .models import Task,Slave
from .master import master
import uuid
import os
def handle_upload_file(request,content,style):
    print settings.CONTENT_DIR
    print content,style
    content_storage = os.path.join(settings.CONTENT_DIR,str(uuid.uuid4())+os.path.splitext(content.name)[1])
    style_storage = os.path.join(settings.STYLE_DIR, str(uuid.uuid4())+os.path.splitext(style.name)[1])
    with open(content_storage,'wb') as destination:
        for chunk in content.chunks():
            destination.write(chunk)
        destination.close()
    with open(style_storage,'wb') as destination:
        for chunk in style.chunks():
            destination.write(chunk)
        destination.close()
    task = Task(content=content_storage,style=style_storage,user=request.user,sub_time=timezone.now())
    task.save()
    m = master()
    args = {'task_id':task.id,'content': content_storage, 'style': style_storage, 'model': 'vgg16', 'ratio': 1e4}
    m.dispatch('10.0.0.64', 8667, args)
    print task.id