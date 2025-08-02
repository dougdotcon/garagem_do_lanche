
function selecionarPrato(nome, preco) {
  localStorage.setItem("pratoSelecionado", nome);
  localStorage.setItem("precoSelecionado", preco);
  window.location.href = "entrega.html";
}
