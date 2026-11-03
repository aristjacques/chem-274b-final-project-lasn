from banking_system import BankingSystem
 

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        # Store account_id strings and corresponding balance integers in an accounts dictionary
        self.accounts: dict[str, int] = {}


    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given identifier if it doesn't already exist. 
        Returns True if the account was successfully created 
        or False if an account with account_id already exists.
        """
        # Return False if the account already exists
        if account_id in self.accounts:
            return False
        # Otherwise create it with a starting balance of 0
        else:
            self.accounts[account_id] = 0
            return True


    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Should transfer the given amount of money from account
        `source_account_id` to account `target_account_id`.
        Returns the balance of `source_account_id` if the transfer
        was successful or `None` otherwise.
          * Returns `None` if `source_account_id` or
          `target_account_id` doesn't exist.
          * Returns `None` if `source_account_id` and
          `target_account_id` are the same.
          * Returns `None` if account `source_account_id` has
          insufficient funds to perform the transfer.
        """
        # Return None if source_account_id or target_account_id is not in the accounts dictionary
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        
        # Return None if source_account_id and target_account_id are the same
        if source_account_id == target_account_id:
            return None

        # Return None if the source account's balance is less than the desired transfer amount
        if self.accounts[source_account_id] < amount:
            return None

        # Deduct the given amount from the source account
        self.accounts[source_account_id] -= amount

        # Add the given amount to the target account
        self.accounts[target_account_id] += amount

        # Return the source account's balance after transferring the given amount
        return self.accounts[source_account_id]


    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        account `account_id`.
        Returns the balance of the account after the operation has
        been processed.
        If the specified account doesn't exist, should return
        `None`.
        """

        # Return None if the account to deposit into is not in the accounts dictionary 
        if account_id not in self.accounts:
            return None

        # Add the deposited money to the acount
        self.accounts[account_id] += amount
        # Return the new balance of the account
        return self.accounts[account_id]