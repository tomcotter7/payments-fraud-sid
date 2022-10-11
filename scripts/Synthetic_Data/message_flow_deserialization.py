from .create_types_iso_msgs import msgPAIN001, msgPACS002, msgPACS008
from ....shared_utils.Connectors.snowflake_connector import SnowflakeConnection
import pandas as pd
from datetime import datetime
from time import time
import xml.etree.ElementTree as ET

class MessageFlowDeserialization():

    def __init__(self, db_config_file, db="Snowflake"):
        """init function for MessageFlowDeserialization. Sets up a database connection.
        Currently only works with Snowflake.

        Args:
            |  db_config_file (String): The location of the config file for the database.
            |  db (String): The database to connect to (defaults to Snowflake).
        """
        self.config = db_config_file
        if db == "Snowflake":
            sc = SnowflakeConnection()
            sc.setCredentials(self.config)
            self.db_connection = sc

     
    def get_personal_info(self, person):
        """Function to parse a person from a message (Debtor, Creditor, Ultimate Creditor, etc..)
        
        Args:
            person (Element): The person to be parsed.

        Returns:
            | String: The persons name.
            | String: The persons bank account.
        """
        return person.find("Nm").text, person.find("Acct").text
    
    def parse_grp_hdr(self, msg):
        """Function to parse the group header of a message.

        Args:
            msg (Element): The root of a ElementTree
        
        Returns:
            |  String: The msg_id.
            |  String: The create_date_time of the message.

        """
        try:
            create_date_time = datetime.strptime(msg.find("./GrpHdr/CreDtTm").text, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            create_date_time = datetime.strptime(msg.find("./GrpHdr/CreDtTm").text, "%Y-%m-%d %H:%M:%S")

        return msg.find("./GrpHdr/MsgId").text, create_date_time
    
    def flatten_pain1(self, msg):
        """Function to flatten a pain1 message.
        
        Args:
            msg (Element): The root element of a populate pain1 message.

        Returns:
            |  String: The message id
            |  Datetime: The CreationDateTime of the message
            |  String: The transaction id associated with this message
            |  String: The id of the debtor
            |  String: The id of the creditor
            |  String: The amount in the transaction
            |  String: The currency of this transaction
            |  String: The name of the debtor
            |  String: The debtor's IBAN
            |  String: The name of the creditor
            |  String: The creditor's IBAN
        """

        msg_id, cre_dt_tm = self.parse_grp_hdr(msg)
        amt = msg.find("./PmtInf/Amt").text
        ccy = msg.find("./PmtInf/Ccy").text
        cdt_tf_tx_inf_id = msg.find("./PmtInf/CdtTfTxInfId").text
        dbtr = msg.find("./PmtInf/Dbtr")
        cdtr = msg.find("./PmtInf/Cdtr")
        dbtr_id = dbtr.text
        cdtr_id = cdtr.text
        d_nm, d_acc = self.get_personal_info(dbtr)
        c_nm, c_acc = self.get_personal_info(cdtr)

        return msg_id, cre_dt_tm, cdt_tf_tx_inf_id, dbtr_id, cdtr_id, amt, ccy, d_nm, d_acc, c_nm, c_acc





    def flatten_pacs8(self, msg):
        """Function to flatten a pacs8 message

        Args:
            msg (Element): A root element of a populated pacs8 message.

        Returns:
            |  String: The message id
            |  Datetime: The CreationDateTime of the message
            |  String: The transaction id associated with this message
            |  String: The id of the debtor
            |  String: The id of the creditor
            |  String: The amount in the transaction
            |  String: The currency of this transaction
            |  String: The name of the debtor
            |  String: The debtor's IBAN
            |  String: The name of the creditor
            |  String: The creditor's IBAN
        """
        amt = msg.find("./CdtTfTxInf/Amt").text
        ccy = msg.find("./CdtTfTxInf/Ccy").text
        msg_id, cre_dt_tm = self.parse_grp_hdr(msg)
        cdt_tf_tx_inf_id = msg.find("./CdtTfTxInf/CdtTfTxInfId").text
        dbtr = msg.find("./CdtTfTxInf/Dbtr")
        cdtr = msg.find("./CdtTfTxInf/Cdtr")
        dbtr_id = dbtr.text
        cdtr_id = cdtr.text
        d_nm, d_acc = self.get_personal_info(dbtr)
        c_nm, c_acc = self.get_personal_info(cdtr)

        return msg_id, cre_dt_tm, cdt_tf_tx_inf_id, dbtr_id, cdtr_id, amt, ccy, d_nm, d_acc, c_nm, c_acc




    def flatten_pacs2(self, msg):
        """Function to flatten a pacs2 message
 
        Args:
            msg (Element): A root element of a populated pacs2 message

        Returns:
            | String: The message id
            | Datetime: The CreationDateTime of the message
            | String: The original message id (pacs8 msg id)
            | String: The status of the transaction
        """
        msg_id, cre_dt_tm = self.parse_grp_hdr(msg)
        tx_inf_and_sts = msg.find("TxInfAndSts")
        orgnl_msg_id = msg.find("./TxInfAndSts/OrgnlMsgId").text
        tx_sts = msg.find("./TxInfAndSts/TxSts").text
 
        return msg_id, cre_dt_tm, orgnl_msg_id, tx_sts
         
    def flatten_xml(self, xml_string):
        """Function to flatten the xml message string.

        Args:
            xml_string: The xml string to read and flatten

        Returns:
            args: An arbitrary amount of data depending on the input message type.
        """
        msg = ET.fromstring(xml_string)
        
        if msg.tag == "FIToFIPmtStsRpt": 
            return self.flatten_pacs2(msg) 
        elif msg.tag == "FIToFICstmrCdtTr":
            return self.flatten_pacs8(msg)
        elif msg.tag == "CstmrCdtTrfInitn":
            return self.flatten_pain1(msg)       
    
 
    def flatten_multiple_msgs_and_write(self, msgs, writeToDB=True, rtrn=False):
        """Function to flatten multiple msgs and write them all at the end to a 3NF database.
        
        Args:
            |  msgs (Array): A list of msgs (as strings)
            |  writeToDB (bool): Whether or not to write to the DB (we don't want to during testing)
            |  rtrn (bool): Used during the testing of deserialization, ensures that the DataFrames are returned.
        """
        pain1_data = []
        pacs8_data = []
        pacs2_data = []
        party_data = set()
        account_data = set()
        cdt_tf_tx_inf_data = []
        start = time()
        for msg in msgs:
            msg = ET.fromstring(msg)
            if msg.tag == "FIToFIPmtStsRpt":
                pacs2_msg_id, pacs2_cre_dt_tm, orgnl_msg_id, tx_sts = self.flatten_pacs2(msg)

                pacs2_data.append([pacs2_msg_id, pacs2_cre_dt_tm, orgnl_msg_id, tx_sts])

            elif msg.tag == "FIToFICstmrCdtTr":
                pacs8_msg_id, pacs8_cre_dt_tm, cdt_tf_tx_inf_id, dbtr_id, \
                    cdtr_id, amt, ccy, d_nm, d_acc, c_nm, c_acc = self.flatten_pacs8(msg)

                pacs8_data.append([pacs8_msg_id, pacs8_cre_dt_tm, cdt_tf_tx_inf_id])
                cdt_tf_tx_inf_data.append([cdt_tf_tx_inf_id, dbtr_id, cdtr_id, amt, ccy])
                party_data.add((dbtr_id, d_nm))
                party_data.add((cdtr_id, c_nm))
                account_data.add((cdtr_id, c_acc, c_acc))
                account_data.add((dbtr_id, d_acc, d_acc))

            elif msg.tag == "CstmrCdtTrfInitn":
                pain1_msg_id, pain1_cre_dt_tm, cdt_tf_tx_inf_id, dbtr_id, \
                    cdtr_id, amt, ccy, d_nm, d_acc, c_nm, c_acc = self.flatten_pain1(msg)

                pain1_data.append([pain1_msg_id, pain1_cre_dt_tm, cdt_tf_tx_inf_id])
                cdt_tf_tx_inf_data.append([cdt_tf_tx_inf_id, dbtr_id, cdtr_id, amt, ccy])
                party_data.add((dbtr_id, d_nm))
                party_data.add((cdtr_id, c_nm))
                account_data.add((cdtr_id, c_acc, c_acc))
                account_data.add((dbtr_id, d_acc, d_acc))

            
            
        print("Time taken for flows to flatten: %f" % (time() - start))
        pain1_df = pd.DataFrame(pain1_data, columns=["MSGID", "CREDTTM", "CDTTRFTXINF_ID"])
        pacs2_df = pd.DataFrame(pacs2_data, columns=["MSGID", "CREDTTM", "ORGNLMSGID", "TXSTS"]) 
        pacs8_df = pd.DataFrame(pacs8_data, columns=["MSGID", "CREDTTM", "CDTTRFTXINF_ID"])
        account_df = pd.DataFrame(list(account_data), columns=["PARTYIDENTIFICATIONID", "ACCOUNTID", "IBAN"])
        party_df = pd.DataFrame(list(party_data), columns=["PARTYIDENTIFICATIONID", "NM"])
        cdt_trf_tx_df = pd.DataFrame(cdt_tf_tx_inf_data, columns=["CDTTRFTXINF_ID", "DBTRID", "CDTRID", "AMT", "CCY"])
        cdt_trf_tx_df.drop_duplicates(subset=["CDTTRFTXINF_ID"], inplace=True)

        
        # Write to DB
        if writeToDB:
            self.db_connection.toSQL(pain1_df, "pain_001", ifExists="append")
            self.db_connection.toSQL(pacs8_df, "pacs_008", ifExists="append") 
            self.db_connection.toSQL(pacs2_df, "pacs_002", ifExists="append")
            self.db_connection.toSQL(cdt_trf_tx_df, "cdt_trf_tx_inf", ifExists="append") 
            self.db_connection.toSQL(party_df, "party_identification", ifExists="append") 
            self.db_connection.toSQL(account_df, "account", ifExists="append")  
        
        if rtrn:
            return pain1_df, pacs8_df, pacs2_df, account_df, party_df, cdt_trf_tx_df
