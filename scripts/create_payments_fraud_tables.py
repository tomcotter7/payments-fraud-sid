# A script to generate all the tables within Snowflake.

from ...shared_utils.Schema_Generators.create_tables import generate_tables
from ...shared_utils.Connectors.snowflake_connector import SnowflakeConnection

def create_payment_tables():
    """Function to create all the tables in the payments fraud data model"""
    sc = SnowflakeConnection()
    sc.setCredentials('lxa_platform/payments_fraud/scripts/configs/db_config.json')
    generate_tables(sc, ['address', 'financial_institution_identification', 'party_identification', 'account', 'account_information', 'agent', 'remittance_information', 'regulatory_reporting', 'tax', 'record', 'cdt_trf_tx_inf', 'pacs_008', 'pacs_002', 'pain_001', 'blob_xml', 'chrgs_inf'], 'lxa_platform/payments_fraud/sql/')


if __name__ == "__main__":
    create_payment_tables()


