from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

def create_portfolio_group(sender, **kwargs):
    from django.contrib.auth.models import Permission, Group
    grp, created = Group.objects.get_or_create(name=_('Project Manager'))
    if created:
        permissions = Permission.objects.filter(codename__in=('view_project',
            'add_project', 'change_project', 'delete_project',
            'view_projectstation', 'add_projectstation', 'change_projectstation',
            'delete_projectstation', 'view_stationimage', 'add_stationimage',
            'change_stationimage', 'delete_stationimage', ))
        grp.permissions.set(permissions)

class PortfolioConfig(AppConfig):
    name = 'portfolio'

    def ready(self):
        post_migrate.connect(create_portfolio_group, sender=self)
