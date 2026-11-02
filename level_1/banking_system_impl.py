from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):

    def __init__(self):
        # Store account_id strings and corresponding balance integers in an accounts dictionary
        self.accounts: dict[str, int] = {}

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