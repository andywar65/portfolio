from django.contrib import admin

from .models import Project, ProjectImage
from pages.admin import GalleryImageInline

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    fields = ('fb_image', 'caption', 'position')
    sortable_field_name = "position"
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', )
    inlines = [ GalleryImageInline,  ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]
