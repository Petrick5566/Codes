from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PropertyAmenity, Property, Amenity, Location
from django.contrib.auth.models import User

class PropertyAmenityViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.location = Location.objects.create(
            country='Country',
            region='Region',
            city='City',
            district='District',
            street='Street'
        )
        self.property = Property.objects.create(
            owner=self.user,
            title='Test Property',
            description='Test Description',
            location=self.location,
            property_type='LAND',
            price=1000,
            price_period='ONETIME',
            is_available=True
        )
        self.amenity = Amenity.objects.create(name='Test Amenity')
        self.property_amenity_data = {
            'property': self.property.id,
            'amenity': self.amenity.id,
            'notes': 'Test notes'
        }

    def test_create_property_amenity(self):
        response = self.client.post('/propertyamenities/', self.property_amenity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PropertyAmenity.objects.count(), 1)
        self.assertEqual(PropertyAmenity.objects.get().notes, 'Test notes')

    def test_list_property_amenities(self):
        PropertyAmenity.objects.create(**self.property_amenity_data)
        response = self.client.get('/propertyamenities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_property_amenity(self):
        pa = PropertyAmenity.objects.create(**self.property_amenity_data)
        response = self.client.get(f'/propertyamenities/{pa.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Test notes')

    def test_update_property_amenity(self):
        pa = PropertyAmenity.objects.create(**self.property_amenity_data)
        updated_data = {
            'property': self.property.id,
            'amenity': self.amenity.id,
            'notes': 'Updated notes'
        }
        response = self.client.put(f'/propertyamenities/{pa.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PropertyAmenity.objects.get().notes, 'Updated notes')

    def test_delete_property_amenity(self):
        pa = PropertyAmenity.objects.create(**self.property_amenity_data)
        response = self.client.delete(f'/propertyamenities/{pa.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PropertyAmenity.objects.count(), 0)
