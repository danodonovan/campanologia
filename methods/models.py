import logging
from django.db import models
from django.core.urlresolvers import reverse

from course import Course

logger = logging.getLogger('django_debug')

ORDER_CHOICES = (
    ( 4, 'Minimus'),
    ( 5, 'Doubles'),
    ( 6, 'Minor'),
    ( 7, 'Triples'),
    ( 8, 'Major'),
    ( 9, 'Caters'),
    (10, 'Royal'),
    (11, 'Cinques'),
    (12, 'Maximus'),
    (13, 'Sextuples'),
    (14, 'Fourteen'),
    (15, 'Septuples'),
    (16, 'Sixteen'),
)

#class MethodsStatus_old(models.Model):
#    """ Some information about when the method database was last updated etc. """
#    updated = models.DateField(unique=True)
#    num_methods = models.IntegerField()
#    orders = models.ManyToManyField('MethodOrderCount')
#
#    class Meta:
#        ordering = ['updated']
#        get_latest_by = 'updated'
#
#    def __str__(self):
#        return unicode(self).encode('utf-8')
#
#    def __unicode__(self):
#        return 'Update %s' % self.updated


#class MethodOrderCount_old(models.Model):
#    """ Information about methods in database """
#
#    order = models.PositiveIntegerField(choices=ORDER_CHOICES)
#    count = models.IntegerField(null=True)
#    updated = models.DateField()
#
#    def get_absolute_url(self):
#        return reverse('methods:order', args=[self.order,])
#
#    class Meta:
#        ordering = ['order']
#        get_latest_by = 'updated'
#
#    def __str__(self):
#        return unicode(self).encode('utf-8')
#
#    def __unicode__(self):
#        return '%d' % self.order


#class Method_old(models.Model):
#    """
#    Simple method class - to hold all methods from that CSV file
#    """
#
#    nbells = models.IntegerField('Number of bells', null=True)
#    name = models.CharField('Name of the method', max_length=255)
#    slug = models.SlugField(max_length=255)
#    places = models.TextField('Place notation')
#    calls = models.CharField('call type', max_length=8)
#    nchanges = models.IntegerField('Number of changes (in a plain course)', null=True)
#    nleadends = models.IntegerField('Number of lead ends (in a plain course)', null=True)
#
#    problem = models.BooleanField('Is there a problem with this entry?')
#
#    sanitised_notation = models.TextField('Sanitised Place notation')
#    leadends = PickledObjectField('Leadends', null=True)
#    changes = PickledObjectField('Changes', null=True)


class MethodSet(models.Model):
    """
    MethodSet
    """

    notes = models.CharField('notes', max_length=255)

    p_stage = models.IntegerField('properties->stage')
    p_lengthOfLead = models.IntegerField('properties->lengthOfLead')
    p_numberOfHunts = models.IntegerField('properties->numberOfHunts')
    p_huntBellPath = models.CharField('properties->huntBellPath', max_length=255)
    p_symmetry = models.CharField('properties->symmetry', max_length=255)

class Method(models.Model):
    """
    Method
    """

    id = models.IntegerField('id', primary_key=True)
    method_set = models.ForeignKey(MethodSet)

    title = models.CharField('title', max_length=255, unique=True)
    slug = models.SlugField('slug', max_length=255)
    name = models.CharField('name', max_length=255)
    notation = models.CharField('notation', max_length=255)

    # possible nulls
    leadHeadCode = models.CharField('lead head code', max_length=16)
    classification = models.CharField('classification', max_length=255)
    method_notes = models.CharField('method notes', max_length=255)

    # have own children in xml
    falseness_groups = models.CharField('fchGroups', max_length=31)

    rw_reference = models.CharField('"Ringing World" reference', max_length=31)
    bn_reference = models.CharField('"The Bell News" reference', max_length=31)
    cb_reference = models.CharField('"Church Bells" reference', max_length=31)
    pmm_reference = models.CharField('Numerical index in the Plain Minor Methods collection', max_length=31)
    tdmm_reference = models.CharField('Numerical index in the Treble Dodging Minor Methods collection', max_length=31)

    # performances
    first_hb_peal = models.OneToOneField('FirstHandbellPeal', related_name='first hand bell peak', null=True)
    first_tb_peal = models.OneToOneField('FirstTowerbellPeal', related_name='first tower bell peak', null=True)

    def get_absolute_url(self):
        return reverse('methods:single_method', args=[self.slug,])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

#    def ring(self, save_changes=False):
#        self.course = Course(self.nbells, self.places, self.name)
#        self.course.ring()
#
#        self.nleadends = self.course.nleadends
#        self.sanitised_notation = self.course.notation
#        self.nchanges = len(self.course.allChanges)
#
#        if save_changes:
#            self.changes = self.course.allChanges
#            self.leadends = self.course.leadends
#
#        self.save()



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

    class Meta:
        abstract = True

class FirstHandbellPeal(Performance):
    pass

class FirstTowerbellPeal(Performance):
    pass

