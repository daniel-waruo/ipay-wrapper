from .utils import parse_data, send_request, get_hash

B2C_ENDPOINT = 'https://apis.ipayafrica.com/b2c/v3/'


class B2C:
    def __init__(self, security_key, vendor_id):
        self.security_key = security_key
        self.vendor_id = vendor_id

    def send_to_mpesa(self, transaction_id, phone_number, amount: float, ):
        """ send the money to mpesa mobile wallet"""
        return self.send_mobile_money(transaction_id, phone_number, amount, channel="mpesa")

    def send_to_airtelmoney(self, transaction_id, phone_number, amount: float, ):
        """ send money to airtel mobile wallet """
        return self.send_mobile_money(transaction_id, phone_number, amount, channel="airtelmoney")

    def send_to_elipa(self, transaction_id, phone_number, amount: float, ):
        """ send money to elipa mobile wallet """
        return self.send_mobile_money(transaction_id, phone_number, amount, channel="elipa")

    def send_mobile_money(self, transaction_id, phone_number: str, amount: float, channel: str):
        """ Send to the customers mobile wallets
        Arguments:
            transaction_id - unique id generated by the merchant to identify the transaction
            phone_number - phone number of the customers wallet
            amount - amount of money to be sent to the customers wallet
            channel - the mobile money wallet where the money will be sent it should be either "mpesa", "elipa", "airtelmoney"
        """
        if phone_number.startswith("+"):
            phone_number = phone_number[1:]
        response = send_request(
            data=self.get_mobile_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                amount=amount,
                phone_number=phone_number
            ),
            url=self.get_mobile_url(channel)
        )
        return response

    def get_mobile_url(self, channel):
        """ Get the url endpoint of the request
        Arguments:
            channel - either - "mpesa", "elipa", "airtelmoney"
        """
        available_channels = ["mpesa", "elipa", "airtelmoney"]
        if channel not in available_channels:
            raise Exception(f"Invalid Channel channel should be in {available_channels} ")
        return f"{B2C_ENDPOINT}mobile/{channel}"

    def get_mobile_parameters(self, vendor_id, transaction_id, phone_number, amount):
        param_dict = {
            "vid": vendor_id,
            "reference": transaction_id,
            "phone": phone_number,
            "amount": str(amount)
        }
        param_dict = {k: v for k, v in param_dict.items() if bool(v)}
        parameters = {
            "hash": get_hash(parse_data(param_dict), self.security_key),
            **param_dict,
        }
        return parameters

    def send_to_bank(self, transaction_id, narration, bank_code, bank_account, amount: float, sender_name):
        """ send the money from the ipay merchant account to the respective owner
        Arguments:
            transaction_id - unique identification of the transaction generated by the merchant
            narration -  a short description of the reason for the transaction
            bank_code - bank code as identified in the following link https://www.kba.co.ke/downloads/BankBranchesReport.pdf
            bank_account - all digits of the bank accounts number
            amount -  amount of money to be sent
            sender_name - names of the merchant sending the money
        """
        response = send_request(
            data=self.get_bank_parameters(
                vendor_id=self.vendor_id,
                transaction_id=transaction_id,
                narration=narration,
                bank_code=bank_code,
                bank_account=bank_account,
                amount=amount,
                sender_name=sender_name
            ),
            url=self.get_bank_url()
        )
        return response

    def get_bank_url(self):
        """ Get the url endpoint of the request to pesalink"""
        return f"{B2C_ENDPOINT}pesalink"

    def get_bank_parameters(self, vendor_id, transaction_id, narration, bank_code, bank_account, amount, sender_name):
        param_dict = {
            "vid": vendor_id,
            "reference": transaction_id,
            "sendernames": sender_name,
            "narration": narration,
            "amount": str(amount),
            "bankcode": bank_code,
            "bankaccount": bank_account
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
            url=f"{B2C_ENDPOINT}transaction/status"
        )
        return response
