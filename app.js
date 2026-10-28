const codeEl = document.getElementById("code");
const langEl = document.getElementById("language");
const levelEl = document.getElementById("level");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const explainBtn = document.getElementById("explainBtn");
const exampleBtn = document.getElementById("exampleBtn");

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function section(title, inner) {
  return `<h2>${title}</h2>${inner}`;
}

function list(items) {
  if (!items || !items.length) return "<p>None.</p>";
  return "<ul>" + items.map((i) => `<li>${esc(i)}</li>`).join("") + "</ul>";
}

exampleBtn.addEventListener("click", async () => {
  const res = await fetch("/example");
  const data = await res.json();
  codeEl.value = data.code;
  langEl.value = data.language;
});

explainBtn.addEventListener("click", async () => {
  const code = codeEl.value.trim();
  if (!code) {
    statusEl.textContent = "Paste some code first.";
    return;
  }
  statusEl.textContent = "Explaining...";
  explainBtn.disabled = true;
  try {
    const res = await fetch("/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, language: langEl.value, level: levelEl.value }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Request failed");
    }
    const d = await res.json();
    const badge = d.demo ? '<span class="demo-badge">DEMO MODE — set LLM_API_KEY for real explanations</span>' : "";
    const lines = d.line_by_line.map(
      (l) => `<pre><code>${esc(l.line)}</code>\n${esc(l.explanation)}</pre>`
    ).join("");
    resultEl.innerHTML =
      badge +
      section("Overview", `<p>${esc(d.overview)}</p>`) +
      section("Line by line", lines || "<p>None.</p>") +
      section("Key concepts", list(d.key_concepts)) +
      section("Possible bugs", list(d.possible_bugs)) +
      section("Improvements", list(d.improvements));
    resultEl.hidden = false;
    statusEl.textContent = "";
  } catch (e) {
    statusEl.textContent = "Error: " + e.message;
  } finally {
    explainBtn.disabled = false;
  }
});
