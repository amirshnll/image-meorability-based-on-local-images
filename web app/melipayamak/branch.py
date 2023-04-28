from zeep import Client


class Branch:
    PATH = "http://api.payamak-panel.com/post/Actions.asmx?wsdl"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client(self.PATH)

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def get(self, owner):
        data = {
            'owner': owner
        }
        return self.client.service.GetBranchs(**self.get_data(), **data)

    def remove(self, branchId):
        data = {
            'branchId': branchId
        }
        return self.client.service.RemoveBranch(**self.get_data(), **data)

    def add(self, branchName, owner):
        data = {
            'branchName': branchName,
            'owner': owner
        }
        return self.client.service.AddBranch(**self.get_data(), **data)

    def add_number(self, mobileNumbers, branchId):
        data = {
            'mobileNumbers': mobileNumbers,
            'branchId': branchId
        }
        return self.client.service.AddNumber(**self.get_data(), **data)

    def send_bulk(self, _from, title, message, branch, DateToSend, requestCount, bulkType, rowFrom, rangeFrom, rangeTo):
        data = {
            'from': _from,
            'title': title,
            'message': message,
            'branch': branch,
            'DateToSend': DateToSend,
            'requestCount': requestCount,
            'bulkType': bulkType,
            'rowFrom': rowFrom,
            'rangeFrom': rangeFrom,
            'rangeTo': rangeTo
        }
        return self.client.service.AddBulk(**self.get_data(), **data)

    def sendBulk2(self, _from, title, message, branch, DateToSend, requestCount, bulkType, rowFrom, rangeFrom, rangeTo):
        data = {
            'from': _from,
            'title': title,
            'message': message,
            'branch': branch,
            'DateToSend': DateToSend,
            'requestCount': requestCount,
            'bulkType': bulkType,
            'rowFrom': rowFrom,
            'rangeFrom': rangeFrom,
            'rangeTo': rangeTo
        }
        return self.client.service.AddBulk2(**self.get_data(), **data)

    def get_bulk_count(self, branch, rangeFrom, rangeTo):
        data = {
            'branch': branch,
            'rangeFrom': rangeFrom,
            'rangeTo': rangeTo
        }
        return self.client.service.GetBulkCount(**self.get_data(), **data)

    def get_bulk_receptions(self, bulkId, fromRows):
        data = {
            'bulkId': bulkId,
            'fromRows': fromRows
        }
        return self.client.service.GetBulkReceptions(**self.get_data(), **data)

    def get_bulk_status(self, bulkId):
        data = {
            'bulkId': bulkId
        }
        return self.client.service.GetBulkStatus(**self.get_data(), **data)

    def get_today_sent(self):
        return self.client.service.GetTodaySent(**self.get_data())

    def get_total_sent(self):
        return self.client.service.GetTotalSent(**self.get_data())

    def remove_bulk(self, bulkId):
        data = {
            'bulkId': bulkId
        }
        return self.client.service.RemoveBulk(**self.get_data(), **data)

    def send_multiple_sms(self, to, _from, text, isflash, udh):
        data = {
            'to': to,
            'from': _from,
            'text': text,
            'isflash': isflash,
            'udh': udh
        }
        result = None
        return (
            self.client.service.SendMultipleSMS2(**self.get_data(), **data)
            if isinstance(_from, list)
            else self.client.service.SendMultipleSMS(**self.get_data(), **data)
        )

    def update_bulk_delivery(self, bulkId):
        data = {
            'bulkId': bulkId
        }
        return self.client.service.UpdateBulkDelivery(**self.get_data(), **data)
