from .create_types_message_flows import HappyFlow
from faker import Faker
from ....shared_utils.generic_utils import gen_datetime, generateFakeName
from ....shared_utils.Connectors.snowflake_connector import SnowflakeConnection
from .singleton import Singleton
import exrex
import pandas as pd
import numpy as np
from datetime import datetime
import threading


class MessageFlowFactory(metaclass=Singleton):
    
    def __init__(self, num_parties, db_config_file, flow_percentages={"HappyFlow": 1}, db="Snowflake", datetime_range=(2020, 2022)):
        """Function to initialise a MessageFlowFactory objects
        
        Args:
            |  num_parties (int): The number of parties you want to generate for this flow.
            |  db_config_file (String): The location of the config file for the database.
            |  flow_percentages (Dictionary): How many of the different types of flows.
            |  db (String): The database to connect to (defaults to Snowflake)

        """
        self.faker = Faker('ar_SA')
        self.parties = self.generate_n_parties(num_parties)
        self.flow_percentages = flow_percentages
        self.dt_range = datetime_range
        self.config = db_config_file
        self.hfs = []
        self.messages = []
        self.lock = threading.Lock()
        if db == "Snowflake":
            sc = SnowflakeConnection()
            sc.setCredentials(self.config)
            self.db_connection = sc

    def sort_function(self, x):
        """Function to use as the key for sorting an array of messages. We want to sort by datetime, and then message id.
        
        Args:
            | x (ISO20022msg): A single message.

        Returns:
            datetime: The create_date_time of the message
            String: The message id
        """
        try:
            return datetime.strptime(x.date_time, "%Y-%m-%d %H:%M:%S.%f"), x.id
        except ValueError:
            return datetime.strptime(x.date_time, "%Y-%m-%d %H:%M:%S"), x.id

    
    def generate_n_parties(self, n):
        """Function to generate N parties for use in the flows. The parties currently have 3 fields:
        ID, NAME & ACCOUNT. The account (IBAN) is generated using the Saudi Arabia format.
        
        Args:
            n (int): The number of parties

        Returns:
            DataFrame: Containing data about all the parties
        """
        parties = []
        for uid in range(n):
            name = generateFakeName(self.faker)
            iban = exrex.getone("SA\\d{2}[ ]\\d{4}[ ]\\d{4}[ ]\\d{4}[ ]\\d{4}[ ]\\d{4}[ ]\\d{4}|SA\\d{26}")
            parties.append([uid, name, iban])
        # I'm not sure whether it's possible to use 0..N as Dbtr/Cdtr_ID.
        # We might have to use a combination of the IBAN+Name to generate the ID.
        # For simplicity, I have just used 0..N.
        parties_df = pd.DataFrame(parties, columns=["ID", "NM", "ACC"])
        return parties_df
    
    def create_flows(self, num_flows, write_to_file=False):
        """Function to create "num_flows" flows. Here we would create all of our types of flows, HappyFlows, SadFlows etc..

        Args:
            | num_flows (int): The number of flows to generate
            | write_to_file (bool): Whether or not to write the generate flows to a .csv

        """
        uids = [x for x in range(num_flows + 1)]
        num_happy_flows = int(self.flow_percentages["HappyFlow"] * num_flows)
        happy_flow_uids = [uids.pop() for _ in range(num_happy_flows)]
        self.create_happy_flows(num_happy_flows, happy_flow_uids, write_to_file)
        with self.lock:
            self.messages.sort(key = lambda x: self.sort_function(x)) 

    def create_happy_flows(self, num_flows, uids, write_to_file=False):
        """
        Function to generate N happy flows (pain1, pacs8 & pacs2).

        Args:
            | num_flows (int): The number of flows to create
            | uids ([int]): A list of possible uids to use in the HappyFlows
            | write_to_file (bool): Whether or not to write the generate flows to a .csv
        """
        for uid in uids:
            hf = HappyFlow(uid, self.parties.sample(1),
                           self.parties.sample(1), self.dt_range)
            hf.generate_flow(write_to_file)
            with self.lock:
                self.hfs.append(hf)
                self.messages.append(hf.pain1)
                self.messages.append(hf.pacs8)
                self.messages.append(hf.pacs2)
    
    def writeToBlobStore(self, store="csv"):
        """Function to write all of the messages in xml format to a 'blob storage'. We have two options currently,
        write to csv and write to Snowflake

        Args:
            | store (String): The type of blob storage to write to ("csv" or "Snowflake")

        """

        xml_strings = np.array([msg.xml_string for msg in self.messages], dtype=object)
        if store == "csv":
            np.savetxt('lxa_platform/payments_fraud/sample_xml/blob.csv', xml_strings, delimiter=',', fmt="%s")
        elif store == "Snowflake":
            xmls = pd.DataFrame(xml_strings, columns=["XML_MESSAGE"])
            self.db_connection.toSQL(xmls, "blob_xml", ifExists="append")


        


    
    
        
            
