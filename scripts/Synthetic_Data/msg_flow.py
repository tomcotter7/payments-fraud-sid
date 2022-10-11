from abc import ABC, abstractmethod

class MessageFlow(ABC):

    def __init__(self, flowType):
        """Function to initialise any "MessageFlow" object.

        Args:
            | flowType (String): The type of message flow to initalise

        """
        self.flowType = flowType
    
    @abstractmethod
    def generate_flow(self, write=False):
        """Abstract function that when implemented will generate the flow for message object.

        Args:
            | write (bool): Whether to write to file or not.
        
        """
        pass

