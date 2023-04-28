from zeep import Client


class Users:
    PATH = 'http://api.payamak-panel.com/post/users.asmx?wsdl'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client(self.PATH)

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def add_payment(self, options):
        return self.client.service.AddPayment(**self.get_data(), **options)

    def add(self, options):
        return self.client.service.AddUser(**self.get_data(), **options)

    def add_complete(self, options):
        return self.client.service.AddUserComplete(**self.get_data(), **options)

    def add_with_location(self, options):
        return self.client.service.AddUserWithLocation(
            **self.get_data(), **options
        )

    def authenticate(self):
        return self.client.service.AuthenticateUser(**self.get_data())

    def change_credit(self, amount, description, targetUsername, GetTax):
        data = {
            'amount': amount,
            'description': description,
            'targetUsername': targetUsername,
            'GetTax': GetTax
        }
        return self.client.service.ChangeUserCredit(**self.get_data(), **data)

    def forgot_password(self, mobileNumber, emailAddress, targetUsername):
        data = {
            'mobileNumber': mobileNumber,
            'emailAddress': emailAddress,
            'targetUsername': targetUsername
        }
        return self.client.service.ForgotPassword(**self.get_data(), **data)

    def get_base_price(self, targetUsername):
        data = {
            'targetUsername': targetUsername
        }
        return self.client.service.GetUserBasePrice(**self.get_data(), **data)

    def remove(self, targetUsername):
        data = {
            'targetUsername': targetUsername
        }
        return self.client.service.RemoveUser(**self.get_data(), **data)

    def get_credit(self, targetUsername):
        data = {
            'targetUsername': targetUsername
        }
        return self.client.service.GetUserCredit(**self.get_data(), **data)

    def get_details(self, targetUsername):
        data = {
            'targetUsername': targetUsername
        }
        return self.client.service.GetUserDetails(**self.get_data(), **data)

    def get_numbers(self):
        return self.client.service.GetUserNumbers(**self.get_data())

    def get_provinces(self):
        return self.client.service.GetProvinces(**self.get_data())

    def get_cities(self, provinceId):
        data = {
            'provinceId': provinceId
        }
        return self.client.service.GetCities(**self.get_data(), **data)

    def get_expire_date(self):
        return self.client.service.GetExpireDate(**self.get_data())

    def get_transactions(self, targetUsername, creditType, dateFrom, dateTo, keyword):
        data = {
            'targetUsername': targetUsername,
            'creditType': creditType,
            'dateFrom': dateFrom,
            'dateTo': dateTo,
            'keyword': keyword
        }
        return self.client.service.GetUserTransactions(**self.get_data(), **data)

    def get(self):
        return self.client.service.GetUsers(**self.get_data())

    def has_filter(self, text):
        data = {
            'text': text
        }
        return self.client.service.HasFilter(**self.get_data(), **data)