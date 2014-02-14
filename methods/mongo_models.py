from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from mongoengine import connect, Document, StringField, IntField, ReferenceField, DateTimeField, BooleanField

from methods.models import sanitise_cccbr_notation

connect(settings.MONGO_DBNAME)


class MongoMethod(Document):
    """
    Method
    """

    id = IntField('id', primary_key=True)

    title = StringField('title', max_length=255, unique=True)
    slug = StringField('slug', max_length=255)
    name = StringField('name', max_length=255)
    raw_notation = StringField('notation', max_length=1023)

    # these two produced from sanitise_cccbr_notation
    notation = StringField('notation', max_length=1023)
    leadHead = StringField('lead head', max_length=63, default='')

    # possible nulls
    leadHeadCode = StringField('lead head code', max_length=31)
    classification = StringField('classification', max_length=255)
    method_notes = StringField('method notes', max_length=255)

    # have own children in xml
    falseness_groups = StringField('fchGroups', max_length=31)

    rw_reference = StringField('"Ringing World" reference', max_length=63)
    bn_reference = StringField('"The Bell News" reference', max_length=63)
    cb_reference = StringField('"Church Bells" reference', max_length=63)
    pmm_reference = StringField('Numerical index in the Plain Minor Methods collection', max_length=63)
    tdmm_reference = StringField('Numerical index in the Treble Dodging Minor Methods collection', max_length=63)

    # performances
    first_hb_peal = ReferenceField('MongoFirstHandbellPeal')
    first_tb_peal = ReferenceField('MongoFirstTowerbellPeal')

    # method set values
    ms_notes = StringField('notes', max_length=255)
    ms_slug = StringField('slug', max_length=255)
    ms_p_stage = IntField('properties->stage', max_value=32)
    ms_p_lengthOfLead = IntField('properties->lengthOfLead')
    ms_p_numberOfHunts = IntField('properties->numberOfHunts')
    ms_p_huntBellPath = StringField('properties->huntBellPath', max_length=511)
    ms_p_symmetry = StringField('properties->symmetry', max_length=31)

    class Meta:
        ordering = ('title',)

    # convenience
    def get_js_notation(self):
        return ''.join(self.notation)

    # convenience
    def get_nchanges(self):
        return (self.ms_p_stage - self.ms_p_numberOfHunts) * self.ms_p_lengthOfLead

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.notation, self.leadHead = sanitise_cccbr_notation(self.raw_notation)
        super(MongoMethod, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('methods:single_method', args=[self.slug, ])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.title


class MongoPerformance(Document):
    """
    Performance - not well sanitised
    """
    date = DateTimeField('date')
    building = StringField('building', max_length=31)
    town = StringField('town', max_length=31)
    county = StringField('county', max_length=31)
    region = StringField('region', max_length=31)
    country = StringField('country', max_length=31)
    address = StringField('address', max_length=31)
    location = StringField('address', max_length=31)

    has_location = BooleanField('has_location', default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for f in self._meta.fields:
            if not isinstance(f, DateTimeField) and getattr(self, f.attname):
                self.has_location = True

        super(MongoPerformance, self).save(*args, **kwargs)


class MongoFirstHandbellPeal(Document):
    date = DateTimeField('date')
    building = StringField('building', max_length=31)
    town = StringField('town', max_length=31)
    county = StringField('county', max_length=31)
    region = StringField('region', max_length=31)
    country = StringField('country', max_length=31)
    address = StringField('address', max_length=31)
    location = StringField('address', max_length=31)

    has_location = BooleanField('has_location', default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for f in self._meta.fields:
            if not isinstance(f, DateTimeField) and getattr(self, f.attname):
                self.has_location = True

        super(MongoFirstHandbellPeal, self).save(*args, **kwargs)


class MongoFirstTowerbellPeal(Document):
    date = DateTimeField('date')
    building = StringField('building', max_length=31)
    town = StringField('town', max_length=31)
    county = StringField('county', max_length=31)
    region = StringField('region', max_length=31)
    country = StringField('country', max_length=31)
    address = StringField('address', max_length=31)
    location = StringField('address', max_length=31)

    has_location = BooleanField('has_location', default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for f in self._meta.fields:
            if not isinstance(f, DateTimeField) and getattr(self, f.attname):
                self.has_location = True

        super(MongoFirstTowerbellPeal, self).save(*args, **kwargs)
