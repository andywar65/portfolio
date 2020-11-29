from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Project, ProjectStation, StationImage
from pages.admin import GalleryImageInline

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', )
    inlines = [ GalleryImageInline,  ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]

    fieldsets = (
        (None, {
            'fields': ('title', 'date', 'intro'),
        }),
        (_('Text'), {
            'classes': ('grp-collapse grp-closed', ),
            'fields': ('body', ),
        }),
        (_('Location'), {
            'fields': ('site', 'lat', 'long', 'zoom', ),
        }),
        (_('Meta'), {
            'fields': ('category', 'type', 'status', 'cost'),
        }),
        )

class StationImageInline(admin.TabularInline):
    model = StationImage
    fields = ('date', 'fb_image', 'caption', )
    extra = 0

@admin.register(ProjectStation)
class ProjectStationAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'intro', 'prog',)
    inlines = [ StationImageInline,  ]
