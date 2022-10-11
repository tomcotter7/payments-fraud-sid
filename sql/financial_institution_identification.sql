-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Financial Instituion Identification Table
-- Serves as the table that holds details of the Financial Institution of Party. 
create or replace table FINANCIAL_INSTITUTION_IDENTIFICATION (
  FinInstnId int not null unique comment 'Unique identifier for Financial Instituion',
  AddressId int not null references ADDRESS(AddressId) comment 'The address ID',
  Nm text not null comment 'Name of Financial Institution',
  ClrSysMmbId text not null comment 'Clearing System Member ID',
  ClrSysId text not null comment 'Clearing System ID',
  BICOrBEI text not null comment 'BIC or BEI of the financial institution',
  LEI text not null comment 'LEI of financial institution',
  PRIMARY KEY (FinInstnId),
  FOREIGN KEY (AddressId) references ADDRESS(AddressId)
);
