import datetime

import requests

from services.document_logic import BrazilianDocumentLogics

import environ


class PurchaseValidation(BrazilianDocumentLogics):
    def __init__(self, data: dict):
        self.document = data["customer"]["document"]
        self.total = data["total"]
        self.products = data["products"]
        self.sold_at_data = data["sold_at"].replace(tzinfo=None)
        self.sold_at = datetime.datetime(self.sold_at_data.year, self.sold_at_data.day, self.sold_at_data.month, self.sold_at_data.hour, self.sold_at_data.minute, self.sold_at_data.second)
        self.veriry_if_is_alright()

    has_error = False
    errors = []

    def is_valid_total(self) -> bool:
        total = 0
        for product in self.products:
            total += float(product["value"]) * product["qty"]

        print(float(self.total), float(total))

        return float(self.total) == total

    def is_valid_date(self) -> bool:
        now = datetime.datetime.now()

        days_diff = abs((now - self.sold_at).days)
        return days_diff <= 0

    def veriry_if_is_alright(self) -> None:
        errors = []

        if not self.is_valid_date():
            errors.append({"detail": "Invalid date to 'sold_at' field."})

        if not self.is_valid_total():
            errors.append({"detail": "Invalid value to 'total' field."})

        if not self.is_valid_document():
            errors.append({"detail": "Invalid value to 'document' field."})

        if len(errors) > 0:
            self.has_error = True
            self.errors = errors

    def get_cashback_value(self):
        if not self.has_error:
            total = float(self.total)

            cashback = 0

            if total < 50.0:
                return cashback

            if total >= 50.0:
                cashback = total * 0.05

            if total >= 100.0:
                cashback = total * 0.1

            if total >= 200.0:
                cashback = total * 0.15

            if cashback > 150:
                return 150

            return cashback

    def get_document_value(self):
        if not self.has_error:
            return self.document

    def send_cashback(self):
        env = environ.Env()
        environ.Env.read_env()

        data = {
            "url": env("MAISTODOS_CASHBACK"),
            "json": {
                "document": self.get_document_value(),
                "cashback": self.get_cashback_value()
            },
            "headers": {
                "Content-Type": "application/json"
            }
        }

        response = requests.post(**data).json()
        return response

