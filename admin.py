from django.contrib import admin

from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    fields = ('image', 'caption', )
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('get_title', )
    inlines = [ ProjectImageInline,  ]
