const connectBtn = document.getElementById("connectBtn");
const clearBtn = document.getElementById("clearBtn");
const output = document.getElementById("output");

const timestamp = () => {
  const d = new Date();
  return d.toISOString().split("T")[1]; // e.g., "14:05:32.481Z"
};

const log = (msg, type = "log") => {
  const p = document.createElement("p");
  p.className = `log ${type}`;
  p.textContent = `[${timestamp()}] ${msg}`;
  output.appendChild(p);
  console[type === "error" ? "error" : "log"](`[${timestamp()}] ${msg}`);
};

connectBtn.addEventListener("click", () => {
  const url = document.getElementById("url").value.trim();
  const v_start = parseInt(document.getElementById("v_start").value);
  const v_end = parseInt(document.getElementById("v_end").value);

  if (!url) return log("⚠️ Please enter a valid URL", "error");

  const wsUrl = `ws://${window.location.hostname}:8000/ws/music_info`;
  const ws = new WebSocket(wsUrl);

  log(`Connecting to ${wsUrl}...`);

  ws.onopen = () => {
    log("✅ WebSocket connected");
    const payload = JSON.stringify({ url, v_start, v_end });
    log(`📤 Sending: ${payload}`);
    ws.send(payload);
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const now = timestamp();

    if (data.status === "complete") {
      log(`✅ Completed in ${data.total_time ?? "unknown"}s`);
      return;
    }
    if (data.error) {
      log(`⚠️ Error: ${data.error}`, "error");
      return;
    }

    log(`📥 Message received for video ${data.index}`);

    const item = document.createElement("div");
    item.className = "item";

    const header = document.createElement("div");
    header.className = "header";
    header.textContent = `🎵 [${now}] Video ${data.index}: ${data.title}`;

    const content = document.createElement("div");
    content.className = "content";
    content.textContent = JSON.stringify(data, null, 2);

    header.onclick = () => {
      content.style.display =
        content.style.display === "block" ? "none" : "block";
    };

    item.appendChild(header);
    item.appendChild(content);
    output.appendChild(item);
  };

  ws.onclose = (e) => log(`❌ WebSocket closed (code=${e.code})`);
  ws.onerror = (err) => log(`⚠️ WebSocket error: ${err.message || err}`, "error");
});

// 🧹 Clear output button
clearBtn.addEventListener("click", () => {
  output.innerHTML = "";
  log("🧹 Log cleared");
});
