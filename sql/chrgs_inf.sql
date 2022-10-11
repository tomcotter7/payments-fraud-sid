-- Author: Thomas Cotter
--LXA: Payments Fraud Data Model

-- Charges Information Table
-- Component of Third and final in the set of Messages that is sent across in the Credit Transfer Process. 
-- PACS 002 Payments Clearing and Settlement Message with approval / rejection status of payment
-- Single Message can have multiple Credit Transfer Transaction ID to track.
create or replace table CHRGS_INF (
  MsgId int references PACS002(MsgId) comment 'The pacs002 message',
  CdtTrfTxInf_Id int references CDT_TRF_TX_INF(CdtTrfTxInf_Id) comment 'The transaction id',
  Amt float comment 'The charge amount',
  Ccy text comment 'The charge currency',
  Agt int references AGENT(AgtId) comment 'The agent that performed these charges',
  FOREIGN KEY (MsgId) references PACS002(MsgId),
  FOREIGN KEY (CdtTrfTxInf_Id) references CDT_TRF_TX_INF(CdtTrfTxInf_Id),
  FOREIGN KEY (Agt) references AGENT(AgtId)
);
