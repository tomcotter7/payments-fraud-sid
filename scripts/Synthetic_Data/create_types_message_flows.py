from .create_types_iso_msgs import msgPAIN001, msgPACS002, msgPACS008
from ....shared_utils.generic_utils import gen_datetime, generateFakeName
from .msg_flow import MessageFlow
from dateutil.relativedelta import relativedelta
import random
import exrex

class HappyFlow(MessageFlow):
    

    def __init__(self, flow_id, dbtr, cdtr, dt_range, ccy="SAR", interval_range=(1, 100000)):
        """
        __init__ function for HappyFlow. Takes an input "flowId" which is used to generate the msg ids, then generates each of the three messages for the flow.
Args:
            flow_id (int): The "flow id",
            dbtr (DataFrame): A dataframe relating to a specific debtor
            cdtr (DataFrame): A dataframe relating to a specific creditor
            dt_range (tuple): A tuple containing the start and end years for the 3 messages we want to generate
            ccy (String): The currency to be used in this transactional flow. Defaults to "SAR"
            interval_range (tuple): A tuple containing the smallest possible interval and the largest possible interval between two messages. Microseconds.
        """
        super().__init__("HappyFlow")
        self.ir = interval_range
        # Not sure on the need for this - was specified in the acceptance criteria in the user story.
        try:
            self.data = {"DbtrNm": dbtr["NM"].array[0], "CdtrNm": cdtr["NM"].array[0],
                         "Amt": str(random.randint(1,20000)),
                         "DbtrAcct": dbtr["ACC"].array[0], "CdtrAcct": cdtr["ACC"].array[0],
                         "DbtrId": dbtr["ID"].array[0], "CdtrId": cdtr["ID"].array[0],
                         "Ccy": ccy}
            self.data_avaliable = True
        except KeyError as e:
            print("Missing Data!")
            print(e)
            self.data_avaliable = False
            return None
            
        self.data["TxSts"] = "SUCCESSFUL"
        self.pain1_msg_id = "PAIN1-" + str(flow_id)
        self.pacs8_msg_id = "PACS8-" + str(flow_id)
        self.pacs2_msg_id = "PACS2-" + str(flow_id)
        self.data["CdtTfTxInfId"] = "TX-" + str(flow_id)
        self.init_cre_dt_tm = gen_datetime(min_year=dt_range[0], max_year=dt_range[1])
    

    def generate_flow(self, write=False):
        """
        Function to generate all 3 messages involved in a 'Happy Flow' - transfer accepted. If write == True then the
        Tree-like objects are written to a .xml file.
        
        Args:
            write (bool): Whether to write the objects to file or not. Defaults to False
        """
        if self.data_avaliable:
            pain1_data = self.data
            pacs8_data = self.data
            pacs2_data = {"OrgnlMsgId": self.pacs8_msg_id, "TxSts": self.data["TxSts"]}

            pain1_data["MsgId"] = self.pain1_msg_id
            pain1_data["CreDtTm"] = self.init_cre_dt_tm
            self.pain1 = msgPAIN001(pain1_data)
            self.pain1.serialize()
            self.pain1.toString()
            
            pacs8_data["MsgId"] = self.pacs8_msg_id
            pacs8_dt = self.init_cre_dt_tm + relativedelta(microseconds=random.randint(self.ir[0], self.ir[1]))
            pacs8_data["CreDtTm"] = pacs8_dt
            self.pacs8 = msgPACS008(pacs8_data)
            self.pacs8.serialize()
            self.pacs8.toString()
            

            pacs2_data["MsgId"] = self.pacs2_msg_id
            pacs2_dt = pacs8_dt + relativedelta(microseconds=random.randint(self.ir[0], self.ir[1]))
            pacs2_data["CreDtTm"] = pacs2_dt
            self.pacs2 = msgPACS002(pacs2_data)
            self.pacs2.serialize()
            self.pacs2.toString()

            if write:
                self.pain1.writeXML()
                self.pacs8.writeXML()
                self.pacs2.writeXML()
        else:
            print("Missing data in __init__")
            print("This function can not be executed.")
       



