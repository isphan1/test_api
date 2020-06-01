from django.db import models
from django.conf import settings

# Create your models here.

def upload_update_image(instance,filename):
    return "uploads/{user}/{filename}".format(user=instance.user,filename=filename)


class StatusQuerySet(models.QuerySet):
    pass 


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model,using=self._db)

class Status(models.Model):

    selection_choice = (
        (0,'Open'),
        (1,"Close"),
        (2,"Draft")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_update_image,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    featured = models.IntegerField(choices=selection_choice,default=0)

    objects = StatusManager()

    def __str__(self):
        return self.content[:50]+" ..." 
    
    class Meta:
        verbose_name = 'Status post'
        verbose_name_plural = 'Status posts'
        ordering = ['-id']


    @property
    def unique_name(self):
        return "{} {}".format(self.user,self.timestamp)

    @property

    def owner(self):

        return self.user
        