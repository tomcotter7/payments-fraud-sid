from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

class ISO20022msg(ABC):

    def __init__(self, messageType, input_data, xml=False, input_data_xml=""):
        """
        __init__ function for a ISO2002msg.

        Args:
            |  messageType (String): The type of input message, e.g pain001, etc...
            |  input_data (Python Dictionary): Contains the data to populate this message with
            |  xml (bool): Whether to directly create the ElementTree from a xml file or not.
            |  input_data_xml (String): The input data in xml format - used if xml is True.
        """
        self.messageType = messageType
        if xml:
           self.doc = ET.fromstring(input_data_xml) 
        else:                
            self.id = str(input_data['MsgId'])
            self.date_time = input_data['CreDtTm']
            self.date_time = self.date_time.__str__()
        
    
    def writeXML(self):
        """"
        Function to write a xml document to an xml file. We can set this up at a later point to write to a database.
        This could be set up to write a single xml to blob storage.
        """
        self.doc.write("lxa_platform/payments_fraud/sample_xml/" + self.messageType + self.id + ".xml")
    
    def toString(self):
        """
        Function to convert the ElementTree stored in this object into a string.
        """
        self.xml_string = ET.tostring(self.doc.getroot(), encoding='unicode', method='xml')
    
    @abstractmethod
    def serialize(self):
        """
        Function to convert the field in a ISO20022 message into an XML/Tree structure.

        """
        pass
    


