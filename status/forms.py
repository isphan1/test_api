from django import forms
from .models import Status

class statusForm(forms.ModelForm):

    class Meta:
        model = Status

        fields = ['user','content','image','is_staff','featured','slug']



    def clean_content(self,*args,**kwargs):
        content = self.cleaned_data.get('content')

        if len(content) >240:
            raise forms.ValidationError('Content is too long')
        return content

    def clean(self,*args,**kwargs):

        data = self.cleaned_data
        content = data.get('content',None)
        if content == "":
            content = None
        image = data.get('image',None)
        print(image)
        if content is None or image is None:
            raise forms.ValidationError('content or image is required')
        return super().clean(*args,**kwargs)


        

