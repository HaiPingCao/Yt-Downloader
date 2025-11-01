const connectBtn = document.getElementById("connectBtn");
const clearBtn = document.getElementById("clearBtn");
const output = document.getElementById("output");

const timestamp = () =>
  new Date().toLocaleTimeString("en-GB", { hour12: false }) +
  "." +
  new Date().getMilliseconds();

const log = (msg) => {
  const p = document.createElement("p");
  p.className = "log";
  p.textContent = `[${timestamp()}] ${msg}`;
  output.appendChild(p);
  console.log(`[${timestamp()}] ${msg}`);
};

connectBtn.addEventListener("click", () => {
  const url = document.getElementById("url").value;
  const v_start = parseInt(document.getElementById("v_start").value);
  const v_end = parseInt(document.getElementById("v_end").value);

  const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/music_info`);

  log("Initializing WebSocket...");

  ws.onopen = () => {
    log("✅ WebSocket connected");
    const payload = JSON.stringify({ url, v_start, v_end });
    log(`Sending data: ${payload}`);
    ws.send(payload);
  };

  ws.onmessage = (event) => {
    const now = timestamp();
    log(`Received message at ${now}`);

    const data = JSON.parse(event.data);
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
  ws.onerror = (err) => log(`⚠️ WebSocket error: ${err.message || err}`);
});

// 🧹 Clear output button
clearBtn.addEventListener("click", () => {
  output.innerHTML = "";
  log("🧹 Log cleared");
});
