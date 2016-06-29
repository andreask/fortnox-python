# coding=utf-8


class VoucherRow():
    def __init__(self, json_data = {}):
        self.account = json_data.get("Account", 0)
        self.cost_center = json_data.get("CostCenter", "")
        self.credit = json_data.get("Credit", 0)
        self.description = json_data.get("Description", "")
        self.debit = json_data.get("Debit", 0)
        self.project = json_data.get("Project", "")
        self.removed = json_data.get("Removed")
        self.transaction_information = json_data.get("TransactionInformation")

    def __str__(self):
        return "%s" % self.account if self.account else ""

    def __repr__(self):
        return "<VoucherRow: %s>" % self.__str__()

    def to_dict(self):
        return {
            "Debit": self.debit,
            "Account": self.account,
            "Credit": self.credit
        }