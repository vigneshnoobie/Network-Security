from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

class WarehouseManagementSystem:
    def __init__(self):
        pass

    

    def get_inventory(self):
        conn = sqlite3.connect("inventory.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM products")
            rows = c.fetchall()
            inventory = [{"product_id": row[0], "name": row[1], "description": row[2], 
                          "quantity": row[3], "location": row[4], "stage": row[5]} for row in rows]
            return inventory
        except sqlite3.Error as e:
            return {"error": str(e)}
        finally:
            conn.close()

warehouse = WarehouseManagementSystem()



@app.route("/inventory", methods=["GET"])
def get_inventory():
    if request.method == "GET":
        inventory = warehouse.get_inventory()
        return jsonify(inventory)
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == "__main__":
    app.run(debug=True)
 


