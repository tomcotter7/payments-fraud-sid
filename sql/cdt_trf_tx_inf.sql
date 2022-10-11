-- Author: Thomas Cotter
-- LXA: Payments Fraud Data Model

-- Credit Transfer Transaction Instruction table
-- Serves as the table that holds details of the transaction. 
-- Analogous to Payment Instruction table that is a sub-child of Credit Transfer Transaction per the Pain001
-- Credit Transfer Transaction is made use of in the Pacs008

create or replace table CDT_TRF_TX_INF (
  CdtTrfTxInf_Id text not null unique comment 'Individual Transaction Id for Credit Transfer',
  InstrPrty text comment 'Instruction Priority',
  CtgyPurp text comment 'Category Purpose',
  IntrBkSttlmAmt float comment 'Interbank settlement amount',
  SttlmPrty text comment 'Settlement priority',
  InstdAmt float comment 'Instructed amount',
  XchgRate float comment 'Exchange rate',
  InstgAgt int references AGENT(AgtId) comment 'Instructing agent',
  InstdAgt int references AGENT(AgtId) comment 'Instructed agent',
  IntrmyAgt int references AGENT(AgtId) comment 'Intermediary agent',
  DbtrId text references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Debtor Id',
  UltmtDbtrId text references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Ultimate Debtor Id',
  DbtrAgt int references AGENT(AgtId) comment 'Debtor Agent',
  CdtrAgt int references AGENT(AgtId) comment 'Creditor Agent',
  CdtrId text references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Creditor Id',
  UltmtCdtrId text references PARTY_IDENTIFICATION(PartyIdentificationId) comment 'Ultimate Creditor Id',
  Purp text comment 'Purpose',
  RgltryRptgId int references REGULATORY_REPORTING(RgltryRptgId) comment 'Regulartory Reporting Id',
  RmtInfId int references REMITTANCE_INFORMATION(RmtInfId) comment 'Remmitance Information Id',
  TaxId int references TAX(TaxId) comment 'Tax Id',
  Amt float comment 'Amount of transaction',
  Ccy text comment 'Currency',
  XpryDt date comment 'Expiry date',
  ReqdExctnDt date comment 'Requested Execution Date',
  ChrgBr text comment 'Charge Bearer',
  PRIMARY KEY (CdtTrfTxInf_Id),
  FOREIGN KEY (InstgAgt) references AGENT(AgtId),
  FOREIGN KEY (InstdAgt) references AGENT(AgtId),
  FOREIGN KEY (IntrmyAgt) references AGENT(AgtId),
  FOREIGN KEY (DbtrId) references PARTY_IDENTIFICATION(PartyIdentificationId),
  FOREIGN KEY (UltmtDbtrId) references PARTY_IDENTIFICATION(PartyIdentificationId),
  FOREIGN KEY (DbtrAgt) references AGENT(AgtId),
  FOREIGN KEY (CdtrAgt) references AGENT(AgtId),
  FOREIGN KEY (CdtrId) references PARTY_IDENTIFICATION(PartyIdentificationId),
  FOREIGN KEY (UltmtCdtrId) references PARTY_IDENTIFICATION(PartyIdentificationId),
  FOREIGN KEY (RgltryRptgId) references REGULATORY_REPORTING(RgltryRptgId),
  FOREIGN KEY (RmtInfId) references REMITTANCE_INFORMATION(RmtInfId),
  FOREIGN KEY (TaxId) references TAX(TaxId)
);
