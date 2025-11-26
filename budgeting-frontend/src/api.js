const API_URL = "http://127.0.0.1:8000";

async function handleResponse(res) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Request failed: ${res.status} ${text}`);
  }
  return res.json();
}

export async function listCategories() {
  const res = await fetch(`${API_URL}/categories/`);
  return handleResponse(res);
}

export async function createCategory(name) {
  const res = await fetch(`${API_URL}/categories/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return handleResponse(res);
}

export async function assignBudget(category_id, month, amount) {
  const res = await fetch(`${API_URL}/budget/assign`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category_id, month, amount }),
  });
  return handleResponse(res);
}

export async function listBudget(month) {
  const res = await fetch(`${API_URL}/budget/${month}`);
  return handleResponse(res);
}

export async function createTransaction(category_id, amount, date, name) {
  const res = await fetch(`${API_URL}/transactions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category_id, amount, date, name }),
  });
  return handleResponse(res);
}

export async function deleteCategory(id) {
  const res = await fetch(`${API_URL}/categories/${id}`, {
    method: "DELETE",
  });
  return handleResponse(res);
}
