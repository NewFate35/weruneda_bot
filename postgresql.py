import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False, executemany: bool = False):
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
                elif executemany:
                    result = await connection.executemany(command, *args)
            return result

    async def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS saturday_training(
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE,
        FIO VARCHAR(255),
        phone VARCHAR(255), 
        children_count INT,
        meat_count INT,
        vegan_count INT
        );
        
        CREATE TABLE IF NOT EXISTS Users(
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE 
        );
        
        CREATE TABLE IF NOT EXISTS registration(
        id INT PRIMARY KEY,
        status BOOLEAN DEFAULT FALSE
        );
        
        CREATE TABLE IF NOT EXISTS last_message(
        id INT PRIMARY KEY,
        message_id BIGINT
        );
        
        CREATE TABLE IF NOT EXISTS duo_run(
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT UNIQUE,
        fio VARCHAR(255),
        phone VARCHAR(255)
        );
        
        INSERT INTO registration(id, status) VALUES (1, FALSE) ON CONFLICT DO NOTHING ;
        """
        await self.execute(sql, execute=True)

    async def add_user_training(self, user_id, FIO, phone, children_count, meat_count, vegan_count):
        sql = "INSERT INTO saturday_training(user_id, FIO, phone, children_count, meat_count, vegan_count) " \
              "VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT(user_id) DO UPDATE " \
              "SET FIO=$2, phone=$3, children_count=$4, meat_count=$5, vegan_count=$6;"
        return await self.execute(sql, user_id, FIO, phone, int(children_count), int(meat_count), int(vegan_count),
                                  fetchrow=True)

    async def add_user_duo_run(self, telegram_id, fio, phone):
        sql = "INSERT INTO duo_run(telegram_id, fio, phone) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"
        return await self.execute(sql, telegram_id, fio, phone, fetchrow=True)

    async def select_all_id_users(self):
        sql = "SELECT telegram_id FROM users"
        return await self.execute(sql, fetch=True)

    async def select_last_msg_id(self):
        sql = "SELECT message_id FROM last_message WHERE id=1"
        return await self.execute(sql, fetch=True)

    async def get_users_info(self):
        sql = "SELECT * FROM saturday_training"
        return await self.execute(sql, fetch=True)

    async def add_user(self, telegram_id):
        sql = "INSERT INTO users(telegram_id) VALUES ($1) ON CONFLICT DO NOTHING"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def insert_last_message_id(self, msg_id):
        sql = "INSERT INTO last_message(id, message_id) VALUES (1, $1) ON CONFLICT (id) " \
              "DO UPDATE SET message_id=$1 WHERE last_message.id=1"
        return await self.execute(sql, msg_id, fetchrow=True)

    async def drop_table_last_mess(self):
        sql = "TRUNCATE TABLE last_message"
        return await self.execute(sql, fetchrow=True)

    async def open_reg(self):
        sql = "UPDATE registration SET status=True WHERE id=1"
        return await self.execute(sql, fetchrow=True)

    async def close_reg(self):
        sql = "UPDATE registration SET status=False WHERE id=1"
        return await self.execute(sql, fetchrow=True)

    async def check_reg_status(self):
        sql = "SELECT * FROM registration WHERE id=1"
        return await self.execute(sql, fetchrow=True)

    async def check_user(self, user_id):
        sql = "SELECT * FROM saturday_training WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM saturday_training WHERE user_id=$1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def count(self):
        sql = "SELECT COUNT(*) FROM saturday_training"
        return await self.execute(sql, fetchval=True)

    async def duo_count(self):
        sql = "SELECT COUNT(*) FROM duo_run"
        return await self.execute(sql, fetchval=True)

    async def children_count(self):
        sql = "SELECT SUM(children_count) FROM saturday_training"
        return await self.execute(sql, fetchval=True)

    async def meat_count(self):
        sql = "SELECT SUM(meat_count) FROM saturday_training"
        return await self.execute(sql, fetchval=True)

    async def vegan_count(self):
        sql = "SELECT SUM(vegan_count) FROM saturday_training"
        return await self.execute(sql, fetchval=True)

    async def delete_all(self):
        sql = "TRUNCATE TABLE saturday_training"
        return await self.execute(sql, fetchrow=True)
