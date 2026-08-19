from enum import StrEnum


class AccountTypeEnum(StrEnum):
  Checking = "checking"
  Savings = "savings"
  Wallet = "wallet"
  CreditCard = "credit_card"
  Investment = "investment"

  Loan = "loan"                  # Mortgage, personal loan
  DigitalWallet = "digital_wallet"  # Apple Pay, Samsung Pay


class AccountLoanTypeEnum(StrEnum):
  Owed ="owed" 
  Give ="give"


class TransactionTypeEnum(StrEnum):
  Expenses = "expenses"
  Incomes = "incomes"













