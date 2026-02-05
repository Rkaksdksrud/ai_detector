const editor = document.getElementById("editor");
let events = [];

function now() {
  return performance.now();
}

// 키보드
editor.addEventListener("keydown", e => {
  events.push({
    type: "keydown",
    key: e.key,
    t: now()
  });
});

editor.addEventListener("keyup", e => {
  events.push({
    type: "keyup",
    key: e.key,
    t: now()
  });
});

// 붙여넣기
editor.addEventListener("paste", e => {
  const text = e.clipboardData.getData("text");
  events.push({
    type: "paste",
    length: text.length,
    t: now()
  });
});

// 마우스
document.addEventListener("mousemove", e => {
  events.push({
    type: "mousemove",
    x: e.clientX,
    y: e.clientY,
    t: now()
  });
});

function download() {
  const blob = new Blob([JSON.stringify(events)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "session.json";
  a.click();
}