from .utils import send_request, get_hash, parse_data

B2B_ENDPOINT = 'https://apis.ipayafrica.com/b2b/v1/'


class B2B:
    def __init__(self, security_key, vendor_id):
        self.security_key = security_key
        self.vendor_id = vendor_id

    def send_to_paybill(self, transaction_id, paybill_number, amount: float, narration):
        """ send money to paybill account
        Arguments:
            transaction_id - unique id generated by the merchant to identify the transaction
            paybill_number - the paybill number where money will be sent
            narration -  a short description of where money wiil be sent or the account number
            amount -  the amount of money that will be sent to the
        """
        response = send_request(
            data=self.get_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                account=paybill_number,
                amount=amount,
                narration=narration
            ),
            url=self.get_url("mpesapaybill")
        )
        return response

    def send_to_tillnumber(self, transaction_id, till_number, amount: float):
        """ Send money to till number
        Arguments:
            transaction_id - a unique id generated by the merchant to identify the transaction
            till_number -  the till number where the money will be sent to
            amount - amount of money to be sent
        """
        response = send_request(
            data=self.get_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                account=till_number,
                amount=amount
            ),
            url=self.get_url("mpesatill")
        )
        return response

    def send_to_ipay(self, transaction_id, vendor_id, amount: float):
        """Send Money to ipay merchant
        Arguments:
            transaction_id - a unique id generated by the merchant to identify the transaction
            vendor_id - the vendor id of the ipay merchant
            amount - the amount of money to be charged for the money transfer
        """
        response = send_request(
            data=self.get_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                account=vendor_id,
                amount=amount
            ),
            url=self.get_url("ipay")
        )
        return response

    def get_url(self, channel, external=True):
        """ Get the url endpoint of the request
        Arguments:
            channel - either - mpesapaybill  mpesatill or ipay
            external - if set to true it means that money is being transfers within ipay
            if false money is transferred outside i-pay like mpesa.
        """
        available_channels = ["mpesapaybill", "mpesatill", "ipay"]
        if channel not in available_channels:
            raise Exception(f"Invalid Channel channel should be in {available_channels} ")
        if not external:
            return f"{B2B_ENDPOINT}internal/send/{channel}"
        return f"{B2B_ENDPOINT}external/send/{channel}"

    def get_parameters(self, vendor_id, transaction_id, account, amount, narration="", currency="KES"):
        param_dict = {
            "vid": vendor_id,
            "reference": transaction_id,
            "account": account,
            "amount": str(amount),
            "narration": narration,
            "curr": currency
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
            "reference": transaction_id,
        }
        # return with hashed key as required by the documentation
        parameters = {
            'hash': get_hash(parse_data(param_dict), self.security_key),
            **param_dict
        }
        response = send_request(
            data=parameters,
            url=f"{B2B_ENDPOINT}transaction/status"
        )
        return response
