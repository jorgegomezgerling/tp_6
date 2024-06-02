import json
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

class PaymentProcessor:
    """Class to process payments using bank accounts and maintain a log of transactions."""
    def __init__(self):
        self.accounts = {
            "token1": BankAccount("C598-ECF9-F0F7-881A", 1000),
            "token2": BankAccount("C598-ECF9-F0F7-881B", 2000)
        }
        self.payments = self._load_payments()
        self.last_account = None

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

    def process_payment(self, order_number, amount):
        """Process a payment and route it to an account with sufficient balance."""
        if self.last_account == "token1":
            next_account = "token2"
        else:
            next_account = "token1"

        for token in [next_account, self.last_account]:
            account = self.accounts.get(token)
            if account and account.withdraw(amount):
                self.payments.append((order_number, token, amount))
                self.last_account = token
                self._save_payments()
                return token, amount
        return None, 0

    def list_payments(self):
        """List all payments made in chronological order."""
        return iter(self.payments)

def main():
    if len(sys.argv) < 2:
        print("Usage: python getJasonR.py <sitedata.json> <token> <amount> OR python getJasonR.py list")
        return

    if sys.argv[1] == "list":
        processor = PaymentProcessor()
        print("Payments list:")
        for payment in processor.list_payments():
            print(payment)
        return

    if len(sys.argv) != 4:
        print("Usage: python getJasonR.py <sitedata.json> <token> <amount>")
        return

    sitedata_file = sys.argv[1]
    token = sys.argv[2]
    amount = int(sys.argv[3])

    # Load tokens
    token_manager = TokenManager()
    with open(sitedata_file) as file:
        token_manager.tokens = json.load(file)

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
