// after.js - Chatbot dengan AI/LLM (contoh pakai fetch ke backend Python)
async function chatbot(input) {
  const response = await fetch("https://mental-health-support-chatbot-by-jackdev.streamlit.app/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input })
  });
  const data = await response.json();
  return data.reply;
}

// Demo
chatbot("Saya lagi sedih").then(console.log);
// Output: Bisa lebih natural, tergantung jawaban LLM
