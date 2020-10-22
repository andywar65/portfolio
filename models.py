import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify

from filebrowser.fields import FileBrowseField

from project.utils import generate_unique_slug
from .choices import *

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    title = models.CharField('Titolo',
        help_text="Il titolo del progetto",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Introduzione',
        default = f'Un altro progetto di {settings.WEBSITE_NAME}!',
        max_length = 100)
    body = models.TextField('Testo', null=True)
    date = models.DateField('Data:', default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)
    site = models.CharField('Luogo', null=True, blank=True,
        help_text = 'Va bene tipo "Roma - Monteverde"',
        max_length = 100)
    category = models.CharField(max_length = 4, choices = CATEGORY,
        default = 'ALT', verbose_name = 'Categoria funzionale', )
    type = models.CharField(max_length = 4, choices = TYPE,
        default = 'ALT', verbose_name = 'Tipo di intervento', )
    status = models.CharField(max_length = 4, choices = STATUS,
        default = 'ALT', verbose_name = "Stato dell'intervento", )
    cost = models.CharField(max_length = 4, choices = COST,
        default = 'ALT', verbose_name = "Costo dell'intervento", )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'Progetto-{self.date.strftime("%d-%m-%y")}'
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.title)
        self.last_updated = now()
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Progetto'
        verbose_name_plural = 'Progetti'
        ordering = ('-date', )
