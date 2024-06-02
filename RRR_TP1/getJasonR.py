import json
import random
import sys

class TokenManager:
    """Singleton class to manage tokens and keys from a JSON file."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._load_tokens(cls._instance)
        return cls._instance

    @staticmethod
    def _load_tokens(self):
        """Load tokens from the JSON file."""
        with open('sitedata.json') as file:
            self.tokens = json.load(file)

    def get_token(self, name):
        """Get the token key by name."""
        return self.tokens.get(name)

class BankAccount:
    """Class representing a bank account with a token and balance."""
    def __init__(self, token, balance):
        self.token = token
        self.balance = balance

    def withdraw(self, amount):
        """Withdraw an amount from the account if there are sufficient funds."""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def deposit(self, amount):
        """Deposit an amount into the account."""
        self.balance += amount

    def get_balance(self):
        """Get the current balance of the account."""
        return self.balance

class PaymentIterator:
    """Iterator class for iterating over payments."""
    def __init__(self, payments):
        self._payments = payments
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._payments):
            result = self._payments[self._index]
            self._index += 1
            return result
        raise StopIteration

class PaymentProcessor:
    """Class to process payments using bank accounts and maintain a log of transactions."""
    def __init__(self):
        self.accounts = {
            "token1": BankAccount("C598-ECF9-F0F7-881A", 1000),
            "token2": BankAccount("C598-ECF9-F0F7-881B", 2000)
        }
        self.payments = self._load_payments()
        self.last_account = None  # Initialize to None to start with random token selection
        self.current_token_index = 0  # Index to track the last token used for payment

    def process_payment(self, order_number, amount):
        """Process a payment and route it to an account with a balance closest to the payment amount."""
        best_account = None
        best_difference = float('inf')  # Initialize to infinity to find the closest balance

        for token, account in self.accounts.items():
            if account.balance >= amount:
                difference = abs(account.balance - amount)
                if difference < best_difference:
                    best_account = token
                    best_difference = difference

        if best_account:
            account = self.accounts[best_account]
            account.withdraw(amount)
            self.payments.append((order_number, best_account, amount))
            self.last_account = best_account
            self._save_payments()
            return best_account, amount
        else:
            return None, 0


    def _load_payments(self):
        """Load payments from a JSON file."""
        try:
            with open('payments.json') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_payments(self):
        """Save payments to a JSON file."""
        with open('payments.json', 'w') as file:
            json.dump(self.payments, file)

    def list_payments(self):
        """List all payments made in chronological order."""
        return PaymentIterator(self.payments)

    def clear_payments(self):
        """Clear all payments and reset account balances to 0."""
        self.payments = []
        for account in self.accounts.values():
            account.balance = 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python getJasonR.py <sitedata.json> <amount> OR python getJasonR.py list OR python getJasonR.py clear")
        return

    if sys.argv[1] == "list":
        processor = PaymentProcessor()
        print("Payments list:")
        for payment in processor.list_payments():
            print(payment)
        return

    if sys.argv[1] == "clear":
        processor = PaymentProcessor()
        processor.clear_payments()
        print("All payments have been cleared.")
        return

    if len(sys.argv) != 3:
        print("Usage: python getJasonR.py <sitedata.json> <amount>")
        return

    sitedata_file = sys.argv[1]
    amount = int(sys.argv[2])

    # Process payment
    processor = PaymentProcessor()
    order_number = len(processor.payments) + 1
    processed_token, processed_amount = processor.process_payment(order_number, amount)

    if processed_token:
        print(f"Payment {order_number} processed: token={processed_token}, amount={processed_amount}")
    else:
        print(f"Payment {order_number} failed: insufficient funds")

    # List payments
    print("Payments list:")
    for payment in processor.list_payments():
        print(payment)

if __name__ == "__main__":
    main()
