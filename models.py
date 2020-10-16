import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import now

from filebrowser.fields import FileBrowseField

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Titolo',
        help_text="Il titolo del progetto",
        max_length = 50, null=True, blank=True)
    intro = models.CharField('Introduzione',
        default = f'Un altro progetto di {settings.WEBSITE_NAME}!',
        max_length = 100)
    date = models.DateTimeField('Data', default = now, )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f'Progetto-{str(self.id)}'
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Progetto'
        verbose_name_plural = 'Progetti'
        ordering = ('-date', )

class ProjectImage(models.Model):
    prog = models.ForeignKey(Project, on_delete = models.CASCADE,
        related_name='article_uploads')
    image = FileBrowseField("Immagine", max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        null=True, directory='portfolio/projects/')
    caption = models.CharField("Didascalia", max_length = 200, blank=True,
        null=True)
    position = models.PositiveSmallIntegerField("Position", null=True)

    def __str__(self):
        return 'Immagine - ' + str(self.id)

    class Meta:
        verbose_name = 'Immagine'
        verbose_name_plural = 'Immagini'
        ordering = ('position', )
