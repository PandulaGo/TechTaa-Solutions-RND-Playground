import { useEffect, useState, type FormEvent } from "react";

type Task = { id: number; title: string; done: boolean; created_at: string };

const API = "http://localhost:8000";
const JSON_HEADERS = { "Content-Type": "application/json" };

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");

  async function load() {
    const res = await fetch(`${API}/tasks`);
    setTasks(await res.json());
  }

  useEffect(() => {
    load();
  }, []);

  async function addTask(e: FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;
    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: JSON_HEADERS,
      body: JSON.stringify({ title }),
    });
    setTitle("");
    load();
  }

  async function toggle(task: Task) {
    await fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: JSON_HEADERS,
      body: JSON.stringify({ done: !task.done }),
    });
    load();
  }

  async function remove(id: number) {
    await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div style={{ maxWidth: 480, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Task Tracker</h1>
      <form onSubmit={addTask}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task"
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <input type="checkbox" checked={t.done} onChange={() => toggle(t)} />
            <span style={{ textDecoration: t.done ? "line-through" : "none" }}>
              {t.title}
            </span>
            <button onClick={() => remove(t.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}