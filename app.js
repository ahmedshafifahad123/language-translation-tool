document.addEventListener("DOMContentLoaded", () => {
  const text = document.getElementById("sourceText");
  const count = document.getElementById("charCount");
  const source = document.getElementById("source");
  const target = document.getElementById("target");

  text.addEventListener("input", () => {
    count.textContent = `${text.value.length} / 5,000`;
  });

  document.getElementById("clearBtn").addEventListener("click", () => {
    text.value = "";
    count.textContent = "0 / 5,000";
    text.focus();
  });

  document.getElementById("swapBtn").addEventListener("click", () => {
    if (source.value === "auto") return;
    [source.value, target.value] = [target.value, source.value];
  });

  const copyButton = document.getElementById("copyBtn");
  const translated = document.getElementById("translatedText");
  if (copyButton && translated) {
    copyButton.addEventListener("click", async () => {
      await navigator.clipboard.writeText(translated.innerText);
      copyButton.querySelector("span").textContent = "Copied!";
      setTimeout(() => copyButton.querySelector("span").textContent = "Copy", 1500);
    });
  }
});
