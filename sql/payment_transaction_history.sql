-- Author: Sidharth Krishnan
-- LXA: Payments Fraud Data Model

-- Payment Transaction History Table
-- Serves as an aggregated to record details about Payment Transaction History of Party
create or replace table PAYMENT_TRANSACTION_HISTORY (
  AccountId int not null references ACCOUNT(AccountId) comment 'The Account id of parties involved making and receiving payments',
  Dt date not null comment 'Date of Transaction',
  StartDayBalance float comment 'Balance at Start of Day',
  EndDayBalance float comment 'Balance at End of Day',
  NbOfDebits int not null comment 'Number of Debits',
  NbOfCredits int not null comment 'Number of Credits',
  AmtDebited float not null comment 'Total Amount Debited',
  AmtCredited float not null comment 'Total Amount Credited',
  FOREIGN KEY (AccountId) references ACCOUNT(AccountId)
);
