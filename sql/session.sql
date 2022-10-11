-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Session Table
-- Serves as an Aggregate Table to record additonal details about a Session 
create or replace table SESSION (
  SessionId int not null unique comment 'Unique identifier for the payment',
  PartyIdentificationId int not null references CDT_TRF_TX_INF(DebtorId) comment 'The party involved in this payment ; the Debtor making the transfer',
  IPAdr varchar(50) not null comment 'IP Address associated with Debtor at time of making transfer',
  Device varchar(50) not null comment 'Type of Device used for making transaction - Mobile / Web',
  DefaultIPAdr varchar(50) not null comment 'Default IP Address of Debtor when transaction is usually made',
  SessionLength time(4) not null comment 'Time taken for each session',
  NbOfMsg int not null comment 'Number of Messages sent in a particular Session',
  NbOfTriesToLogin int not null comment 'Number of Tries made my Debtor to log in to account',
  SendTimeOfOTP time(4) not null comment 'Time at which Double Factor Authentication was sent for payment transfer request',
  EntryTimeOfOTP time(4) not null comment 'Time at which Double Factor Authentication was entered post send time',
  VersionOfApp float not null comment 'Version of Applicatio used',
  NbOfOTPEntries int not null comment 'Number of Double Factor Authentication Entries',
  PRIMARY KEY (SessionId),
  FOREIGN KEY (PartyIdentificationId) references CDT_TRF_TX_INF(DebtorId)
);
