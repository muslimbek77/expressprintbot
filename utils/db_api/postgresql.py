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
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
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

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(13) NOT NULL,
        myaddress VARCHAR(50) NOT NULL,
        username varchar(255) NULL,
        mylanguage varchar(2) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name,mylanguage, username, telegram_id,phone_number,myaddress):
        sql = "INSERT INTO users (full_name,mylanguage, username, telegram_id, phone_number, myaddress) VALUES($1, $2, $3, $4, $5,$6) returning *"
        return await self.execute(sql, full_name,mylanguage, username, telegram_id,phone_number,myaddress, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

  
    
    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
        id SERIAL PRIMARY KEY,
        category VARCHAR(50) NOT NULL,
        subcategory VARCHAR(50) NOT NULL,
        productname VARCHAR(50) NOT NULL,
        photo varchar(255) NULL,
        price INT NOT NULL, 
        descriptions VARCHAR(3000) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_product(self, category,subcategory, productname, photo,price,descriptions):
        sql = "INSERT INTO Products (category,subcategory, productname, photo, price, descriptions) VALUES($1, $2, $3, $4, $5,$6) returning *"
        return await self.execute(sql, category,subcategory, productname, photo,price,descriptions, fetchrow=True)

    async def get_categories(self):
        sql = "SELECT DISTINCT category FROM Products"
        return await self.execute(sql, fetch=True)

    async def get_subcategories(self, category):
        sql = f"SELECT DISTINCT subcategory FROM Products WHERE category='{category}'"
        return await self.execute(sql, fetch=True)

    async def count_products(self, category, subcategory=None):
        if subcategory:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category}' AND subcategory_code='{subcategory}'"
        else:
            sql = f"SELECT COUNT(*) FROM Products WHERE category_code='{category}'"
        return await self.execute(sql, fetchval=True)


#new

    # async def get_products_category(self, category, subcategory):
    #     sql = f"SELECT * FROM Products WHERE category='{category}' AND subcategory='{subcategory}'"
    #     return await self.execute(sql, fetch=True)
    
    async def get_products(self):
        sql = f"SELECT * FROM Products"
        return await self.execute(sql, fetch=True)

    async def product_for_basket(self, item_id):
        sql = f"SELECT * FROM Products WHERE id={item_id}"
        return await self.execute(sql, fetchrow=True)
   

    async def get_product_names(self, category,subcategory):
        sql = f"SELECT DISTINCT productname FROM Products WHERE category='{category}' and subcategory='{subcategory}'"
        return await self.execute(sql, fetch=True) 

    async def get_product(self, category,subcategory,productname):
        sql = f"SELECT * FROM Products WHERE productname='{productname}' and category='{category}' and subcategory='{subcategory}'"
        return await self.execute(sql, fetchrow=True)
    
    async def delete_product(self,item_id):
        await self.execute(f"DELETE FROM Products WHERE id={item_id}", execute=True)


    async def delete_products(self):
        await self.execute("DELETE FROM Products WHERE TRUE", execute=True)

    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)





#.
    async def create_table_basket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Bskts (
        id SERIAL PRIMARY KEY,

        item_id VARCHAR(50) NOT NULL,
        user_id BIGINT NOT NULL,
        product_count INT DEFAULT 1
        );
        """
        await self.execute(sql, execute=True)

       
    async def drop_basket(self):
        await self.execute("DROP TABLE Bskts", execute=True)

    async def delete_basket(self,item_id):
        await self.execute(f"DELETE FROM Bskts WHERE item_id='{item_id}'", execute=True)

    async def add_basket(self, item_id, user_id, product_count=1):
        sql = "INSERT INTO Bskts (item_id, user_id, product_count) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, item_id, user_id, product_count, fetchrow=True)
        

    async def get_baskets(self, user_id):
        sql = f"SELECT * FROM Bskts WHERE user_id={user_id}"
        return await self.execute(sql, fetch=True)
    
    async def get_bskts_where(self, user_id, item_id):
        sql = f"SELECT * FROM Bskts WHERE user_id={user_id} AND item_id='{item_id}'"
        return await self.execute(sql, fetchrow=True)


    async def get_count(self, user_id, item_id):
        sql = f"SELECT product_count FROM Bskts WHERE user_id={user_id} AND item_id='{item_id}'"
        return await self.execute(sql, fetchval=True)




    async def plus_count(self, user_id, item_id):
        sql = f"UPDATE Bskts SET product_count=product_count + 1 WHERE user_id={user_id} AND item_id='{item_id}'"
        return await self.execute(sql, fetchval=True)

    async def minus_count(self, user_id, item_id):
        sql = f"UPDATE Bskts SET product_count=product_count - 1 WHERE user_id={user_id} AND item_id='{item_id}'"
        return await self.execute(sql, fetchval=True)
    
    async def del_count(self, user_id, item_id):
        sql = f"DELETE FROM Bskts WHERE user_id={user_id} AND item_id='{item_id}'"
        return await self.execute(sql, execute=True)






