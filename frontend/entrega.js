
document.addEventListener("DOMContentLoaded", () => {
  atualizarTotal();
});

function buscarCEP() {
  const cep = document.getElementById("cep").value.replace(/\D/g, '');
  if (cep.length === 8) {
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then(response => response.json())
      .then(data => {
        if (!data.erro) {
          document.getElementById("rua").value = data.logradouro || "";
          document.getElementById("bairro").value = data.bairro || "";
          atualizarTotal();
        }
      });
  }
}

function calcularTaxaEntrega(bairro) {
  if (!bairro) return 5.00;
  const nome = bairro.toLowerCase();
  if (nome.includes("gramacho")) return 1.00;
  if (nome.includes("centro")) return 2.00;
  if (nome.includes("parque") || nome.includes("vila")) return 3.00;
  if (nome.includes("jardim") || nome.includes("mutuá")) return 4.00;
  return 5.00;
}

function atualizarTotal() {
  const preco = parseFloat(localStorage.getItem("precoSelecionado"));
  const bairro = document.getElementById("bairro")?.value || "";
  const taxa = calcularTaxaEntrega(bairro);
  const total = preco + taxa;
  document.getElementById("prato-selecionado").innerText = `Seu pedido: ${localStorage.getItem("pratoSelecionado")}`;
  document.getElementById("total-pedido").innerText = `Total: R$ ${total.toFixed(2)} (inclui R$ ${taxa.toFixed(2)} de entrega)`;
}

function finalizarPedido(event) {
  event.preventDefault();
  const acompanhamento = document.querySelector('input[name="acompanhamento"]:checked');
  if (!acompanhamento) {
    alert("Escolha um acompanhamento.");
    return;
  }

  localStorage.setItem("nome", document.getElementById("nome").value);
  localStorage.setItem("telefone", document.getElementById("telefone").value);
  localStorage.setItem("rua", document.getElementById("rua").value);
  localStorage.setItem("numero", document.getElementById("numero").value);
  localStorage.setItem("bairro", document.getElementById("bairro").value);
  localStorage.setItem("complemento", document.getElementById("complemento").value);
  localStorage.setItem("pagamento", document.getElementById("pagamento").value);
  localStorage.setItem("acompanhamento", acompanhamento.value);
  window.location.href = "status.html";
}
