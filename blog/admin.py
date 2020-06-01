from django.contrib import admin

from blog.models import BlogPost
# Register your models here.


@admin.register(BlogPost)
class userAdmin(admin.ModelAdmin):
    list_display =['__str__','slug','content','timestamp']
    prepopulated_fields = {'slug':('content',)}
