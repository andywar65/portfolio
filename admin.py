from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Project, ProjectStation, StationImage, ProjectMapDxf
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
        (_("Gallery"), {"classes": ("placeholder project_image-group",),
            "fields" : ()}),
        (_('Meta'), {
            'fields': ('site', 'category', 'type', 'status', 'cost'),
        }),
        (_('Map'), {
            'fields': ('lat', 'long', 'zoom', ),
        }),
        )

class StationImageInline(admin.TabularInline):
    model = StationImage
    fields = ('date', 'fb_image', 'caption', )
    extra = 0

@admin.register(ProjectStation)
class ProjectStationAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'intro', 'prog', 'lat', 'long')
    list_editable = ( 'lat', 'long')
    inlines = [ StationImageInline,  ]

@admin.register(ProjectMapDxf)
class ProjectMapDxfAdmin(admin.ModelAdmin):
    list_display = ( 'prog', 'file')
