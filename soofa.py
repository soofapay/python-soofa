import requests
import logging

from datetime import datetime

__all__ = ["Transaction", "Soofa"]

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)


class Transaction(object):
    def __init__(self, status, sender_currency, receiver_currency, tid, reference, sender, receiver,
                 receipt_no, timestamp, gross_amount, net_amount, transacted_via, is_money_in, **kwargs):
        self.sender = sender
        self.sender_currency = sender_currency
        self.status = status
        self.receiver_currency = receiver_currency
        self.tid = tid
        self.reference = reference
        self.receiver = receiver
        self.receipt_no = receipt_no
        self.timestamp = timestamp
        self.gross_amount = gross_amount
        self.net_amount = net_amount
        self.transacted_via = transacted_via
        self.is_money_in=is_money_in

    def json(self):
        return {
            "status": self.status,
            "sender_currency": self.sender_currency,
            "receiver_currency": self.receiver_currency,
            "tid": self.tid,
            "reference": self.reference,
            "receipt_no": self.receipt_no,
            "timestamp": self.timestamp,
            "gross_amount": self.gross_amount,
            "net_amount": self.net_amount,
            "transacted_via": self.transacted_via,
            "is_money_in": self.is_money_in,
            "sender": self.sender,
            "receiver": self.receiver
        }

    def get_time(self):
        return datetime.fromtimestamp(self.timestamp)


class Soofa(object):
    TRANSACTION_DOES_NOT_EXIST = 404
    PERMISSION_DENIED = 403
    SUCCESSFUL = 200


    def __init__(self, till_no, client_secret):
        self.till_no = till_no
        self.client_secret = client_secret
        self.transaction = None
        self.status = None

    def find(self, tid):
        url = f"http://api.soofapay.com/v1/transactions/{tid}/"
        r = requests.get(
            url, headers={
                "Authorization": f"Token {self.client_secret}",
                "X-TILL": self.till_no
        })
        self.status = r.status_code
        if self.status == self.SUCCESSFUL:
            data = r.json()
            self.transaction = Transaction(**data)
            return True,
        self.__raise403(self.status)
        if self.status == self.TRANSACTION_DOES_NOT_EXIST:
            logging.warning("The transaction {0} does not exist".format(tid))
        return False

    def __raise403(self, status_code):
        if status_code==403:
            raise PermissionError("Your are not allowed to perform this action. Please ensure you use your "
                              "correct till number and client_secret")

    def get_transaction(self):
        if self.transaction is None:
            raise UserWarning("A transaction is not available yet. Please ensure you call find method and verify "
                            "that one exists before proceeding")
        return self.transaction

    def get_balance(self):
        url = f"http://api.soofapay.com/v1/balance/"
        r = requests.get(
            url, headers={
                "Authorization": f"Token {self.client_secret}",
                "X-TILL": self.till_no
        })
        self.__raise403(r.status_code)
        return r.json()


