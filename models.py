import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.urls import reverse
from django.core.validators import FileExtensionValidator

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject

from project.utils import generate_unique_slug
from .choices import *
from .map_utils import workflow

def project_default_intro():
    return f'Un altro progetto di {settings.WEBSITE_NAME}!'


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, editable=False, null=True)
    title = models.CharField(_('Title'),
        help_text=_("Title of the project"),
        max_length = 50, null=True, blank=True)
    intro = models.CharField(_('Introduction'),
        default = project_default_intro,
        max_length = 100)
    body = models.TextField(_('Text'), null=True)
    date = models.DateField(_('Date:'), default = now, )
    last_updated = models.DateTimeField(editable=False, null=True)
    site = models.CharField(_('Site'), null=True, blank=True,
        help_text = _('Something like "Rome - Monteverde"'),
        max_length = 100)
    category = models.CharField(max_length = 4, choices = CATEGORY,
        default = 'ALT', verbose_name = _('Functional category'), )
    type = models.CharField(max_length = 4, choices = TYPE,
        default = 'ALT', verbose_name = _('Type of intervention'), )
    status = models.CharField(max_length = 4, choices = STATUS,
        default = 'ALT', verbose_name = _("Status of intervention"), )
    cost = models.CharField(max_length = 4, choices = COST,
        default = 'ALT', verbose_name = _("Cost of intervention"), )
    lat = models.FloatField(_("Latitude"), default = 41.8988)
    long = models.FloatField(_("Longitude"), default = 12.5451)
    zoom = models.FloatField(_("Zoom factor"), default = 10,
        help_text=_("Collect these data fron https://openstreetmap.org"))
    map = models.JSONField(_("Map overlay"), null=True, blank=True)

    def __str__(self):
        return self.title

    def get_full_path(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = _('Project-%(date)s') % {'date': self.date.strftime("%d-%m-%y")}
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.title)
        self.last_updated = now()
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('-date', )

class ProjectMapDxf(models.Model):
    prog = models.ForeignKey(Project, on_delete = models.CASCADE,
        related_name='projectmap_dxf', verbose_name = _('Project'))
    file = models.FileField(_("DXF file"), max_length=200,
        upload_to="uploads/portfolio/projects/maps/dxf/",
        validators=[FileExtensionValidator(allowed_extensions=['dxf', ])])

    def save(self, *args, **kwargs):
        super(ProjectMapDxf, self).save(*args, **kwargs)
        prog = Project.objects.get(id = self.prog_id)
        prog.map = workflow(self.file, prog.lat, prog.long)
        prog.save()

def project_station_default_intro():
    return _('Another photo station by %(sitename)s!') % {'sitename': settings.WEBSITE_NAME}

class ProjectStation(models.Model):

    prog = models.ForeignKey(Project, on_delete = models.CASCADE,
        related_name='project_station', verbose_name = _('Project'))
    title = models.CharField(_('Title'),
        help_text=_("Title of the photo station"), max_length = 50, )
    slug = models.SlugField(max_length=100, editable=False, null=True)
    intro = models.CharField(_('Description'),
        default = project_station_default_intro,
        max_length = 100)
    lat = models.FloatField(_("Latitude"), null=True, blank=True)
    long = models.FloatField(_("Longitude"), null=True, blank=True)

    def __str__(self):
        return self.title + ' / ' + self.prog.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(ProjectStation, self.title)
        if not self.lat:
            self.lat = self.prog.lat
        if not self.long:
            self.long = self.prog.long
        super(ProjectStation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Photo station')
        verbose_name_plural = _('Photo stations')
        ordering = ('prog', 'title')

class StationImage(models.Model):
    stat = models.ForeignKey(ProjectStation, null=True,
        on_delete = models.CASCADE, related_name='station_image',
        verbose_name = _('Station'))
    date = models.DateTimeField(_('Date:'), default = now, )
    image = models.ImageField(_("Image"), max_length=200,
        null=True, upload_to='uploads/images/galleries/')
    fb_image = FileBrowseField(_("Image"), max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='images/galleries/')
    caption = models.CharField(_("Caption"), max_length = 200, blank=True,
        null=True)

    def save(self, *args, **kwargs):
        #save and upload image
        super(StationImage, self).save(*args, **kwargs)
        if self.image and not self.fb_image:
            #save with filebrowser image, sloppy workaround to make working test
            StationImage.objects.filter(id=self.id).update(fb_image=FileObject(str(self.image)))

    class Meta:
        verbose_name=_("Image")
        verbose_name_plural=_("Images")
        ordering = ('-date', )
