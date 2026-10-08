from neo4j import GraphDatabase
from app.core.config import Settings


class Database:
    """Một driver dùng chung; mỗi query mở session riêng. Không cache dữ liệu tiến độ."""

    def __init__(self, settings: Settings):
        self.database = settings.database
        self.driver = GraphDatabase.driver(
            settings.uri, auth=(settings.user, settings.password), connection_timeout=5
        )

    def verify(self):
        self.driver.verify_connectivity()
        self.read("RETURN 1 AS ok")

    def read(self, query: str, **params) -> list[dict]:
        with self.driver.session(database=self.database) as session:
            return session.execute_read(lambda tx: tx.run(query, params).data())

    def write(self, query: str, **params) -> list[dict]:
        with self.driver.session(database=self.database) as session:
            return session.execute_write(lambda tx: tx.run(query, params).data())

    def transaction(self, work):
        """Callback chỉ chứa thao tác DB/tính toán; không gửi email hay đổi session UI vì có retry."""
        with self.driver.session(database=self.database) as session:
            return session.execute_write(work)

    def apply(self, statements: list[str]):
        # DDL chạy riêng; seed được gửi toàn bộ trong một transaction khác.
        with self.driver.session(database=self.database) as session:

            def execute(tx):
                for statement in statements:
                    tx.run(statement).consume()

            session.execute_write(execute)

    def close(self):
        self.driver.close()
