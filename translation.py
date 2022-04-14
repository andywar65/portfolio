from modeltranslation.translator import TranslationOptions, register

from .models import Activity, Project, ProjectCarousel


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "intro",
        "body",
    )
    # required_languages = ('it', 'en')


@register(ProjectCarousel)
class ProjectCarouselTranslationOptions(TranslationOptions):
    fields = ("description",)
    # required_languages = ('it', 'en')


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):
    fields = ("full",)
    # required_languages = ('it', 'en')
