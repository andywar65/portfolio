import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify

from filebrowser.fields import FileBrowseField

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Titolo',
        help_text="Il titolo del progetto",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Introduzione',
        default = f'Un altro progetto di {settings.WEBSITE_NAME}!',
        max_length = 100)
    body = models.TextField('Testo', null=True)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    date = models.DateField('Data:', default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'Progetto-{str(self.id)}'
            self.slug = f'progetto-{str(self.id)}'
        elif not self.slug:
            self.slug = f'{slugify(self.title)}-{str(self.id)}'
        self.last_updated = now()
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Progetto'
        verbose_name_plural = 'Progetti'
        ordering = ('-date', )
