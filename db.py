import sqlite3


class Bot:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                   id            INTEGER    PRIMARY KEY AUTOINCREMENT,
                                   user_id       INTEGER    NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                                   connect_date  DATETIME   NOT NULL DEFAULT (DATETIME('now'))
                               )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                                   id         INTEGER    PRIMARY KEY AUTOINCREMENT,
                                   user_id    INTEGER    NOT NULL,
                                   oper       BOOLEAN    NOT NULL,
                                   summ       DECIMAL    NOT NULL,
                                   category   text       NOT NULL DEFAULT (''),
                                   date       DATETIME   NOT NULL DEFAULT (DATETIME('now'))
                               )''')

    def user_exists(self, user_id):
        ans = False
        helper = self.cursor.execute('''SELECT id FROM users WHERE user_id = ?''', (user_id,))

        if len(helper.fetchall()) > 0:
            ans = True

        return ans

    def get_user_id(self, user_id):
        ans = self.cursor.execute('''SELECT id FROM users WHERE user_id = ?''', (user_id,))

        return ans.fetchone()[0]

    def add(self, user_id):
        self.cursor.execute('''INSERT INTO users (user_id) VALUES (?)''', (user_id,))

        return self.conn.commit()

    def add_record(self, user_id, operation, value, category = ''):
        self.cursor.execute('''INSERT INTO records (user_id, oper, summ, category) VALUES (?, ?, ?, ?)''',
                            (self.get_user_id(user_id), operation == "+", value if operation == "+" else -1 * value, category))

        return self.conn.commit()

    def get_records(self, user_id, time = "all"):

        if time == "day":
            result = self.cursor.execute('''SELECT * FROM records
                                            WHERE user_id = ? AND date BETWEEN datetime('now', 'start of day') AND
                                                                               datetime('now', 'localtime')
                                            ORDER BY date ASC''', (self.get_user_id(user_id),))
        elif time == "week":
            result = self.cursor.execute('''SELECT * FROM records
                                            WHERE user_id = ? AND date BETWEEN datetime('now', '-6 days') AND
                                                                               datetime('now', 'localtime')
                                            ORDER BY date ASC''', (self.get_user_id(user_id),))
        elif time == "month":
            result = self.cursor.execute('''SELECT * FROM records
                                            WHERE user_id = ? AND date BETWEEN datetime('now', 'start of month') AND
                                                                               datetime('now', 'localtime')
                                            ORDER BY date ASC''', (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute('''SELECT * FROM records
                                            WHERE user_id = ?
                                            ORDER BY date ASC''', (self.get_user_id(user_id),))

        return result.fetchall()

    def total(self, user_id):
        result = self.cursor.execute('''SELECT sum(summ)
                                        FROM records
                                        WHERE user_id = ?''', (self.get_user_id(user_id),))

        return result.fetchall()

    def get_stat(self, user_id):
        result = self.cursor.execute('''SELECT category, sum(summ) AS s
                                        FROM records
                                        WHERE user_id = ? AND category != ''
                                        GROUP BY category
                                        ORDER BY s ASC, category ASC''', (self.get_user_id(user_id),))

        return result.fetchall()

    def close(self):
        self.connection.close()
