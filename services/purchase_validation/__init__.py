import datetime

from services.document_logic import BrazilianDocumentLogics


class PurchaseValidation(BrazilianDocumentLogics):
    def __init__(self, data):
        self.document = data["customer"]["document"]
        self.total = data["total"]
        self.products = data["products"]
        self.sold_at_data = data["sold_at"].replace(tzinfo=None)
        self.sold_at = datetime.datetime(self.sold_at_data.year, self.sold_at_data.day, self.sold_at_data.month, self.sold_at_data.hour, self.sold_at_data.minute, self.sold_at_data.second)

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
