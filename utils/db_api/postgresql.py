from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # async def create_table_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS products_user (
    #     id SERIAL PRIMARY KEY,
    #     full_name VARCHAR(255) NOT NULL,
    #     username varchar(255) NULL,
    #     telegram_id BIGINT NOT NULL UNIQUE
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO products_user (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM products_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM products_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM products_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE products_user SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM products_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE products_user", execute=True)

    async def check_telegram_id(self, tg_id):
        sql = "SELECT * FROM products_user WHERE telegram_id=$1"
        return await self.execute(sql, tg_id, fetch=True)
    # async def create_table_products(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS products_product (
    #     id SERIAL PRIMARY KEY,
    #     Mahsulot_nomi VARCHAR(255) NOT NULL,
    #     Mahsulot_narhi varchar(20) NULL,
    #     Mahsulot_rasmi varchar(255) NOT NULL
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    async def add_product(self, Mahsulot_nomi, Mahsulot_narhi, Mahsulot_rasmi):
        sql = "INSERT INTO products_product (nomi, narhi, rasmi) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, Mahsulot_nomi, Mahsulot_narhi, Mahsulot_rasmi, fetchrow=True)

    async def select_all_products(self):
        sql = "SELECT * FROM products_product"
        return await self.execute(sql, fetch=True)

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM products_product WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_products(self):
        sql = "SELECT COUNT(*) FROM products_product"
        return await self.execute(sql, fetchval=True)


    async def delete_products(self):
        await self.execute("DELETE FROM products_product WHERE TRUE", execute=True)

    async def drop_products(self):
        await self.execute("DROP TABLE products_product", execute=True)