import React, { useState, useEffect } from "react";
import {
  listCategories,
  createCategory,
  assignBudget,
  listBudget,
  createTransaction,
} from "./api";

function App() {
  const [categories, setCategories] = useState([]);
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {
    listCategories().then(setCategories);
  }, []);

  const handleAddCategory = async () => {
    const name = prompt("Enter category name:");
    if (name) {
      await createCategory(name);
      setCategories(await listCategories());
    }
  };

  const handleAssignBudget = async () => {
    const category_id = prompt("Category ID:");
    const month = prompt("Month (YYYY-MM):");
    const amount = prompt("Amount:");
    await assignBudget(Number(category_id), month, Number(amount));
    setBudgets(await listBudget(month));
  };

  const handleTransaction = async () => {
    const category_id = prompt("Category ID:");
    const month = prompt("Month (YYYY-MM):");
    const amount = prompt("Amount (negative=spend):");
    await createTransaction(Number(category_id), Number(amount), month);
    setBudgets(await listBudget(month));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Budgeting App</h1>
      <button onClick={handleAddCategory}>Add Category</button>
      <button onClick={handleAssignBudget}>Assign Budget</button>
      <button onClick={handleTransaction}>Record Transaction</button>

      <h2>Categories</h2>
      <ul>
        {categories.map((c) => (
          <li key={c.id}>{c.id}: {c.name}</li>
        ))}
      </ul>

      <h2>Budgets</h2>
      <ul>
        {budgets.map((b) => (
          <li key={b.id}>
            Cat {b.category_id} | {b.month} | Budgeted: {b.budgeted} | Spent: {b.spent} | Balance: {b.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
