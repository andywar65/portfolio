from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from filebrowser.fields import FileBrowseField
from project.utils import generate_unique_slug

from .choices import CATEGORY, COST, STATUS, TYPE


def project_default_intro():
    # following try/except for test to work
    try:
        current_site = Site.objects.get_current()
        return _("Another project by %(name)s!") % {"name": current_site.name}
    except Site.DoesNotExist:
        return _("Another project by this site!")


class Activity(models.Model):
    full = models.CharField(
        max_length=32,
        verbose_name=_("Name"),
    )
    abbrev = models.CharField(
        max_length=4,
        verbose_name=_("Code name"),
    )

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ("abbrev",)


class Project(models.Model):
    slug = models.SlugField(max_length=100, editable=False, null=True)
    title = models.CharField(
        _("Title"),
        help_text=_("Title of the project"),
        max_length=50,
        null=True,
        blank=True,
    )
    intro = models.CharField(
        _("Introduction"), default=project_default_intro, max_length=100
    )
    body = models.TextField(_("Text"), null=True)
    date = models.DateField(
        _("Date:"),
        default=now,
    )
    last_updated = models.DateTimeField(editable=False, null=True)
    site = models.CharField(
        _("Site"),
        null=True,
        blank=True,
        help_text=_('Something like "Rome - Monteverde"'),
        max_length=100,
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY,
        default="ALT",
        verbose_name=_("Functional category"),
    )
    type = models.CharField(
        max_length=4,
        choices=TYPE,
        default="ALT",
        verbose_name=_("Type of intervention"),
    )
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default="ALT",
        verbose_name=_("Status of intervention"),
    )
    cost = models.CharField(
        max_length=4,
        choices=COST,
        default="ALT",
        verbose_name=_("Cost of intervention"),
    )
    activity = models.ManyToManyField(
        Activity,
        blank=True,
        verbose_name=_("Performed activities"),
    )

    def __str__(self):
        return self.title

    def get_full_path(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def get_activities(self):
        list = []
        for act in self.activity.all():
            list.append(act.full)
        s = ", "
        s = s.join(list)
        return s

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = _("Project-%(date)s") % {
                "date": self.date.strftime("%d-%m-%y")
            }
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.title)
        self.last_updated = now()
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("-date",)


class ProjectCarousel(models.Model):

    home = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_carousel",
        verbose_name=_("Project"),
    )
    fb_image = FileBrowseField(
        _("Image"),
        max_length=200,
        extensions=[".jpg", ".png", ".jpeg", ".gif", ".tif", ".tiff"],
        directory="images/",
    )
    description = models.CharField(
        _("Description"),
        help_text=_("Will be used in captions"),
        max_length=100,
        null=True,
        blank=True,
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _("Project carousel")
        verbose_name_plural = _("Project carousels")
        ordering = [
            "position",
        ]
