-- Author: Sidharth Krishnan

-- Agent Table
-- Serves as the table that holds details of the Agent / Bank involved in Transaction for Debtor and Creditor Party. 
create or replace table AGENT (
  AgtId int not null unique comment 'Identifier for the agent',
  AddressId int not null references ADDRESS(AddressId) comment 'Address of agent',
  FinInstnId int not null references FINANCIAL_INSTITUTION_IDENTIFICATION(FinInstnId) comment 'Financial institution of agent',
  BrnchId int not null comment 'Branch of agent',
  BICFI text not null comment 'BICFI of the agent',
  ClrSysMmbId text not null comment 'Clearing System Member ID',
  LEI text not null comment 'LEI of agent',
  PRIMARY KEY (AgtId),
  FOREIGN KEY (AddressId) references ADDRESS(AddressId),
  FOREIGN KEY (FinInstnId) references FINANCIAL_INSTITUTION_IDENTIFICATION(FinInstnId)
);
