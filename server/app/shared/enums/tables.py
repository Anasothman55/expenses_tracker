from enum import StrEnum


class AccountTypeEnum(StrEnum):
  Checking = "checking"
  Savings = "savings"
  Wallet = "wallet"
  CreditCard = "credit_card"
  Investment = "investment"

  Cash = "cash"                  # Optional if different from wallet
  Loan = "loan"                  # Mortgage, personal loan
  Asset = "asset"                # House, car, gold
  EWallet = "e_wallet"           # PayPal, Apple Pay, Google Pay
  DigitalWallet = "digital_wallet"  # Apple Pay, Samsung Pay
  Crypto = "crypto"              # Bitcoin, Ethereum


class TransactionTypeEnum(StrEnum):
    Expenses = "expenses"
    Incomes = "incomes"













