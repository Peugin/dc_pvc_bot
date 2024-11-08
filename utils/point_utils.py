import sqlite3
from functools import wraps

__conn = sqlite3.connect("points.db")
__cursor = __conn.cursor()


def transaction(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        ___conn = sqlite3.connect("points.db")
        try:
            ___cursor = ___conn.cursor()

            # 2. 开始事务
            ___conn.execute("BEGIN TRANSACTION;")

            # 3. 执行原始函数
            result = func(self, *args, **kwargs)

            # 4. 提交事务
            ___conn.commit()

            return result
        except Exception as e:
            # 5. 如果发生异常，回滚事务
            ___conn.rollback()
            print(f"Transaction failed: {e}")
            raise
        finally:
            # 6. 关闭连接
            ___conn.close()

    return wrapper


# 查詢使用者的當前積分
def get_point(user_id: int) -> int:
    __cursor.execute("SELECT points FROM user_points WHERE user_id = ?", (user_id,))
    result = __cursor.fetchone()
    return result if result is None else result[0]


# 更新使用者的積分
def update_point(user_id: int, updated_points: int):
    __cursor.execute("UPDATE user_points SET points = ? WHERE user_id = ?", (updated_points, user_id))
