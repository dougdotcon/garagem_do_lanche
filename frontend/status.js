
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("nomeCliente").textContent = localStorage.getItem("nome") || "...";
  document.getElementById("telefoneCliente").textContent = localStorage.getItem("telefone") || "...";
  const rua = localStorage.getItem("rua") || "";
  const numero = localStorage.getItem("numero") || "";
  const bairro = localStorage.getItem("bairro") || "";
  document.getElementById("enderecoCliente").textContent = `${rua}, ${numero} – ${bairro}`;
  document.getElementById("complementoCliente").textContent = localStorage.getItem("complemento") || "—";
  document.getElementById("pagamentoCliente").textContent = localStorage.getItem("pagamento") || "...";
  document.getElementById("totalCliente").textContent = localStorage.getItem("total") || "...";
  document.getElementById("acompanhamentoSelecionado").textContent = localStorage.getItem("acompanhamento") || "...";

  atualizarStatus(); // controle visual do status
});

function atualizarStatus() {
  const status = localStorage.getItem("statusPedido") || "aceito";
  const etapas = document.querySelectorAll(".etapa");

  etapas.forEach(etapa => etapa.classList.remove("ativo"));

  if (status === "aceito") etapas[0].classList.add("ativo");
  if (status === "preparo") etapas[1].classList.add("ativo");
  if (status === "entrega") etapas[2].classList.add("ativo");
  if (status === "final") etapas[3].classList.add("ativo");
}
