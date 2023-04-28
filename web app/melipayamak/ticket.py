from zeep import Client


class Ticket:
    PATH = 'http://api.payamak-panel.com/post/Tickets.asmx?wsdl'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client(self.PATH)

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def add(self, title, content, aws=True):
        data = {
            'title': title,
            'content': content,
            'alertWithSms': aws
        }
        return self.client.service.AddTicket(**self.get_data(), **data)

    def get_received(self, ticketOwner, ticketType, keyword):
        data = {
            'ticketOwner': ticketOwner,
            'ticketType': ticketType,
            'keyword': keyword
        }
        return self.client.service.GetReceivedTickets(**self.get_data(), **data)

    def get_received_count(self, ticketType):
        data = {
            'ticketType': ticketType,
        }
        return self.client.service.GetReceivedTicketsCount(
            **self.get_data(), **data
        )

    def get_sent(self, ticketOwner, ticketType, keyword):
        data = {
            'ticketOwner': ticketOwner,
            'ticketType': ticketType,
            'keyword': keyword
        }
        return self.client.service.GetSentTickets(**self.get_data(), **data)

    def get_sent_count(self, ticketType):
        data = {
            'ticketType': ticketType,
        }
        return self.client.service.GetSentTicketsCount(**self.get_data(), **data)

    def response(self, ticketId, _type, content, alertWithSms=True):
        data = {
            'ticketId': ticketId,
            'type': _type,
            'content': content,
            'alertWithSms': alertWithSms
        }
        return self.client.service.ResponseTicket(**self.get_data(), **data)
