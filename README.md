                                    Cashier

***
For run the project:
1. Clone the repository using `git clone`.
2. Set up a database in `PostgreSQL`.
3. Create a new file called `.env` in the project root and fill it as shown in `.env.example`.
4. Install the requirements `pip install -r requirements.txt`
5. Run `alembic upgrade head` in terminal.
6. Run `uvicorn main:app --reload` in terminal.
***

*Note:*

If needed, you can provide database link in `project/alembic.ini` file by `sqlalchemy.url` param.
