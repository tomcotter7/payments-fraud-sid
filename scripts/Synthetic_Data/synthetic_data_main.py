from .message_flow_factory import MessageFlowFactory
from .message_flow_deserialization import MessageFlowDeserialization


def payments_synthetic_main():
    """Function to create a message flow factory and create N flows. These will then be deserialized into
    a our 3NF database"""
    NUM_PARTIES = 500
    # POPULATION_OF_SA_WITH_BANK_ACCOUNTS = 11983465
    NUM_FLOWS = 1000

    mff = MessageFlowFactory(NUM_PARTIES, "lxa_platform/payments_fraud/scripts/configs/db_config.json")
    mfd = MessageFlowDeserialization("lxa_platform/payments_fraud/scripts/configs/db_config.json")

    print("Creating")
    mff.create_flows(NUM_FLOWS)
    mff.writeToBlobStore(store="Snowflake")
    # mff.writeToBlobStore(store="Snowflake")
    messages = list(map(lambda x: x.xml_string, mff.messages))
    print("Flattening")
    mfd.flatten_multiple_msgs_and_write(messages, writeToDB=True)



if __name__ == "__main__":
    payments_synthetic_main()
