import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {
  listCategories,
  createCategory,
  createTransaction,
  deleteCategory,
} from "./api";

function App() {
  const [categories, setCategories] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [newTxName, setNewTxName] = useState("");
  const [newTxAmount, setNewTxAmount] = useState("");
  const [newTxDate, setNewTxDate] = useState(new Date());

  // Load categories + transactions on mount
  useEffect(() => {
    listCategories()
      .then((cats) => {
        console.log("Fetched categories:", cats);
        setCategories(cats);
      })
      .catch((err) => {
        console.error("Error fetching categories:", err);
      });

    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/transactions/");
      if (!res.ok) {
        throw new Error(`Failed to fetch transactions: ${res.status}`);
      }
      const data = await res.json();
      console.log("Fetched transactions:", data);
      setTransactions(data);
    } catch (err) {
      console.error("Error fetching transactions:", err);
    }
  };

  const handleAddCategory = async () => {
    const name = prompt("Enter category name:");
    if (name) {
      await createCategory(name);
      const updated = await listCategories();
      setCategories(updated);
    }
  };

  const handleDeleteCategory = async (id) => {
    await deleteCategory(id);
    const updated = await listCategories();
    setCategories(updated);
  };

  const handleAddTransaction = async (category_id) => {
    if (!newTxName || !newTxAmount || !newTxDate) {
      alert("Please fill in all fields");
      return;
    }
    await createTransaction(
      category_id,
      parseFloat(newTxAmount),
      newTxDate.toISOString().slice(0, 10),
      newTxName
    );
    setNewTxName("");
    setNewTxAmount("");
    setNewTxDate(new Date());
    await fetchTransactions();
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontWeight: "normal", marginBottom: "20px" }}>Budgeting App</h1>

      <button
        style={{
          backgroundColor: "#007bff",
          color: "white",
          padding: "10px 20px",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          marginBottom: "20px",
        }}
        onClick={handleAddCategory}
      >
        Add Category
      </button>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {categories.map((c) => (
          <div
            key={c.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "15px",
              width: "260px",
              boxShadow: "2px 2px 6px rgba(0,0,0,0.1)",
              backgroundColor: "#fafafa",
            }}
          >
            <div
              style={{
                marginBottom: "10px",
                fontWeight: "bold",
                fontSize: "16px",
              }}
            >
              {c.name}
            </div>

            {/* Transaction Form */}
            <input
              type="text"
              placeholder="Transaction name"
              value={newTxName}
              onChange={(e) => setNewTxName(e.target.value)}
              style={{ width: "100%", marginBottom: "8px", padding: "6px" }}
            />
            <input
              type="number"
              placeholder="Amount"
              value={newTxAmount}
              onChange={(e) => setNewTxAmount(e.target.value)}
              style={{ width: "100%", marginBottom: "8px", padding: "6px" }}
            />
            <DatePicker
              selected={newTxDate}
              onChange={(date) => setNewTxDate(date)}
              dateFormat="yyyy-MM-dd"
              className="form-control"
              style={{ width: "100%", marginBottom: "8px" }}
            />

            <button
              style={{
                backgroundColor: "#28a745",
                color: "white",
                padding: "6px 12px",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                width: "100%",
                marginBottom: "10px",
              }}
              onClick={() => handleAddTransaction(c.id)}
            >
              Add Transaction
            </button>

            {/* Transactions List */}
            <div style={{ fontSize: "14px", color: "#555" }}>
              <strong>Transactions:</strong>
              <ul style={{ paddingLeft: "18px", marginTop: "6px" }}>
                {transactions
                  .filter((t) => t.category_id === c.id)
                  .map((t) => (
                    <li key={t.id}>
                      {t.name} – {t.amount} ({t.date})
                    </li>
                  ))}
              </ul>
            </div>

            <button
              style={{
                backgroundColor: "#dc3545",
                color: "white",
                padding: "6px 12px",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                width: "100%",
              }}
              onClick={() => handleDeleteCategory(c.id)}
            >
              Delete Category
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
