-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Account Table
-- Serves as a Table to record details about Bank Account of Party
create or replace table ACCOUNT (
  AccountId text not null unique comment 'The parties involved making and receiving this payment',
  PartyIdentificationId text not null references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Party Identification ID',
  IBAN varchar(40) not null comment 'IBAN associated with account of party',
  Ccy varchar(10) comment 'Currency in which money is stored in Account',
  PRIMARY KEY (AccountId),
  FOREIGN KEY (PartyIdentificationId) references PARTY_IDENTIFICATION(PartyIdentificationId)
);
