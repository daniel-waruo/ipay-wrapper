import uuid
from unittest import TestCase

from ipay.b2b import B2B
from ipay.tests import IPAY_SECURITY_KEY, IPAY_VENDOR_ID


class B2BTest(TestCase):
    def setUp(self) -> None:
        assert IPAY_SECURITY_KEY
        self.b2b = B2B(IPAY_SECURITY_KEY, IPAY_VENDOR_ID)
        self.amount = 1000

    def test_send_to_till_number(self):
        transaction_id = uuid.uuid4().hex
        till_number = '4035503'
        response = self.b2b.send_to_tillnumber(transaction_id, till_number, self.amount)
        print(response)
        # self.assertEqual(response.get('status'), 200, "Sending Not Successfull")

    def test_send_to_paybill(self):
        transaction_id = uuid.uuid4().hex
        paybill_number = '522522'
        paybill_account = '1276805594'
        response = self.b2b.send_to_paybill(
            transaction_id=transaction_id,
            paybill_number=paybill_number,
            amount=self.amount,
            narration=paybill_account
        )
        print(response)
        # self.assertEqual(response.get('status'), 200, "Sending Not Successfull")
