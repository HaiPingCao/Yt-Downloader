const connectBtn = document.getElementById("connectBtn");
const clearBtn = document.getElementById("clearBtn");
const output = document.getElementById("output");

const log = (msg) => {
  const p = document.createElement("p");
  p.className = "log";
  p.textContent = msg;
  output.appendChild(p);
};

connectBtn.addEventListener("click", () => {
  const url = document.getElementById("url").value;
  const v_start = parseInt(document.getElementById("v_start").value);
  const v_end = parseInt(document.getElementById("v_end").value);

  const ws = new WebSocket("ws://127.0.0.1:8000/ws/music_info");

  ws.onopen = () => {
    ws.send(JSON.stringify({ url, v_start, v_end }));
    log("✅ WebSocket connected");
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    const item = document.createElement("div");
    item.className = "item";

    const header = document.createElement("div");
    header.className = "header";
    header.textContent = `🎵 Video ${data.index}: ${data.title}`;

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

  ws.onclose = () => log("❌ WebSocket closed");
  ws.onerror = (err) => log("⚠️ Lỗi WebSocket: " + err.message);
});

// 🧹 Nút clear output
clearBtn.addEventListener("click", () => {
  output.innerHTML = "";
});
