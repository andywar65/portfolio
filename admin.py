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
        ProjectCarouselInline,
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
                "fields": (
                    "title",
                    "intro",
                    "date",
                    "date_end",
                    "client",
                ),
            },
        ),
        (
            _("Text"),
            {
                "classes": ("grp-collapse grp-closed",),
                "fields": ("body",),
            },
        ),
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
class ActivityAdmin(TranslationAdmin):
    list_display = (
        "abbrev",
        "full",
    )
