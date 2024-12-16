                                    Cashier

***
For run the project:
1. Clone the repository using `git clone`.
2. Set up a database in `PostgreSQL`.
3. Create a new file called `.env` in the project root and fill it as shown in `.env.example`.
4. Create a new file called `alembic.ini` in the project root and fill it as shown in `alembic.ini.example`.
5. Install the requirements `pip install -r requirements.txt`
6. Run `alembic upgrade head` in terminal.
7. Run `uvicorn main:app --reload` in terminal.
***

*Note:*

If needed, you can provide database link in `project/alembic.ini` file by `sqlalchemy.url` param.
