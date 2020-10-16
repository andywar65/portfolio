from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from imap_tools import MailBox, AND

from portfolio.models import Project

class Command(BaseCommand):

    def handle(self, *args, **options):

        HOST = settings.IMAP_HOST
        USER = settings.IMAP_USER
        PASSWORD = settings.IMAP_PWD
        PORT = settings.IMAP_PORT
        FROM = settings.IMAP_FROM

        with MailBox(HOST).login(USER, PASSWORD, 'INBOX') as mailbox:
            for message in mailbox.fetch(AND(seen=False, subject='progetti',
                from_=FROM), mark_seen=False):
                pass
                #for att in message.attachments:  # list: [Attachment objects]
                    #file = SimpleUploadedFile(att.filename, att.payload,
                        #att.content_type)
                    #instance = CSVInvoice(csv=file)
                    #instance.save()
