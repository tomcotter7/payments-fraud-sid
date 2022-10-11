-- Author: Thomas Cotter
-- LXA: Payments Fraud Data Model

-- pain001 message
-- First in the set of Messages that is sent across in the Credit Transfer Process. 
-- Payments Initiation Message

create or replace table PAIN_001 (
  MsgId text not null unique comment 'Unique Message identifier',
  CreDtTm datetime comment 'Creation datetime',
  NbOfTxs int comment 'Number of transactions',
  CdtTrfTxInf_Id text not null references CDT_TRF_TX_INF(CdtTrfTxInf_Id) comment 'Unique Individual Transaction ID for Credit Transfer',
  PRIMARY KEY (MsgId),
  FOREIGN KEY (CdtTrfTxInf_Id) references CDT_TRF_TX_INF(CdtTrfTxInf_Id)
);
