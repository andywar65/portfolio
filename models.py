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

def project_default_intro():
    return _('Another Project by %(website)s!') % {'website': settings.WEBSITE_NAME}

def project_station_default_intro():
    pass
