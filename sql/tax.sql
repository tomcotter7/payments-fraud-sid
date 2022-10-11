-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Tax Table
-- Serves as a Table to record details about Tax Associated
create or replace table TAX (
  TaxId int not null unique comment 'Unique identifier for Tax applicable on Payment',
  CdtrTaxId int comment 'The tax id for the creditor - NI number in Uk?',
  CdtrTaxTp text comment 'The tax type of the creditor',
  DbtrTaxId int comment 'The tax id for the debtor',
  DbtrTaxTp text comment 'The tax type of the debtor',
  AdmstnZn text comment 'The administrative zone of where the tax is applicable',
  Mtd text comment 'Method of taxation',
  Ctgy varchar(50) not null comment 'Category Of Tax applicable',
  DbtrSts varchar(10) not null comment 'Status of Debitor',
  Prd date not null comment 'Period until which Tax is applicable',
  TtlTaxblBaseAmt float not null comment 'Total Taxable base amount',
  TTACcy text comment 'The currency the tax will be taken in',
  TtlTaxAmt float not null comment 'Total Taxable Amount',
  Dt date not null comment 'Date for when Tax is levied',
  PRIMARY KEY (TaxId)
);
