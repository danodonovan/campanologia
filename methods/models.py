from django.db import models

class Methods( models.Model ):
    """ Simple method class - to hold all methods from that CSV file """

    order  = models.IntegerField( 'Number of bells' )
    name   = models.CharField(    'Name of the method', max_length=256 )
    places = models.CharField(    'Place notation',     max_length=256 )
    calls  = models.CharField(    'call type',          max_length=32  )

    def __unicode__(self):
        return u'%s method' % self.name

    def Meta():
        get_latest_by = 'name'
