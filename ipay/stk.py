from .utils import parse_data, send_request, get_hash

STK_ENDPOINT = 'https://apis.ipayafrica.com/payments/v2/transact/push/mpesa'

INITIATOR_REQUEST_ENDPOINT = 'https://apis.ipayafrica.com/payments/v2/transact'

TRANSACTION_QUERY_ENDPOINT = 'https://apis.ipayafrica.com/payments/v2/transaction/search'

IS_LIVE = False


class STK:
    def __init__(self, security_key, vendor_id):
        self.security_key = security_key
        self.vendor_id = vendor_id

    def call_initiator_request(self, transaction_id, phone_number, amount):
        """Initiator request for all c2b transactions
        Arguments:
            transaction_id - the transaction id generated by the merchant
            phone_number -  the phone number of the customer
            amount - amount of money requested by the customer
        """
        return send_request(
            data=self.get_initiator_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                amount=amount,
                phone_number=phone_number
            ),
            url=STK_ENDPOINT
        )

    def request_stk_push(self, transaction_id, phone_number, amount: float):
        """ Call an stk push to user
        Arguments:
            transaction_id - unique id generated by the merchant to identify the transaction
            phone_number - phone number of the customers wallet
            amount - amount of money to be sent to the customers wallet
        """
        initiator_response = self.call_initiator_request(
            transaction_id,
            phone_number,
            amount
        )
        sid = initiator_response.get("sid")
        response = send_request(
            data=self.get_stk_parameters(
                vendor_id=self.vendor_id,
                amount=amount,
                sid=sid,
                phone_number=phone_number
            ),
            url=STK_ENDPOINT
        )
        return response

    def get_initiator_parameters(self, vendor_id, transaction_id, phone_number, amount):
        param_dict = {
            "vid": vendor_id,
            "oid": transaction_id,
            "phone": phone_number,
            "amount": amount
        }
        param_dict = {k: v for k, v in param_dict.items() if bool(v)}
        parameters = {
            "hash": get_hash(parse_data(param_dict), self.security_key),
            **param_dict,
        }
        return parameters

    def get_stk_parameters(self, vendor_id, sid, phone_number, amount):
        param_dict = {
            "vid": vendor_id,
            "sid": sid,
            "amount": amount,
            "phone": phone_number
        }
        param_dict = {k: v for k, v in param_dict.items() if bool(v)}
        parameters = {
            "hash": get_hash(parse_data(param_dict), self.security_key),
            **param_dict,
        }
        return parameters

    def get_transaction_status(self, transaction_id):
        """ check transaction status status in case of no callback """
        param_dict = {
            "vid": self.vendor_id,
            "oid": transaction_id,
        }
        # return with hashed key as required by the documentation
        parameters = {
            'hash': get_hash(parse_data(param_dict), self.security_key),
            **param_dict
        }
        response = send_request(
            data=parameters,
            url=TRANSACTION_QUERY_ENDPOINT
        )
        return response
