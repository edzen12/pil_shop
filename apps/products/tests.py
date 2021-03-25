from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.request import Request
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User

from .models import Product, ProductItem
from .serializers import *


class ProductTest(APITestCase):
    def setUp(self):
        product = Product.objects.create(name = 'Jeans', description = 'Long_stylish')
        product_item = ProductItem.objects.create(color = 'Blue', size = 40, quantity = 3, price = 1000, product = product) 
        user = User.objects.create(username = 'super', email = 'super@mail.ru')
        user.set_password('none')
        user.save()  
        self.client.login(username = 'super', password = 'none')


    def test_get_product_list(self):
        url = reverse('product-list')
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        product = Product.objects.first()
        url = product.get_absolute_url()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_get_product_item_detail(self):
        product_item = ProductItem.objects.first()
        url = product_item.get_absolute_url()
        responce = self.client.get(url)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

    def test_add_product_item_to_bookmark(self):
        product_item = ProductItem.objects.first()
        url = product_item.add_to_bookmark_url()
        responce = self.client.post(url)
        self.assertEqual(responce.status_code, status.HTTP_202_ACCEPTED)

    def test_remove_product_item_from_bookmark(self):
        product_item = ProductItem.objects.first()
        url = product_item.add_to_bookmark_url()
        responce = self.client.post(url)
        responce = self.client.post(url)
        self.assertEqual(responce.status_code, status.HTTP_202_ACCEPTED)




class ProductSerializerTest(APITestCase):
    def setUp(self):
        self.product_attributes = {
            'name': 'shirts',
            'description': 'summer shirts'
        }

        self.serialized_data = {
            'name': 'troussers',
            'description': 'summer troussers'
        }

        self.product = Product.objects.create(**self.product_attributes)
        self.serializer = ProductCreateSerializer(instance=self.product)
        
    
    def test_includes_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['name', 'description']))

    
    def test_content_of_inputs(self):
        data = self.serializer.data
        self.assertEqual(data['name'], str(self.product_attributes['name']))


    def test_new_product(self):
        self.serialized_data['name'] = "skirts"

        serializer = ProductCreateSerializer(data=self.serialized_data)

        self.assertTrue(serializer.is_valid())



class ProductItemSerializerTest(APITestCase):
    def setUp(self):
        product = Product.objects.create(name = 'Jeans', description = 'Long_stylish')
        
        factory = APIRequestFactory()
        request = factory.get(f'{product.get_absolute_url}/items/')

        self.product_item_attributes = {'color': 'Blue', 'size': 40, 'quantity': 3, 'price': 1000}
        self.product_item = ProductItem.objects.create(product = product, **self.product_item_attributes) 

        serializer_context = {
            'request': Request(request),
        }
        self.serializer = ProductItemSerializer(instance=self.product_item, context=serializer_context)

    
    def test_fields_identity(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['url', 'color', 'size', 'quantity', 'price', 'product', 'product_item_images']))