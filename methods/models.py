import hashlib
import logging

from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify

from methods.notation import sanitise_cccbr_notation

logger = logging.getLogger('django_debug')


class MethodSet(models.Model):
    """
    MethodSet
    """

    notes = models.CharField('notes', max_length=255)
    slug = models.SlugField('slug', max_length=255)
    p_stage = models.IntegerField('properties->stage')
    p_lengthOfLead = models.IntegerField('properties->lengthOfLead')
    p_numberOfHunts = models.IntegerField('properties->numberOfHunts')
    p_huntBellPath = models.CharField('properties->huntBellPath', max_length=511)
    p_symmetry = models.CharField('properties->symmetry', max_length=31)
    uniq_hash = models.CharField('uniq_hash', max_length=57, unique=True)

    class Meta:
        ordering = ('p_stage', 'notes',)

    # convenience
    def get_nchanges(self):
        return (self.p_stage - self.p_numberOfHunts) * self.p_lengthOfLead

    # django functions
    def __str__(self):
        return '{nbells} bells: {notes}'.format(notes=self.notes, nbells=self.p_stage)

    def get_absolute_url(self):
        return reverse('methods:list_method_set', args=[self.slug, ])

    def get_unique_hash(self):
        class_vals = [self.notes, self.p_stage, self.p_lengthOfLead,
                      self.p_numberOfHunts, self.p_huntBellPath, self.p_symmetry]
        ustring = ''.join(['%s' % a for a in class_vals])
        return hashlib.sha224(ustring.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.notes)
        self.uniq_hash = self.get_unique_hash()
        super(MethodSet, self).save(*args, **kwargs)


class Method(models.Model):
    """
    Method
    """

    id = models.IntegerField('id', primary_key=True)
    method_set = models.ForeignKey(MethodSet, on_delete=models.CASCADE)

    title = models.CharField('title', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255)
    name = models.CharField('name', max_length=255)
    raw_notation = models.CharField('notation', max_length=1023)

    # these two produced from sanitise_cccbr_notation
    notation = models.CharField('notation', max_length=1023)
    leadHead = models.CharField('lead head', max_length=63, blank=True, default='')

    # possible nulls
    leadHeadCode = models.CharField('lead head code', max_length=31)
    classification = models.CharField('classification', max_length=255)
    method_notes = models.CharField('method notes', max_length=255)

    # have own children in xml
    falseness_groups = models.CharField('fchGroups', max_length=31)

    rw_reference = models.CharField('"Ringing World" reference', max_length=63)
    bn_reference = models.CharField('"The Bell News" reference', max_length=63)
    cb_reference = models.CharField('"Church Bells" reference', max_length=63)
    pmm_reference = models.CharField('Numerical index in the Plain Minor Methods collection', max_length=63)
    tdmm_reference = models.CharField('Numerical index in the Treble Dodging Minor Methods collection', max_length=63)

    # performances
    first_hb_peal = models.OneToOneField('FirstHandbellPeal', related_name='firstHandBellPeak', null=True, on_delete=models.CASCADE)
    first_tb_peal = models.OneToOneField('FirstTowerbellPeal', related_name='firstTowerBellPeak', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)

    # convenience
    def get_js_notation(self):
        return ''.join(self.notation)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.notation, self.leadHead = sanitise_cccbr_notation(self.raw_notation)
        super(Method, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('methods:single_method', args=[self.slug, ])

    def __str__(self):
        return self.title


class Performance(models.Model):
    """
    Performance - not well sanitised
    """
    date = models.DateField('date')
    building = models.CharField('town', max_length=31)
    town = models.CharField('town', max_length=31)
    county = models.CharField('county', max_length=31)
    region = models.CharField('region', max_length=31)
    country = models.CharField('country', max_length=31)
    address = models.CharField('address', max_length=31)
    location = models.CharField('address', max_length=31)

    has_location = models.BooleanField('has_location', default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for f in self._meta.fields:
            if not isinstance(f, models.DateField) and getattr(self, f.attname):
                self.has_location = True

        super(Performance, self).save(*args, **kwargs)


class FirstHandbellPeal(Performance):
    pass


class FirstTowerbellPeal(Performance):
    pass

