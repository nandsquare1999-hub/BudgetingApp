const API_URL = "http://127.0.0.1:8000";

export async function listCategories() {
  const res = await fetch(`${API_URL}/categories/`);
  return res.json();
}

export async function createCategory(name) {
  const res = await fetch(`${API_URL}/categories/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return res.json();
}

export async function assignBudget(category_id, month, amount) {
  const res = await fetch(`${API_URL}/budget/assign`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category_id, month, amount }),
  });
  return res.json();
}

export async function listBudget(month) {
  const res = await fetch(`${API_URL}/budget/${month}`);
  return res.json();
}

export async function createTransaction(category_id, amount, month) {
  const res = await fetch(`${API_URL}/transactions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category_id, amount, month }),
  });
  return res.json();
}
