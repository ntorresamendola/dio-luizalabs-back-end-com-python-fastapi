from databases.interfaces import Record

from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn, AccountOut


class AccountService:
    async def read_all(self, limit: int = 100, skip: int = 0) -> list[Record]:
        query = """
             SELECT id, user_id,
                 CASE WHEN balance THEN balance/100.0 ELSE balance END as balance,
                 created_at
             FROM accounts
             LIMIT :limit OFFSET :skip"""

        return await database.fetch_all(query, values={"limit": limit, "skip": skip})

    async def create(self, account: AccountIn) -> Record | None:
        account_balance = str(account.balance)  # Convert to cents
        if len(str.split(account_balance, ".")[1]) > 2:
            raise ValueError(
                "Balance must be a valid currency amount with two decimal places."
            )
        account_balance = int(float(account_balance) * 100)  # Convert to cents
        command = accounts.insert().values(
            user_id=account.user_id, balance=account_balance
        )
        account_id = await database.execute(command)
        # Modify the column output value conditionally inside the database query
        query = """
            SELECT id, user_id,  
                CASE WHEN balance THEN balance/100.0 ELSE balance END as balance,
                created_at
            FROM accounts
            WHERE accounts.id = :account_id
        """
        query_result = await database.fetch_one(
            query, values={"account_id": account_id}
        )
        return query_result

    async def read_balance(self, account_id: int) -> float | None:
        query = """
            SELECT 
                CASE WHEN balance THEN balance/100.0 ELSE balance END as balance
            FROM accounts
            WHERE accounts.id = :account_id
        """
        query_result = await database.fetch_one(
            query, values={"account_id": account_id}
        )
        return query_result["balance"] if query_result else None
