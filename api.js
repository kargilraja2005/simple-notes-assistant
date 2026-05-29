// =============================================================
// api.js — Shared helpers used by all pages
// =============================================================

const API = "http://127.0.0.1:5000/api";

// ---- Toast notification ----
function showToast(msg, type = "success") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = `show ${type}`;
  setTimeout(() => t.className = "", 3000);
}

// ---- Generic fetch ----
async function apiFetch(path, options = {}) {
  try {
    const res = await fetch(`${API}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");
    return data;
  } catch (err) {
    showToast(err.message, "error");
    throw err;
  }
}

// ---- Notes API ----
const getNotes    = (search = "") => apiFetch(`/notes${search ? "?search=" + encodeURIComponent(search) : ""}`);
const getNote     = (id)          => apiFetch(`/notes/${id}`);
const createNote  = (t, c)        => apiFetch("/notes", { method: "POST", body: JSON.stringify({ title: t, content: c }) });
const updateNote  = (id, t, c)    => apiFetch(`/notes/${id}`, { method: "PUT", body: JSON.stringify({ title: t, content: c }) });
const deleteNote  = (id)          => apiFetch(`/notes/${id}`, { method: "DELETE" });
const togglePin   = (id)          => apiFetch(`/notes/${id}/pin`, { method: "POST" });

// ---- Quiz API ----
const getQuiz     = (id)          => apiFetch(`/notes/${id}/quiz`);
const saveQuiz    = (id, qs)      => apiFetch(`/notes/${id}/quiz`, { method: "POST", body: JSON.stringify({ questions: qs }) });
const deleteQuiz  = (id)          => apiFetch(`/notes/${id}/quiz`, { method: "DELETE" });

// ---- Helpers ----
function formatDate(iso) {
  return new Date(iso).toLocaleString("en-US", {
    month: "short", day: "numeric", year: "numeric",
    hour: "numeric", minute: "2-digit"
  });
}

function escapeHtml(str = "") {
  return str.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function setLoading(btn, on) {
  if (on) {
    btn.dataset.orig = btn.innerHTML;
    btn.innerHTML = `<span class="spinner"></span> Wait...`;
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.orig;
    btn.disabled = false;
  }
}

// ---- Dark mode (persists via localStorage) ----
function initDarkMode() {
  if (localStorage.getItem("dark") === "1") {
    document.body.classList.add("dark");
    const btn = document.getElementById("dark-toggle");
    if (btn) btn.textContent = "☀️";
  }
}

function toggleDark() {
  document.body.classList.toggle("dark");
  const isDark = document.body.classList.contains("dark");
  localStorage.setItem("dark", isDark ? "1" : "0");
  const btn = document.getElementById("dark-toggle");
  if (btn) btn.textContent = isDark ? "☀️" : "🌙";
}
