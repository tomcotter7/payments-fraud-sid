from .iso_msg import ISO20022msg
import xml.etree.ElementTree as ET

class msgPAIN001(ISO20022msg):

    def __init__(self, input_data, xml=False, input_data_xml=""):
        if xml:
            super().__init__("pain001", "", xml=True, input_data_xml=input_data_xml)
        else:
            super().__init__("pain001", input_data)
            self.dbtr_id = str(input_data["DbtrId"])
            self.cdtr_id = str(input_data["CdtrId"])
            self.debtor_name = input_data['DbtrNm']
            self.creditor_name = input_data['CdtrNm']
            self.debtor_bank_account = input_data['DbtrAcct']
            self.creditor_bank_account = input_data['CdtrAcct']
            self.amount = str(input_data['Amt'])
            self.tx_id = input_data["CdtTfTxInfId"]
            self.ccy = input_data["Ccy"]

    def serialize(self):
        root = ET.Element("CstmrCdtTrfInitn")
        grp_hdr = ET.SubElement(root, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = self.id
        ET.SubElement(grp_hdr, "CreDtTm").text = self.date_time
        pmt_inf = ET.SubElement(root, "PmtInf")
        ET.SubElement(pmt_inf, "CdtTfTxInfId").text = self.tx_id
        dbtr = ET.SubElement(pmt_inf, "Dbtr")
        dbtr.text = self.dbtr_id
        ET.SubElement(dbtr, "Nm").text = self.debtor_name
        ET.SubElement(dbtr, "Acct").text = self.debtor_bank_account
        cdtr = ET.SubElement(pmt_inf, "Cdtr")
        cdtr.text = self.cdtr_id
        ET.SubElement(cdtr, "Nm").text = self.creditor_name
        ET.SubElement(cdtr, "Acct").text = self.creditor_bank_account
        ET.SubElement(pmt_inf, "Amt").text = self.amount
        ET.SubElement(pmt_inf, "Ccy").text = self.ccy
        self.doc = ET.ElementTree(root)

class msgPACS008(ISO20022msg):

    def __init__(self, input_data, xml=False, input_data_xml=""):
        if xml:
            super().__init__("pacs008", "", xml=True, input_data_xml=input_data_xml)
        else:
            super().__init__("pacs008", input_data)
            self.dbtr_id = str(input_data["DbtrId"])
            self.cdtr_id = str(input_data["CdtrId"])
            self.debtor_name = input_data['DbtrNm']
            self.creditor_name = input_data['CdtrNm']
            self.debtor_bank_account = input_data['DbtrAcct']
            self.creditor_bank_account = input_data['CdtrAcct']
            self.amount = str(input_data['Amt'])
            self.tx_id = input_data["CdtTfTxInfId"]
            self.ccy = input_data["Ccy"]

    def serialize(self):
        root = ET.Element("FIToFICstmrCdtTr")
        grp_hdr = ET.SubElement(root, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = self.id
        ET.SubElement(grp_hdr, "CreDtTm").text = self.date_time
        crd_tf_tx_inf = ET.SubElement(root, "CdtTfTxInf")
        ET.SubElement(crd_tf_tx_inf, "CdtTfTxInfId").text = self.tx_id
        dbtr = ET.SubElement(crd_tf_tx_inf, "Dbtr")
        dbtr.text = self.dbtr_id
        ET.SubElement(dbtr, "Nm").text = self.debtor_name
        ET.SubElement(dbtr, "Acct").text = self.debtor_bank_account
        cdtr = ET.SubElement(crd_tf_tx_inf, "Cdtr")
        cdtr.text = self.cdtr_id
        ET.SubElement(cdtr, "Nm").text = self.creditor_name 
        ET.SubElement(cdtr, "Acct").text = self.creditor_bank_account
        ET.SubElement(crd_tf_tx_inf, "Amt").text = self.amount
        ET.SubElement(crd_tf_tx_inf, "Ccy").text = self.ccy
        self.doc = ET.ElementTree(root)


class msgPACS002(ISO20022msg):

    def __init__(self, input_data, xml=False, input_data_xml=""):
        if xml:
            super().__init__("pacs002", "", xml=True, input_data_xml=input_data_xml)
        else:
            super().__init__("pacs002", input_data)
            self.og_msg_id = input_data["OrgnlMsgId"]
            self.tx_sts = input_data["TxSts"]

    

    def serialize(self):
        root = ET.Element("FIToFIPmtStsRpt")
        grp_hdr = ET.SubElement(root, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = self.id
        ET.SubElement(grp_hdr, "CreDtTm").text = self.date_time
        tx_inf_and_sts = ET.SubElement(root, "TxInfAndSts")
        ET.SubElement(tx_inf_and_sts, "OrgnlMsgId").text = self.og_msg_id
        ET.SubElement(tx_inf_and_sts, "TxSts").text = self.tx_sts
        self.doc = ET.ElementTree(root)


        
