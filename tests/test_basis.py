import os
import unittest

from seldon import BasisClient


class TestSeldonBasis(unittest.TestCase):
    def setUp(self):
        user = os.getenv('SELDON_USER')
        password = os.getenv('SELDON_PASS')
        if None in {user, password}:
            raise Exception('Set SELDON_USER, SELDON_PASS env variables')
        self.client = BasisClient(user, password)

    def test_get_company_card(self):
        inn = '6663003127'
        org = self.client.get_company_card(inn=inn)
        self.assertIsInstance(org, dict, org)

        self.assertIn('status', org, org)
        self.assertIn('methodStatus', org['status'], org['status'])
        self.assertEqual('Success', org['status']['methodStatus'], org)

        self.assertIn('company_card', org, org)
        company = org['company_card']
        self.assertIsInstance(company, dict, company)
        self.assertIn('basic', company, company)
        self.assertIn('inn', company['basic'], company)
        self.assertEqual(inn, company['basic']['inn'], company)
