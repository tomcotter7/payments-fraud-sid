-- Author: Thomas Cotter
-- LXA: Payments Fraud Data Model

-- pacs008 message
-- Second in the set of Messages that is sent across in the Credit Transfer Process. 
-- Payments Clearing and Settlement Message
-- Single Message can have multiple Credit Transfer Transaction ID to track.
create or replace table PACS_008 (
  MsgId text not null unique comment 'message identifier',
  CreDtTm datetime comment 'Creation Date Time',
  CtrlSum float comment 'Control sum',
  NbOfTxs int comment 'Number of transactions',
  IntrBkSttlmDt datetime comment 'Interbank settlement date',
  CdtTrfTxInf_Id text not null references CDT_TRF_TX_INF(CdtTrfTxInf_Id) comment 'Unique Individual Transaction ID in the Credit Transfer Process',
  PRIMARY KEY (MsgId),
  FOREIGN KEY (CdtTrfTxInf_Id) references CDT_TRF_TX_INF(CdtTrfTxInf_Id)
);
