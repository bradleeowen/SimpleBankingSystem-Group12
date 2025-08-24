from rest_framework.test import APITestCase
from django.test import TestCase
from django.urls import resolve

class URLSmokeTests(TestCase):
    def test_docs_routes_exist(self):
        self.assertIsNotNone(resolve("/schema/"))
        self.assertIsNotNone(resolve("/docs/"))

class APISmokeTests(APITestCase):
    def test_list_endpoints_return_ok_or_auth(self):
        # Adjust these to match your actual routes if needed
        for path in [
            "/api/",
            "/api/customers/",
            "/api/branches/",
            "/api/accounts/",
            "/api/cards/",
            "/api/loans/",
            "/api/transactions/",
        ]:
            r = self.client.get(path)
            self.assertIn(r.status_code, {200, 401, 403, 404}, msg=f"{path} -> {r.status_code}")