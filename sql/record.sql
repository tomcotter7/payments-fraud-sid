-- Author: Thomas Cotter

-- Tax Record Table
create or replace table RECORD (
  TaxId int not null references TAX(TaxId),
  Tp text comment 'The type of this tax record',
  Ctgy text comment 'The category of tax paid within this record',
  DbtrSts text comment 'The debtor status',
  PrdYr int comment 'The year of which this tax was paid',
  TaxblBaseAmt float comment 'The taxable base amount',
  TtlAmt float comment 'The amount of tax paid',
  Rate text comment 'The rate at which the tax was paid',
  FrDt date comment 'When did this tax period start',
  ToDt date comment 'When did this tax period end',
  FOREIGN KEY (TaxId) references TAX(TaxId)
);
