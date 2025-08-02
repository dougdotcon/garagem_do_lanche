document.addEventListener("DOMContentLoaded", () => {
  const pedido = {
    nome: localStorage.getItem("nome"),
    telefone: localStorage.getItem("telefone"),
    prato: localStorage.getItem("pratoSelecionado"),
    acompanhamento: localStorage.getItem("acompanhamento"),
    rua: localStorage.getItem("rua"),
    numero: localStorage.getItem("numero"),
    bairro: localStorage.getItem("bairro"),
    complemento: localStorage.getItem("complemento"),
    pagamento: localStorage.getItem("pagamento"),
    total: document.querySelector("#total-pedido")?.innerText || localStorage.getItem("total")
  };

  const container = document.getElementById("lista-pedidos");

  const card = document.createElement("div");
  card.className = "pedido-card";
  card.innerHTML = `
    <h3>${pedido.nome}</h3>
    <p><strong>Prato:</strong> ${pedido.prato}</p>
    <p><strong>Acompanhamento:</strong> ${pedido.acompanhamento}</p>
    <p><strong>Endereço:</strong> ${pedido.rua}, ${pedido.numero} - ${pedido.bairro}</p>
    ${pedido.complemento ? `<p><strong>Complemento:</strong> ${pedido.complemento}</p>` : ""}
    <p><strong>Telefone:</strong> ${pedido.telefone}</p>
    <p><strong>Pagamento:</strong> ${pedido.pagamento}</p>
    <p><strong>${pedido.total || "Total no ato"}</strong></p>
    <button onclick="imprimirPedido(this)">🖨️ Imprimir Pedido</button>
  `;

  container.appendChild(card);
});

function imprimirPedido(botao) {
  const pedidoHTML = botao.parentElement.innerHTML;
  const janela = window.open("", "", "width=600,height=800");
  janela.document.write(`
    <html>
    <head><title>Imprimir Pedido</title></head>
    <body>${pedidoHTML}</body>
    </html>
  `);
  janela.document.close();
  janela.focus();
  janela.print();
  janela.close();
}
