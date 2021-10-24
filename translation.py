from modeltranslation.translator import translator, TranslationOptions
from .models import Project

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'body', )
    required_languages = ('it', 'de')

translator.register(Project, ProjectTranslationOptions)
