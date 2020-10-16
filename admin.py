from django.contrib import admin

from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    fields = ('image', 'caption', 'position')
    sortable_field_name = "position"
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', )
    inlines = [ ProjectImageInline,  ]
