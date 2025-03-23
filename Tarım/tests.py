from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class ContactPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_page_status_code(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_template(self):
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'contact.html')
