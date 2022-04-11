from django.contrib import admin
from django.utils.translation import gettext as _
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import Activity, Project, ProjectCarousel


class ProjectCarouselInline(TranslationTabularInline):
    model = ProjectCarousel
    fields = (
        "position",
        "fb_image",
        "description",
    )
    sortable_field_name = "position"
    extra = 0


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = (
        "title",
        "intro",
    )
    inlines = [
        ProjectCarousel,
    ]

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "date", "intro"),
            },
        ),
        (
            _("Text"),
            {
                "classes": ("grp-collapse grp-closed",),
                "fields": ("body",),
            },
        ),
        (_("Gallery"), {"classes": ("placeholder project_image-group",), "fields": ()}),
        (
            _("Meta"),
            {
                "fields": (
                    "site",
                    "category",
                    "type",
                    "status",
                    "cost",
                    "activity",
                ),
            },
        ),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "abbrev",
        "full",
    )
