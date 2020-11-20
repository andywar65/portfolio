from django.utils.translation import gettext as _

CATEGORY = [ ('ALT', _('Other')), ('RES', _('Residential')),
    ('TER', _('Offices')), ('SAN', _('Hospitals')), ('PRO', _('Production')),
    ('SCO', _('Schools')),]

TYPE = [('ALT', _('Other')), ('ARR', _('Furniture')), ('RIS', _('Refurbishment')),
    ('RES', _('Restoration')), ('AMP', _('Extension')), ('COS', _('Construction')),
    ('DEM', _('Demolition')), ]

STATUS = [('ALT', _('Other')), ('PRO', _('Designed')),
    ('COR', _('Under construction')), ('REA', _('Done')), ]

COST = [('ALT', _('Other')), ('1K', '1K'), ('10K', '10K'), ('100K', '100K'),
    ('1M', '1M'), ('10M', '10M'), ]
