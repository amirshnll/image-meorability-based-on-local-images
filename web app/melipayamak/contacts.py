from zeep import Client


class Contacts:
    PATH = "http://api.payamak-panel.com/post/contacts.asmx?wsdl"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client(self.PATH)

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def add_group(self, groupName, Descriptions, showToChilds):
        data = {
            'groupName': groupName,
            'Descriptions': Descriptions,
            'showToChilds': showToChilds
        }
        return self.client.service.AddGroup(**self.get_data(), **data)

    def add(self, options):
        return self.client.service.AddContact(**self.get_data(), **options)

    def check_mobile_exist(self, mobileNumber):
        data = {
            'mobileNumber': mobileNumber
        }
        return self.client.service.CheckMobileExistInContact(
            **self.get_data(), **data
        )

    def get(self, groupId, keyword, _from, count):
        data = {
            'groupId': groupId,
            'keyword': keyword,
            'from': _from,
            'count': count

        }
        return self.client.service.GetContacts(**self.get_data(), **data)

    def get_groups(self):
        return self.client.service.GetGroups(**self.get_data())

    def change(self, options):
        return self.client.service.ChangeContact(**self.get_data(), **options)

    def remove(self, mobilenumber):
        data = {
            'mobileNumber': mobilenumber
        }
        return self.client.service.RemoveContact(**self.get_data(), **data)

    def get_events(self, contactId):
        data = {
            'contactId': contactId
        }
        return self.client.service.GetContactEvents(**self.get_data(), **data)
