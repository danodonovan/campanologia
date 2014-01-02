import logging
import hashlib

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

logger = logging.getLogger('django_debug')


def sanitise_cccbr_notation(raw_notation):
    """
    Clean up CCCBR notation for JS plotter
        - provide method, return updated method (unsaved)
    """

    # check for lead head
    if raw_notation.count(',') == 1:
        rns = raw_notation.split(',')

        # we've got a symmetric method
        if len(rns[0]) > len(rns[-1]):
            nr, lh = rns

        # we've got a screwy odd bell method
        elif len(rns[0]) < len(rns[-1]):
            lh, nr = rns

    elif raw_notation.count(',') == 0:
        nr, lh = raw_notation, ''

    else:
        print 'more than one "," in %s : %s' % raw_notation
        raise Exception

    i = 0
    n_t, n = [], []
    n_t_reset = False

    # there are edge case problems for Orignal N and Cheeky Little Place Minimus
    if len(nr) == 1:
        # if we're dealing with original
        if nr[0] == '-':
            n.extend(['X', '1'])
            return n, lh

        # if we're dealing with original odd
        if nr[0] in ['3', '5', '7', '9', 'E', 'A', 'C']:
            n.extend(['X', '1'])
            return n, lh

        # if we're dealing with Cheeky Little Place
        elif nr[0] == '1':
            n.extend(['14', '12'])
            return n, lh

    while i < len(nr):
        if n_t_reset:
            n_t = []

        if nr[i] == '-' or nr[i] == '.':
            if n_t:
                n.append(''.join(n_t))
                n_t = []
            if nr[i] == '-':
                n.append('X')
            n_t_reset = True

        elif nr[i] in raw_notation:
            n_t.append(nr[i])
            n_t_reset = False

        else:
            n.append(''.join(n_t))
            n_t_reset = True

        i += 1

    if n_t:
        n.append(''.join(n_t))

    #return '%s' % n.__repr__(), lh
    return '%s' % n.__str__(), lh


class Method(models.Model):
    """
    Method
    """

    id = models.IntegerField('id', primary_key=True)

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
    first_hb_peal = models.ForeignKey('FirstHandbellPeal', related_name='first hand bell peak', null=True)
    first_tb_peal = models.ForeignKey('FirstTowerbellPeal', related_name='first tower bell peak', null=True)

    # method set values
    ms_notes = models.CharField('notes', max_length=255)
    ms_slug = models.SlugField('slug', max_length=255)
    ms_p_stage = models.IntegerField('properties->stage')
    ms_p_lengthOfLead = models.IntegerField('properties->lengthOfLead')
    ms_p_numberOfHunts = models.IntegerField('properties->numberOfHunts')
    ms_p_huntBellPath = models.CharField('properties->huntBellPath', max_length=511)
    ms_p_symmetry = models.CharField('properties->symmetry', max_length=31)

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
        super(Method, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('methods:single_method', args=[self.slug, ])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.title


class Performance(models.Model):
    """
    Performance - not well sanitised
    """
    date = models.DateField('date')
    building = models.CharField('building', max_length=31)
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

