import unittest
from unittest.mock import patch
import sqlite3
import os

from Final_Source_Code import WarehouseManagementSystem, Product

class TestWarehouseManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a temporary test database for testing
        cls.conn = sqlite3.connect(":memory:")
        cls.c = cls.conn.cursor()
        cls.c.execute('''CREATE TABLE products
                         (product_id INT PRIMARY KEY, name TEXT, description TEXT, quantity INT, location TEXT, stage TEXT)''')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
       
        self.warehouse = WarehouseManagementSystem()

    def tearDown(self):
        
        self.warehouse.products = []

    def test_add_product(self):
        self.warehouse.add_product(1, "Test Product", "Test Description", 10, "Test Location", "Test Stage")
        self.assertEqual(len(self.warehouse.products), 1)
        self.assertEqual(self.warehouse.products[0].name, "Test Product")

    def test_update_inventory(self):
        self.warehouse.add_product(1, "Test Product", "Test Description", 10, "Test Location", "Test Stage")
        self.warehouse.update_inventory(1, 20)
        self.assertEqual(self.warehouse.products[0].quantity, 20)

    

if __name__ == "__main__":
    unittest.main()
