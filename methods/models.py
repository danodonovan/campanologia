import logging
from django.db import models
from django.core.urlresolvers import reverse

from picklefield.fields import PickledObjectField

from course import Course

logger = logging.getLogger('django_debug')


class MethodsStatus(models.Model):
    """ Some information about when the method database was last updated etc. """
    updated = models.DateField(unique=True)
    num_methods = models.IntegerField()
    orders = models.ManyToManyField('MethodOrderCount')

    class Meta:
        ordering = ['updated']
        get_latest_by = 'updated'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Update %s' % self.updated


class MethodOrderCount(models.Model):
    """ Information about methods in database """
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

    order = models.PositiveIntegerField(choices=ORDER_CHOICES)
    count = models.IntegerField(null=True)
    updated = models.DateField()

    # get_order_display()

    class Meta:
        ordering = ['order']
        get_latest_by = 'updated'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%d' % self.order


class Method(models.Model):
    """
    Simple method class - to hold all methods from that CSV file
    """

    nbells = models.IntegerField('Number of bells', null=True)
    name = models.CharField('Name of the method', max_length=255)
    slug = models.SlugField(max_length=255)
    places = models.TextField('Place notation')
    calls = models.CharField('call type', max_length=8)
    nchanges = models.IntegerField('Number of changes (in a plain course)', null=True)
    nleadends = models.IntegerField('Number of lead ends (in a plain course)', null=True)

    problem = models.BooleanField('Is there a problem with this entry?')

    sanitised_notation = models.TextField('Sanitised Place notation')
    leadends = PickledObjectField('Leadends', null=True)
    changes = PickledObjectField('Changes', null=True)

    # @models.permalink
    def get_absolute_url(self):
        # return "%s" % self.slug
        # return reverse('methods.views.method_view', args=[self.slug,])
        # return ('methods.view.method_view', [str(self.slug)])
        return reverse('methods:single_method', args=[self.slug,])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

    def ring(self, save_changes=False):
        self.course = Course(self.nbells, self.places, self.name)
        self.course.ring()
        
        self.nleadends = self.course.nleadends
        self.sanitised_notation = self.course.notation
        self.nchanges = len(self.course.allChanges)

        if save_changes:
            self.changes = self.course.allChanges
            self.leadends = self.course.leadends
    
        self.save()





