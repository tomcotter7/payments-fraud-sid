-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Regulatory Reporting Table
-- Serves as a Table to record details about Regulations applied on Payments
create or replace table REGULATORY_REPORTING (
  RgltryRptgId int not null unique comment 'The regulatory reporting id corresponding to a message with payments',
  DbtCdtRptgInd varchar(20) not null comment 'Type of Party - Debtor / Creditor or Both',
  Ctry varchar(50) not null comment 'Country of which Regulations apply',
  Dt date not null comment 'Date associated with regulation report',
  -- Inf varchar(120) comment 'Additional Info if any',
  Amt float not null comment 'Regulatory amount levied',
  PRIMARY KEY (RgltryRptgId)
);
