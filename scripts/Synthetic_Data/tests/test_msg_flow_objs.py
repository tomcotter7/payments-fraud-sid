from ..create_types_message_flows import HappyFlow
from faker import Faker
from datetime import datetime
import pandas as pd 

class Test_HappyFlow:
    def setup(self):
        cdtr = pd.DataFrame([[1, "Tom", "SAD2786EXAMPLE"]], columns=["ID", "NM", "ACC"])
        dbtr = pd.DataFrame([[2, "Luiza", "SAB5345EXAMPLE"]], columns=["ID", "NM", "ACC"])
        self.hf = HappyFlow(1, dbtr, cdtr, (2020, 2021))
        self.hf.generate_flow(write=False)

    def test_cre_dt_work(self):
        paindt = datetime.strptime(self.hf.pain1.date_time, '%Y-%m-%d %H:%M:%S.%f') 
        pacs8dt = datetime.strptime(self.hf.pacs8.date_time, '%Y-%m-%d %H:%M:%S.%f')
        pacs2dt = datetime.strptime(self.hf.pacs2.date_time, '%Y-%m-%d %H:%M:%S.%f') 
        assert paindt < pacs8dt < pacs2dt
    
    def test_pain_and_pacs_identical_db_nm(self):
        pain_db_nm = self.hf.pain1.debtor_name
        pacs8_db_nm = self.hf.pacs8.debtor_name
        assert pacs8_db_nm == pain_db_nm
    
    def test_identical_tx_ids(self):
        pain_txid = self.hf.pain1.tx_id
        pacs8_txid = self.hf.pacs8.tx_id
        assert pain_txid == pacs8_txid
    
    def test_amt_within_20000(self):
        assert int(self.hf.data['AMT']) < 20000
    
    def test_correctly_do_not_create_hf(self):
        cdtr = pd.DataFrame([[1, "Tom", "SAD2786EXAMPLE"]], columns=["ID", "NM", "ACC"])
        missing_dbtr = pd.DataFrame([[3, "SALKJR3EXAMPLE"]], columns=["ID", "ACC"])
        new_hf = HappyFlow(2, missing_dbtr, cdtr, (2020, 2021))
        assert not new_hf.data_avaliable

