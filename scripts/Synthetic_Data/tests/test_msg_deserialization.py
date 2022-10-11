from ..message_flow_deserialization import MessageFlowDeserialization
from ..create_types_iso_msgs import msgPACS008
from datetime import datetime

pacs_08_data = {"ID": "PACS8-01",
                "DATETIME": datetime(year=2022, month=5, day=1, hour=12, minute=30, second=16),
                "DBTR_ID": 1, "CDTR_ID": 2, "DBTR_NM": "Test Debtor Name", "CDTR_NM": "Test Creditor Name",
                "AMT": 120, "DBTR_ACC": "DBTR_IBAN", "CDTR_ACC": "CDTR_IBAN", "TX_ID": 1, "CURRENCY": "SAR"}

xml_string_pacs8 = "<FIToFICstmrCdtTr><GrpHdr><MsgId>2</MsgId><CreDtTm>2022-09-30 15:52:37.1223</CreDtTm></GrpHdr><CdtTfTxInf><Amt>430</Amt><Ccy>SAR</Ccy><CdtTfTxInfId>1</CdtTfTxInfId><Dbtr>1<Nm>David</Nm><Acct>SA213EXAMPLE</Acct></Dbtr><Cdtr>2<Nm>Tom</Nm><Acct>SA4324EXAMPLE</Acct></Cdtr></CdtTfTxInf></FIToFICstmrCdtTr>"
xml_string_pain1 = "<CstmrCdtTrfInitn><GrpHdr><MsgId>1</MsgId><CreDtTm>2022-06-17 06:14:35.677560</CreDtTm></GrpHdr><PmtInf><CdtTfTxInfId>1</CdtTfTxInfId><Dbtr>1<Nm>David</Nm><Acct>SA213EXAMPLE</Acct></Dbtr><Cdtr>2<Nm>Tom</Nm><Acct>SA4324EXAMPLE</Acct></Cdtr><Amt>430</Amt><Ccy>SAR</Ccy></PmtInf></CstmrCdtTrfInitn>"
xml_string_pacs2 = "<FIToFIPmtStsRpt><GrpHdr><MsgId>3</MsgId><CreDtTm>2022-10-13 03:00:32.968890</CreDtTm></GrpHdr><TxInfAndSts><OrgnlMsgId>2</OrgnlMsgId><TxSts>SUCCESSFUL</TxSts></TxInfAndSts></FIToFIPmtStsRpt>"



class Test_MessageFlowDeserialization():
    
    def setup(self):
        self.mfd = MessageFlowDeserialization("lxa_platform/payments_fraud/scripts/configs/db_config.json")
        self.pacs8 = msgPACS008(pacs_08_data)
        self.pacs8.serialize()

    def test_get_personal_info(self):
        person = self.pacs8.doc.getroot().find('./CdtTfTxInf/Dbtr')
        nm , acc = self.mfd.get_personal_info(person)
        assert (nm == "Test Debtor Name") & (acc == "DBTR_IBAN")

    def test_parse_grp_hdr(self):
        root = self.pacs8.doc.getroot()
        msgid, cre_dt_tm = self.mfd.parse_grp_hdr(root)
        assert (msgid == "PACS8-01") & (cre_dt_tm.second == 16)

    def test_parse_xml_string(self):
        msg_id, cre_dt_tm, cdt_tf_tx_inf_id, dbtr_id, cdtr_id, \
            amt, ccy, d_nm, d_acc, c_nm, c_acc = self.mfd.flatten_xml(xml_string_pacs8)
        assert (msg_id == '2') & (d_nm == "David")

    def test_correct_deserialization(self):
        msgs = [xml_string_pain1, xml_string_pacs8, xml_string_pacs2]
        pain1_df, pacs8_df, pacs2_df, account_df, party_df, cdt_tf_tx_df = self.mfd.flatten_multiple_msgs_and_write(msgs, writeToDB=False, rtrn=True)
        assert (pain1_df["MSGID"].values[0] == '1') & (pacs8_df["MSGID"].values[0] == '2') & (pacs2_df["MSGID"].values[0] == '3') \
                & (cdt_tf_tx_df["AMT"].values[0] == '430') & (cdt_tf_tx_df.shape[0] == 1) & (account_df.shape[0] == 2) & \
                (party_df.shape[0] == 2)

