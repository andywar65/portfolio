from django.utils.translation import gettext as _

CATEGORY = [
    ("ALT", _("Other")),
    ("RES", _("Residential")),
    ("TER", _("Offices")),
    ("SAN", _("Hospitals")),
    ("PRO", _("Production")),
    ("SCO", _("Schools")),
]

TYPE = [
    ("ALT", _("Other")),
    ("ARR", _("Furniture")),
    ("RIS", _("Refurbishment")),
    ("RES", _("Restoration")),
    ("AMP", _("Extension")),
    ("COS", _("Construction")),
    ("DEM", _("Demolition")),
]

STATUS = [
    ("ALT", _("Other")),
    ("PRO", _("Designed")),
    ("COR", _("Under construction")),
    ("REA", _("Done")),
]

COST = [
    ("ALT", _("Other")),
    ("1K", "1K"),
    ("10K", "10K"),
    ("100K", "100K"),
    ("1M", "1M"),
    ("10M", "10M"),
]

ACTIVITY = [
    ("LP0", _("Other")),
    ("LP1", _("Feasibility study")),
    ("LP2", _("Preliminary design")),
    ("LP3", _("Definitive design")),
    ("LP4", _("Authoring")),
    ("LP5", _("Construction design")),
    ("LP6", _("Tender design")),
    ("LP7", _("Project management")),
    ("LP8", _("Construction supervision")),
    ("LP9", _("Maintenance design")),
]
