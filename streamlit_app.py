import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Budgeting App")

# --- Categories ---
st.header("Categories")
if st.button("Load Categories"):
    res = requests.get(f"{API_URL}/categories/")
    if res.ok:
        st.write(res.json())
    else:
        st.error("Failed to fetch categories")

st.subheader("🗑️ Delete Category")
cat_id_to_delete = st.number_input("Category ID to delete", step=1)
if st.button("Delete Category"):
    res = requests.delete(f"{API_URL}/categories/{cat_id_to_delete}")
    if res.ok:
        st.success(f"Category {cat_id_to_delete} deleted!")
    else:
        st.error("Failed to delete category")

new_cat = st.text_input("New Category Name")
if st.button("Add Category"):
    res = requests.post(f"{API_URL}/categories/", json={"name": new_cat})
    if res.ok:
        st.success("Category added!")
    else:
        st.error("Failed to add category")

# --- Transactions ---
st.header("Transactions")
res = requests.get(f"{API_URL}/transactions/")
if res.ok:
    st.table(res.json())

st.subheader("🗑️ Delete Transaction")
tx_id_to_delete = st.number_input("Transaction ID to delete", step=1)
if st.button("Delete Transaction"):
    res = requests.delete(f"{API_URL}/transactions/{tx_id_to_delete}")
    if res.ok:
        st.success(f"Transaction {tx_id_to_delete} deleted!")
    else:
        st.error("Failed to delete transaction")

st.subheader("Add Transaction")
tx_name = st.text_input("Transaction Name")
tx_amount = st.number_input("Amount", step=1)
tx_date = st.date_input("Date")
tx_cat_id = st.number_input("Category ID", step=1)

if st.button("Record Transaction"):
    month_str = str(tx_date)[:7]  # YYYY-MM
    res = requests.post(f"{API_URL}/transactions/", json={
        "category_id": tx_cat_id,
        "amount": int(tx_amount),
        "month": month_str,
        "date": str(tx_date)
    })
    if res.ok:
        st.success("Transaction recorded!")
    else:
        st.error(f"Failed to record transaction: {res.text}")
