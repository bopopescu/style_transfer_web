from django import forms

class UploadFileForm(forms.Form):
    content = forms.FileField()
    style = forms.FileField()