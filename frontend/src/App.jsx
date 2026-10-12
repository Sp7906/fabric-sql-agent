import { useState } from "react";

const EXAMPLES = [
  "Total revenue by region",
  "Monthly revenue trend",
  "Which product category earns the most?",
];

export default function App() {
  const [q, setQ] = useState("");
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function ask(question) {
    if (!question.trim()) return;
    setLoading(true); setErr(""); setRes(null);
    try {
      const r = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!r.ok) throw new Error(`Request failed (${r.status})`);
      setRes(await r.json());
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Ask your data</h1>
      <p className="sub">Natural language to safe, read-only SQL over the gold layer.</p>

      <div className="row">
        <input value={q} onChange={(e) => setQ(e.target.value)}
               onKeyDown={(e) => e.key === "Enter" && ask(q)}
               placeholder="e.g. Total revenue by region" />
        <button onClick={() => ask(q)} disabled={loading}>{loading ? "Thinking..." : "Ask"}</button>
      </div>
      <div className="chips">
        {EXAMPLES.map((e) => (
          <button key={e} className="chip" onClick={() => { setQ(e); ask(e); }}>{e}</button>
        ))}
      </div>

      {err && <p className="error">{err}</p>}
      {res?.error && <p className="error">{res.error}</p>}

      {res?.sql && (
        <>
          <h3>Generated SQL <span className="tag">{res.mode}</span></h3>
          <pre>{res.sql}</pre>
          {res.attempts.length > 1 && <p className="sub">Self-corrected after {res.attempts.length - 1} failed attempt(s).</p>}
          <div className="scroll">
            <table>
              <thead><tr>{res.columns.map((c) => <th key={c}>{c}</th>)}</tr></thead>
              <tbody>
                {res.rows.map((r, i) => <tr key={i}>{r.map((v, j) => <td key={j}>{String(v)}</td>)}</tr>)}
              </tbody>
            </table>
          </div>
        </>
      )}
    </main>
  );
}
