import uuid
from unittest import TestCase

from ipay.b2c import B2C
from ipay.tests import IPAY_SECURITY_KEY, IPAY_VENDOR_ID


class B2CTest(TestCase):
    def setUp(self) -> None:
        self.b2c = B2C(IPAY_SECURITY_KEY, IPAY_VENDOR_ID)
        self.amount = 100

    def test_send_to_mpesa(self):
        transaction_id = uuid.uuid4().hex
        phone_number = '+254797792447'
        response = self.b2c.send_to_mpesa(transaction_id, phone_number, self.amount)
        print(response)
        # self.assertEqual(response.get('status'), 200, "Sending Not Successful")
