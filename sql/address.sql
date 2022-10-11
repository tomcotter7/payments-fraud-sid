-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Address table
-- Serves as the table that holds details of the Address for Party and Institutions. 
create or replace table ADDRESS (
  AddressId int not null unique comment 'Unique identifier for address',
  City text not null comment 'City of Address',
  StrtNm text not null comment 'Name of Street',
  BldgNm text not null comment 'Building number',
  PstCd text not null comment 'Post code',
  Ctry text not null comment 'Country',
  AdrTp text not null comment 'Type of address (Delivery, Mail, Rental)',
  PRIMARY KEY (AddressId)
);
