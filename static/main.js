async function updateGameState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  renderGame(data);
}

function renderGame(data) {
  const div = document.getElementById("game-state");
  div.innerHTML = `
    <div class="card mb-3">
      <div class="card-body">
        <h2 class="card-title">${data.player.name}</h2>
        <p class="card-text">Mana: ${data.player.mana}</p>
        <div class="d-flex">
          ${data.player.deck
            .map(
              (card) => `
            <div class="card mr-2" style="width: 10rem;">
              <div class="card-body">
                <h5 class="card-title">${card.name}</h5>
                <p class="card-text">Custo: ${card.mana_cost}</p>
                <p class="card-text">Dano: ${card.damage}</p>
              </div>
            </div>
          `
            )
            .join("")}
        </div>
      </div>
    </div>

    <h3>Orcs em campo:</h3>
    <ul class="list-group">
      ${data.orcs
        .map(
          (orc) => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
          ${orc.name} - Vida: ${orc.life} - Pontos: ${orc.points}
          <div class="btn-group">
            ${data.player.deck
              .map(
                (card) => `
              <button class="btn btn-sm btn-danger" onclick="attack('${card.name}', '${orc.name}')">
                Atacar com ${card.name}
              </button>
            `
              )
              .join("")}
          </div>
        </li>
      `
        )
        .join("")}
    </ul>
  `;
}

async function attack(cardName, orcName) {
  const res = await fetch("/api/attack", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_name: cardName, orc_name: orcName }),
  });
  const data = await res.json();
  if (data.result === "not_enough_mana") {
    alert("Mana insuficiente!");
  }
  renderGame({ player: data.player, orcs: data.orcs });
}

window.onload = updateGameState;
