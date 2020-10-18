from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from imap_tools import MailBox, AND

from portfolio.models import Project, ProjectImage

def do_command():

    HOST = settings.IMAP_HOST
    USER = settings.IMAP_USER
    PASSWORD = settings.IMAP_PWD
    PORT = settings.IMAP_PORT
    FROM = settings.IMAP_FROM

    with MailBox(HOST).login(USER, PASSWORD, 'INBOX') as mailbox:
        for message in mailbox.fetch(AND(seen=False, subject='progetti',
            from_=FROM), mark_seen=True):
            msg = message.text
            d = {'title': 'TITOLO[', 'intro': 'DESCRIZIONE[',
                'body': 'TESTO[', }
            for key, value in d.items():
                msg = msg.replace(value, '')
                d[key] = msg.split(']', 1)[0]
                msg = msg.split(']', 1)[1]
            prog = Project(title=d['title'], intro=d['intro'], body=d['body'])
            prog.save()
            for att in message.attachments:  # list: [Attachment objects]
                file = SimpleUploadedFile(att.filename, att.payload,
                    att.content_type)
                position = att.filename.split('-', 1)[0]
                caption = att.filename.split('-', 1)[1]
                caption = caption.rsplit('.', 1)[0]
                instance = ProjectImage(prog_id=prog.id, image=file,
                    position=position, caption=caption)
                instance.save()

class Command(BaseCommand):

    def handle(self, *args, **options):
        do_command()
