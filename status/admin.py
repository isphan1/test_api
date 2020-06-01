from django.contrib import admin
from .forms import statusForm
from .models import Status
from django.utils import timezone

# Register your models here.


def ship(modeladmin,request,queryset):
    queryset.update(
        is_staff=True,
        updated=timezone.now()
    )
ship.short_description = "Mark user as staff"

@admin.register(Status)
class statusAdmin(admin.ModelAdmin):
    list_display = ['__str__','unique_name','slug','featured','is_staff','timestamp']
    list_filter = ['timestamp','updated']
    search_fields = ('content',)
    ordering = ['timestamp']
    date_hierarchy = 'updated'
    list_editable = ['is_staff']
    prepopulated_fields = {'slug':('content',)}
    actions =[ship]
    form = statusForm
    radio_fields = {'featured':admin.HORIZONTAL}
    fieldsets =(
        (None,{
        'fields':(('user','image'),'slug')
    }),

    ('Description',{
        # 'classes':('collapse',),
        'fields':(('content','is_staff',),
        'featured')
    })
    
    )



