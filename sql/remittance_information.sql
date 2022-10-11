-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Remmitance Information Table
-- Serves as a Table to record details about Remittance
create or replace table REMITTANCE_INFORMATION (
  RmtInfId int not null unique comment 'The remmitance id for remitter involved in payment',
  AddressId int not null references ADDRESS(AddressId) comment 'Unique identifier for party address',
  Strd boolean not null comment 'If message to remitter is structured',
  RfrdDocAmt float not null comment 'Referred amount in Document',
  RltdDt  date not null comment 'Date on Referred Document',
  Nb int not null comment 'Number of Remmited payments',
  Cd varchar(50) not null comment 'Remittance Code for a specific Remittance Information',
  RmtdAmt float not null comment 'Amount which has been remitted',
  DuePyblAmt float not null comment 'Amount which is due to be paid',
  PRIMARY KEY (RmtInfId),
  FOREIGN KEY (AddressId) references ADDRESS(AddressId)
);
