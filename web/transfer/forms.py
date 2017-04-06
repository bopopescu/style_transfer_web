from django import forms

class UploadFileForm(forms.Form):
    content = forms.FileField()
    style = forms.FileField()

class OutputUpload(forms.Form):
    args = forms.CharField()
    output = forms.FileField()