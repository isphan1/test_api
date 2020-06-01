from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from blog.models import BlogPost 
from blog.forms import userForm

# Create your views here.

def index(request):

    form = userForm()

    if request.method == "POST":
        data = userForm(request.POST)

        if data.is_valid():
            user = BlogPost(user=request.user,content=request.POST['content'],image=request.POST['image'])
            user.save()
    else:
        form = userForm()

    data = BlogPost.objects.all()

    return render(request,'pages/home.html',{'data':data,'form':form})
    