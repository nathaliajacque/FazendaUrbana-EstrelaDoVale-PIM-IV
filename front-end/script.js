const exitButton = document.getElementById("exitButton");
const modal = document.getElementById("confirmationModal");
const confirmExit = document.getElementById("confirmExit");
const cancelExit = document.getElementById("cancelExit");

// Exibir o modal ao clicar no botão de sair
exitButton.addEventListener("click", () => {
  modal.style.display = "flex";
});


// Fechar o modal ao clicar no botão "Não"
cancelExit.addEventListener("click", () => {
  modal.style.display = "none";
});

// Executar ação ao clicar no botão "Sim"
confirmExit.addEventListener("click", () => {
  modal.style.display = "none";
  // Aqui você pode redirecionar ou realizar outra ação
  window.location.href = "../Login/Login.html";
});

// Fechar o modal ao clicar fora do conteúdo
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});