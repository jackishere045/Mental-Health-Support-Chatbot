function chatbot(input) {
  if (input.includes("halo")) {
    return "Halo, ada yang bisa saya bantu?";
  } else if (input.includes("sedih")) {
    return "Coba tarik napas dalam, kamu pasti bisa melewatinya.";
  } else {
    return "Maaf, saya tidak mengerti. Bisa ulangi?";
  }
}

console.log(chatbot("halo")); 
// Output: Halo, ada yang bisa saya bantu?
