from django.test import TestCase
from django.template.defaultfilters import slugify

from method.models import Method

# method = {
#     'name' : 
# }

class MethodCourseInternalTest(TestCase):

    def test_little_bob(self):

        places = '-1-4LH2'
        calls = 'e'

        # for nbells in [6, 8, 10, 12, 14, 16]:
        for nbells in [6]:

            name = 'Little Bob %d' % nbells
            slug = slugify(name)

            m = Method.objects.create(nbells=nbells, name=name, slug=slug, places=places, calls=calls)
            c = m._course_(m.nbells, m.places, name=slug)
            c.ring()

            self.assertTrue(c.n_lead_ends)


    def test_125th_anniversary_bob_doubles(self):

        places = '34.1.2.3.5.23.5.1.5.23'
        calls = 'z'
        nbells = 5
        name = '125th_anniversary_bob_doubles'
        slug = slugify(name)

        m = Method.objects.create(nbells=nbells, name=name, slug=slug, places=places, calls=calls)
        c = m._course_(m.nbells, m.places, name=slug)
        c.ring()

        self.assertTrue(c.n_lead_ends)

    def test_cambridge_surprise_maximus(self):

        places = '-3-4-25-36-47-58-69-70-8-9-0-ELH2'
        calls = 'b'
        nbells = 12
        name = 'Cambridge Surprise Maximus'
        slug = slugify(name)

        m = Method.objects.create(nbells=nbells, name=name, slug=slug, places=places, calls=calls)
        c = m._course_(m.nbells, m.places, name=slug)
        c.ring()

        self.assertTrue(c.n_lead_ends)

    def test_kent_treble_bob_maximus(self):

        places = '34-34.1-2-1-2-1-2-1-2-1-2-1LH1'
        calls = 'mx'
        nbells = 12
        name = 'Kent Treble Bob Maximus'
        slug = slugify(name)

        m = Method.objects.create(nbells=nbells, name=name, slug=slug, places=places, calls=calls)
        c = m._course_(m.nbells, m.places, name=slug)
        c.ring()

        self.assertTrue(c.n_lead_ends)

    def test_kent_treble_bob_fourteen(self):

        places = '34-34.1-2-1-2-1-2-1-2-1-2-1-2-1LH1'
        calls = 'mx'
        nbells = 14
        name = 'Kent Treble Bob Fourteen'
        slug = slugify(name)

        m = Method.objects.create(nbells=nbells, name=name, slug=slug, places=places, calls=calls)
        c = m._course_(m.nbells, m.places, name=slug)
        c.ring()

        self.assertTrue(c.n_lead_ends)

