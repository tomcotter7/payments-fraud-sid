-- Author: Thomas Cotter

-- Account Information table
create or replace table ACCOUNT_INFORMATION (
  AccountId text not null references ACCOUNT(AccountId) comment 'The account id',
  PartyIdentificationId text not null references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'The owner of the account',
  JointPartyId text not null references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Identification for Joint Account',
  JointAccount boolean not null comment 'Whether account is joint account or not',
  Identification1 varchar(30) not null comment 'Party Identification document 1',
  Identification2 varchar(30) not null comment 'Party Identification documetn 2',
  DtOpened date not null comment 'Date of Account Opening',
  ActualBalance float not null comment 'Actual Balance in Account',
  LastTransactionDt date not null comment 'Date of Last Transaction from account',
  Defaulted boolean not null comment 'If account holder is defaulter',
  Default6Mths boolean not null comment 'If Defaulted in last 6 months',
  Default12Mths boolean not null comment 'If Defaulted in last 12 months',
  FOREIGN KEY (AccountId) references ACCOUNT(AccountId),
  FOREIGN KEY (PartyIdentificationId) references PARTY_IDENTIFICATION(PartyIdentificationId),
  FOREIGN KEY (JointPartyId) references PARTY_IDENTIFICATION(PartyIdentificationId)
);
