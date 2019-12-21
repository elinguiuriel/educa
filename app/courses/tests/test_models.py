from django.test import TestCase
from ..models import Subject, Course, Module
from django.db.utils import DataError
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_subject_successful(self):
        """Test the sucessuful creation of a subject"""

        title = "This is just a title"
        subject = Subject()
        subject.title = title
        subject.save()

        self.assertEqual(subject.title, title)
        self.assertIsNotNone(subject.slug)

    def test_subject_title_length_lt_200(self):
        """Test that the suject length cannot be more than 200 characters"""

        title = """This is a very long subject with more that 200 characters, to
        test that we cannot add more than 200 character in a subject, bla bla 
        bla bla bla bla  bla bla  bla bla  bla bla  bla bla  bla bla  bla bla
        """

        subject = Subject()
        subject.title = title
        
        with self.assertRaisesMessage(DataError, 
            'value too long for type character varying(200)'):
            subject.save()

    def test_module_ordering_successful(self):
        """Test that created module will be well ordered by subject"""

        user = get_user_model().objects.create_user(
            username='user',
            email='user@uriellabs.com',
            password='Testpass123'
        )

        subject = Subject()
        subject.title = 'Mathematics'
        subject.save()

        c1 = Course.objects.create(subject=subject, owner=user, 
            title='Course 1', slug='course1')
        c2 = Course.objects.create(subject=subject, 
            title='Course 2', slug='course2', owner=user)

        # module of course 1
        m1 = Module.objects.create(course=c1, title='Module 1')
        m2 = Module.objects.create(course=c1, title='Module 2')
        m3 = Module.objects.create(course=c1, title='Module 3', order=5)
        m4 = Module.objects.create(course=c1, title='Module 4')
        # first module of course 2
        m5 = Module.objects.create(course=c2, title='Module 1')        

        self.assertEqual(m1.order, 0)
        self.assertEqual(m2.order, 1)
        self.assertEqual(m3.order, 5)
        self.assertEqual(m4.order, 6)
        self.assertEqual(m5.order, 0)
