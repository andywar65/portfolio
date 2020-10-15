import uuid
from django.db import models
from django.conf import settings

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Titolo',
        help_text="Il titolo del progetto",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Introduzione',
        default = f'Un altro progetto di {settings.WEBSITE_NAME}!',
        max_length = 100)

    def __str__(self):
        return self.title if self.title else self.id

    class Meta:
        verbose_name = 'Progetto'
        verbose_name_plural = 'Progetti'
