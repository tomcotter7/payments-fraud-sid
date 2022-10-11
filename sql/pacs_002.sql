-- Author: Thomas Cotter
--LXA: Payments Fraud Data Model

-- pacs002 table
-- Third and final in the set of Messages that is sent across in the Credit Transfer Process. 
-- Payments Clearing and Settlement Message with approval / rejection status of payment
-- Single Message can have multiple Credit Transfer Transaction ID to track.
create or replace table PACS_002 (
  MsgId text not null unique comment 'Message identifier',
  OrgnlMsgId text not null references PACS_008(MsgId) comment 'The original pacs008 message',
  OrgnlTxId text references CDT_TRF_TX_INF(CdtTrfTxInf_Id) comment 'The original unique identifier for transaction',
  InstgAgt int references AGENT(AgtId) comment 'Instructing agent',
  InstdAgt int references AGENT(AgtId) comment 'Instructed agent',
  OrgnlTxRef int comment 'Reference Number for Original Transaction',
  OrgnlCreDtTm datetime comment 'Original Message Creation Date Time',
  CreDtTm datetime comment 'Creation Date Time',
  TxSts text comment 'Transaction Status if rejected or successful ; is usally a code',
  StsRsnInf  text comment 'Detailed Reason for Status',
  PRIMARY KEY (MsgId),
  FOREIGN KEY (OrgnlMsgId) references PACS_008(MsgId),
  FOREIGN KEY (OrgnlTxId) references CDT_TRF_TX_INF(CdtTrfTxInf_Id),
  FOREIGN KEY (InstgAgt) references AGENT(AgtId),
  FOREIGN KEY (InstdAgt) references AGENT(AgtId)
);
