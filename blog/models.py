from django.db import models
from django.conf import settings
from slugify import slugify

# Create your models here.

def upload_update_image(instance,filename):
    return "media/uploads/{user}/{filename}".format(user=instance.user,filename=filename)

class BlogPost(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to=upload_update_image,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Blog post'

    def __str__(self):
        return self.content[:50]+"..." or ""

    
    def save(self,*args,**kwargs):

        self.slug = slugify(self.content)

        super(BlogPost,self).save(*args, **kwargs) 
