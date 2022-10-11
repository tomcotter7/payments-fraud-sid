from ..message_flow_factory import MessageFlowFactory
import os
import threading
from datetime import datetime

class Test_MessageFlowFactory:

    def setup(self):
        self.nparties = 10
        self.mff = MessageFlowFactory(self.nparties, "lxa_platform/payments_fraud/scripts/configs/db_config.json")
    
    def test_number_parties_correct(self):
        assert self.mff.parties.shape[0] == self.nparties

    def test_create_happy_flows_correct_number(self):
        self.mff.create_flows(5)
        assert len(self.mff.hfs) == 5

    def test_create_happy_flows_percentage_flow(self):
        self.mff.hfs = []
        self.mff.messages = []
        self.mff.flow_percentages={"HappyFlow": 0.5}
        self.mff.create_flows(10)
        assert len(self.mff.hfs) == 5


    def test_create_happy_flows_write_to_file(self):
        self.mff.create_happy_flows(1, write_to_file=True)
        assert os.path.isfile("lxa_platform/payments_fraud/sample_xml/pain001PAIN1-0.xml") & os.path.isfile("lxa_platform/payments_fraud/sample_xml/pacs008PACS8-0.xml") & os.path.isfile("lxa_platform/payments_fraud/sample_xml/pacs002PACS2-0.xml")
    
    
    def test_msgs_written_to_blob_csv(self):
        self.mff.hfs = []
        self.mff.messages = []
        self.mff.create_flows(10)
        self.mff.writeToBlobStore()
        assert os.path.isfile('lxa_platform/payments_fraud/sample_xml/blob.csv')

    
    def test_messages_are_sorted(self):
        self.mff.flow_percentages = {"HappyFlow": 1}
        self.mff.messages = []
        self.mff.create_flows(2)
        assert datetime.strptime(self.mff.messages[0].date_time, "%Y-%m-%d %H:%M:%S.%f") < datetime.strptime(self.mff.messages[4].date_time, "%Y-%m-%d %H:%M:%S.%f")

    
    def create_mff_threads(self):
       new_mff = MessageFlowFactory(5, "lxa_platform/payments_fraud/scripts/configs/db_config.json")
       # basically checking that this flow factory is never created.
       self.nparties = new_mff.parties.shape[0]
       new_mff.create_flows(10)


    def test_object_is_thread_safe(self):
        # test that mff is thread safe.
        # how to do this?
        # first let's create an instance of a second object.
        self.mff.hfs = []
        self.mff.messages = []
        self.mff.flow_percentages = {"HappyFlow": 1}
        threads = [threading.Thread(target=self.create_mff_threads) for t in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert (self.nparties == 10) & (len(self.mff.hfs) == 1000)
        


    

