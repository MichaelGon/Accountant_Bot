from db import Bot
import sqlite3
import unittest


class Test_Accountant_Bot(unittest.TestCase):
    def test_1(self):
        example = Bot("Test.sqlite")

        example.cursor.execute('''INSERT INTO users (id, user_id) VALUES
                                      (1, 1),
                                      (2, 3)''')

        self.assertEqual(example.user_exists(1), True)
        self.assertEqual(example.user_exists(2), False)

    def test_2(self):
        example = Bot("Test.sqlite")

        example.cursor.execute('''INSERT INTO users (id, user_id) VALUES
                                      (1, 1),
                                      (2, 3)''')

        self.assertEqual(example.get_user_id(1), 1)
        self.assertEqual(example.get_user_id(3), 2)

    def test_3(self):
        example = Bot("Test.sqlite")

        example.cursor.execute('''INSERT INTO users (id, user_id) VALUES
                                      (1, 1),
                                      (2, 3)''')
        example.cursor.execute('''INSERT INTO records (id, user_id, oper, summ) VALUES
                                      (1, 1, TRUE, 1000),
                                      (2, 2, TRUE, 200),
                                      (3, 1, FALSE, -900),
                                      (4, 2, FALSE, -500)''')

        self.assertEqual(example.total(1), [(100, )])
        self.assertEqual(example.total(3), [(-300,)])

    def test_4(self):
        example = Bot("Test.sqlite")

        example.cursor.execute('''INSERT INTO users (id, user_id) VALUES
                                      (1, 1),
                                      (2, 3)''')
        example.cursor.execute('''INSERT INTO records (id, user_id, oper, summ, category) VALUES
                                      (1, 1, FALSE, -1000, 'Food'),
                                      (2, 2, FALSE, -200, 'Food'),
                                      (3, 1, FALSE, -900, 'Advert'),
                                      (4, 2, FALSE, -500, 'Food'),
                                      (5, 2, FALSE, -750, 'Taxi')''')

        self.assertEqual(example.get_stat(1), [('Food', -1000), ('Advert', -900)])
        self.assertEqual(example.get_stat(3), [('Taxi', -750), ('Food', -700)])


if __name__ == 'bot':
    unittest.bot()
