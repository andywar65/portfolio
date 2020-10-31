import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify

from filebrowser.fields import FileBrowseField

from project.utils import generate_unique_slug
from .choices import *

def project_default_intro():
    return f'Un altro progetto di {settings.WEBSITE_NAME}!'


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    title = models.CharField('Titolo',
        help_text="Il titolo del progetto",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Introduzione',
        default = project_default_intro,
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

    def get_full_path(self):
        return f'/progetti/{self.slug}'

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

def project_station_default_intro():
    return f'Un altra postazione fotografica di {settings.WEBSITE_NAME}!'

class ProjectStation(models.Model):

    prog = models.ForeignKey(Project, on_delete = models.CASCADE,
        related_name='project_station', verbose_name = 'Progetto')
    title = models.CharField('Titolo',
        help_text="Il titolo della postazione fotografica", max_length = 50, )
    slug = models.SlugField(max_length=100, editable=False, null=True)
    intro = models.CharField('Descrizione',
        default = project_station_default_intro,
        max_length = 100)

    def __str__(self):
        return self.title + ' / ' + self.prog.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(ProjectStation, self.title)
        super(ProjectStation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Stazione fotografica'
        verbose_name_plural = 'Stazioni fotografiche'
        ordering = ('prog', 'title')

class StationImage(models.Model):
    stat = models.ForeignKey(ProjectStation, null=True, editable=False,
        on_delete = models.CASCADE, related_name='station_image')
    date = models.DateTimeField('Data:', default = now, )
    image = models.ImageField("Immagine", max_length=200, editable = False,
        null=True, upload_to='uploads/images/galleries/')
    fb_image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='images/galleries/')
    caption = models.CharField("Didascalia", max_length = 200, blank=True,
        null=True)
    position = models.PositiveSmallIntegerField("Posizione", null=True)

    class Meta:
        verbose_name="Immagine"
        verbose_name_plural="Immagini"
