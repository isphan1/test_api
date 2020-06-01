from django import forms
from .models import BlogPost 

class userForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ("user","content",'image')

    def clean_content(self,*args,**kwargs):

        content = self.cleaned_data.get('content')

        if content is None:
            raise forms.ValidationError('This filed cannot blank')
        return content
        


