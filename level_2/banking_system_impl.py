from banking_system import BankingSystem
 

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        # Store account_id strings and corresponding balance integers in an accounts dictionary
        self.accounts: dict[str, int] = {}
        # Store account_id strings and corresponding spending integers in an account_spending dictionary
        self.account_spending: dict[str, int] = {}


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

            # add default spending of 0
            self.account_spending[account_id] = 0

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

        # add exception if amount is negative:
        if amount < 0:
            raise ValueError("Amount to transfer cannot be negative")

        # Deduct the given amount from the source account
        self.accounts[source_account_id] -= amount

        # Add the given amount to the target account
        self.accounts[target_account_id] += amount

        # Add the transferred amount to the source account's spending
        self.account_spending[source_account_id] += amount
        
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

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest outgoing transactions - the total amount of
        money either transferred out of or paid/withdrawn (the
        **pay** operation will be introduced in level 3) - sorted in
        descending order, or in case of a tie, sorted alphabetically
        by `account_id` in ascending order.
        The result should be a list of strings in the following
        format: `["<account_id_1>(<total_outgoing_1>)", "<account_id
        _2>(<total_outgoing_2>)", ..., "<account_id_n>(<total_outgoi
        ng_n>)"]`.
            * If less than `n` accounts exist in the system, then return
            all their identifiers (in the described format).
            * Cashback (an operation that will be introduced in level 3)
            should not be reflected in the calculations for total
            outgoing transactions.
        """
        
        # default implementation
        # if n is less than or equal 0 return an empty list 
        if n <= 0:
            return []
        
        # use sorted function key, value pairs of our spending dictionary
        # set sort to sort by dict values in DESCENDING order using lambda function that returns negative value of a dict entry tuple (index 1)
        # include the account ID as a secondary sort key in ascending order to meet the following spec: 
            # in case of a tie, sorted alphabetically by `account_id` in ascending order.
        
        spending_sorted = sorted(self.account_spending.items(), 
                                    key = lambda account_value_tuple : (-account_value_tuple[1], account_value_tuple[0]))

        # now build list that is of size n from this sorted list. 
        results = []
        # if fewer than n accounts exists, slicing should still return all accounts
        for account_id, spending in spending_sorted[:n]:
            results.append(f"{account_id}({spending})")

        return results