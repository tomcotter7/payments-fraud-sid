from ..create_types_iso_msgs import msgPAIN001, msgPACS002, msgPACS008
from datetime import datetime

pain_01_data = {"ID": "PAIN1-01",
                "DATETIME": datetime(year=2022, month=5, day=1, hour=12, minute=30, second=15),
                "DBTR_ID": 1, "CDTR_ID": 2, "DBTR_NM": "Test Debtor Name", "CDTR_NM": "Test Creditor Name", "AMT": 120,
                "DBTR_ACC": "DBTR_IBAN", "CDTR_ACC": "CDTR_IBAN", "TX_ID": 1, "CURRENCY": "SAR"}

pacs_08_data = {"ID": "PACS8-01",
                "DATETIME": datetime(year=2022, month=5, day=1, hour=12, minute=30, second=16),
                "DBTR_ID": 1, "CDTR_ID": 2, "DBTR_NM": "Test Debtor Name", "CDTR_NM": "Test Creditor Name",
                "AMT": 120, "DBTR_ACC": "DBTR_IBAN", "CDTR_ACC": "CDTR_IBAN", "TX_ID": 1, "CURRENCY": "SAR"}


pacs_02_data = {"ID": "PACS2-01",
                "DATETIME": datetime(year=2022, month=5, day=1, hour=12, minute=30, second=17),
                "TX_STS": "SUCCESSFUL",
                "PACS_008_ID": "PACS8-01",
                "TX_ID": 1}

class Test_msgPAIN001:
    def setup(self):
        self.painmsg = msgPAIN001(pain_01_data)
        self.painmsg.serialize()

    def test_datetime_is_string(self):
        assert isinstance(self.painmsg.date_time, str)
    
    def test_amt_is_string(self):
        assert isinstance(self.painmsg.amount, str)
    
class Test_msgPACS002:
    def setup(self):
        self.pacs2msg = msgPACS002(pacs_02_data)
        self.pacs2msg.serialize()

    def test_datetime_is_string(self):
        assert isinstance(self.pacs2msg.date_time, str)
    
class Test_msgPACS008:
    def setup(self):
        self.pacs8msg = msgPACS008(pacs_08_data)
        self.pacs8msg.serialize()

    def test_datetime_is_string(self):
        assert isinstance(self.pacs8msg.date_time, str)
    
    def test_amt_is_string(self):
        assert isinstance(self.pacs8msg.amount, str)


    
         



