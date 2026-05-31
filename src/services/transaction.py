from alembic.environment import Optional
from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
    async def read_all(
        self, account_id: int, limit: int, skip: int = 0, tipo: str = "all"
    ) -> list[Record]:
        if tipo not in ("all", TransactionType.DEPOSIT, TransactionType.WITHDRAWAL):
            raise ValueError(
                "Invalid transaction type. Must be 'all', 'deposit' or 'withdrawal'."
            )

        query = accounts.select().where(accounts.c.id == account_id)
        account = await database.fetch_one(query)
        if not account:
            raise AccountNotFoundError

        if tipo != "all":
            query = transactions.select().where(
                (transactions.c.account_id == account_id)
                & (transactions.c.type == tipo)
            )
        else:
            query = (
                transactions.select()
                .where(transactions.c.account_id == account_id)
                .limit(limit)
                .offset(skip)
            )
        return await database.fetch_all(query)

    @database.transaction()
    async def create(self, transaction: TransactionIn) -> Record | None:
        if len(str(transaction.amount).split(".")[1]) > 2:
            raise ValueError(
                "Balance must be a valid currency amount with two decimal places."
            )

        query = accounts.select().where(accounts.c.id == transaction.account_id)
        account = await database.fetch_one(query)
        if not account:
            raise AccountNotFoundError

        if transaction.type == TransactionType.WITHDRAWAL:
            balance = account.balance - 100 * transaction.amount  # type: ignore
            if balance < 0:
                raise BusinessError("Operation not carried out due to lack of balance")
        else:
            balance = account.balance + 100 * transaction.amount  # type: ignore

        # Create transaction entry
        transaction_id = await self.__register_transaction(transaction)
        # Update account balance
        await self.__update_account_balance(transaction.account_id, balance)

        query = transactions.select().where(transactions.c.id == transaction_id)
        return await database.fetch_one(query)

    async def __update_account_balance(self, account_id: int, balance: float) -> None:
        command = (
            accounts.update().where(accounts.c.id == account_id).values(balance=balance)
        )
        await database.execute(command)

    async def __register_transaction(self, transaction: TransactionIn) -> int:
        command = transactions.insert().values(
            account_id=transaction.account_id,
            type=transaction.type,
            amount=transaction.amount,
        )
        return await database.execute(command)
