import mysql.connector 
import streamlit as st
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kush@guha15",
    database="pizza_db"
)

c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS customers (" \
                "id INT AUTO_INCREMENT PRIMARY KEY," \
                "name VARCHAR(100)," \
                "phone VARCHAR(20)," \
                "email VARCHAR(255)," \
                "date DATE" \
                ")")

c.execute("""CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100),
                pizza VARCHAR(50),
                quantity INT,
                total FLOAT,
                date DATE
            )""")
conn.commit()

st.title("🍕 Online Pizza Ordering App")
 
# ----CUSTOMER DETAILS------
st.header("Customer Information")
name = st.text_input("Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email")
order_date = st.date_input("Order Date", datetime.now())

if st.button("Save Details"):
    if name and phone and email:
        c.execute("INSERT INTO customers (name, phone, email, date) VALUES (%s, %s, %s, %s)",
                  (name, phone, email, order_date))
        conn.commit()
        st.success("Customer details saved successfully!")
    else:
        st.error("Please fill in all fields.")

# ----ORDER DETAILS------
st.header("Pizza Menu")

menu = {
    "Margherita (₹200)": 200,
    "Pepperoni (₹350)": 350,
    "Veggie Delight (₹250)": 250,
    "Chicken Supreme (₹400)": 400
}

pizza_choice = st.selectbox("Choose your pizza", list(menu.keys()))
order_list = []
if pizza_choice:
    qty = st.number_input(f"Quantity of {pizza_choice}", min_value=1, step=1, key=pizza_choice)
    if qty > 0:
        total = menu[pizza_choice] * qty
        order_list.append((pizza_choice, qty, total))

if st.button("Add to Order"):
    if name:
        for p, qty, total in order_list:
            c.execute("INSERT INTO orders (customer_name, pizza, quantity, total, date) VALUES (%s, %s, %s, %s, %s)", 
                      (name, p, qty, total, order_date))
        conn.commit()
        st.success("✅ Order added successfully!")
    else:
        st.error("⚠️ Please enter customer details first.")

#------DISPLAY ORDERS-----
st.header("Your Orders")
c.execute("SELECT pizza, quantity, total FROM orders WHERE customer_name=%s", (name,))
orders = c.fetchall()
if orders:
    for pizza, qty, tot in orders:
        st.write(f"{pizza} × {qty} = ₹{tot}")
    total_bill = sum([o[2] for o in orders])
    st.subheader(f"💰 Total Bill: ₹{total_bill}")
else:
    st.info("No orders yet!")

#--------payment(dummy)
if orders:
    st.header("💳 Payment")
    payment_method = st.radio("Choose a payment method", 
                              ["Credit Card", "UPI", "Cash on Delivery"])
    c.execute("UPDATE customers SET payment_method=%s WHERE name=%s AND phone=%s",
                  (payment_method, name, phone))
    conn.commit()
    
    if st.button("Proceed to Payment"):
        st.success(f"✅ Payment Successful via {payment_method}!")
        st.balloons()
        st.info("🎉 Your pizza is on the way 🚴‍♂️🍕")