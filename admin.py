from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Project, Activity
#from pages.admin import GalleryImageInline

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', )
    #inlines = [ GalleryImageInline,  ]

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
            'fields': ('site', 'category', 'type', 'status', 'cost', 'activity', ),
        }),
        )

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('abbrev', 'full', )
