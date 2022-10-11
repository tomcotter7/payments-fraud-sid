-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Party Identification Table
-- Serves as a Table to record details about Party Involved
create or replace table PARTY_IDENTIFICATION (
  PartyIdentificationId text not null unique comment 'The parties involved making and receiving this payment',
  Nm varchar(50) not null comment 'The corresponding name of the party',
  AddressId int references ADDRESS(AddressId) comment 'Unique identifier for party address',
  FinInstnId int references FINANCIAL_INSTITUTION_IDENTIFICATION(FinInstnId) comment 'Unique identifier for Financial Instituion of party',
  BirthDt date comment 'Birth Date of Party',
  CityOfBirth varchar(20) comment 'City of Birth of party',
  CtryOfBirth varchar(40) comment 'Country Of Birth of party',
  PhneNb varchar(15) comment 'Phone number associated with party',
  MobNb varchar(15) comment 'Mobile number associated with party',
  EmailAdr varchar(70) comment 'Email Address of party',
  JobTitl varchar(50) comment 'Job Title of party',
  PrefrdMtd varchar(25) comment 'Preferred method of contact for party',
  TaxTp text comment 'The tax type of the party',
  TaxId text comment 'The tax Id of the party',
  -- IndustryOfWork varchar(50) not null comment 'Industry of work for party',
  -- Gender varchar(15) not null comment 'Gender of Party',
  -- CdtScore float not null comment 'Credit Score of Party',
  PRIMARY KEY (PartyIdentificationId),
  FOREIGN KEY (AddressId) references ADDRESS(AddressId),
  FOREIGN KEY (FinInstnId) references FINANCIAL_INSTITUTION_IDENTIFICATION(FinInstnId)
);
