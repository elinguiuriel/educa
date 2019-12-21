from django.test import TestCase
from ..models import Subject, Course, Module
from django.db.utils import DataError


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
        
        with self.assertRaisesMessage(DataError, 'value too long for type character varying(200)'):
            subject.save()

