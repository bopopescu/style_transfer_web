from django import forms

class UploadFileForm(forms.Form):
    content = forms.FileField()
    style = forms.FileField()

class OutputUpload(forms.Form):
    task_id = forms.IntegerField()
    output = forms.FileField()