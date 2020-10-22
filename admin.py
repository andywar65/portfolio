from django.contrib import admin

from .models import Project
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
        ('Testo', {
            'classes': ('grp-collapse grp-closed', ),
            'fields': ('body', ),
        }),
        (None, {
            'fields': ('site', 'category', 'type', 'status', 'cost'),
        }),
        )
