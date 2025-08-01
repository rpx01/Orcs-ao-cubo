async function updateGameState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  renderGame(data);
}

function renderGame(data) {
  const div = document.getElementById("game-state");

  // Se o jogo terminou, mostra a tela de Fim de Jogo
  if (data.game_over) {
    div.innerHTML = `
      <div class="text-center">
        <h1>Fim de Jogo!</h1>
        <h2>Pontuação Final: ${data.score}</h2>
        <p>Você não tem mana suficiente para derrotar os orcs restantes.</p>
        <button class="btn btn-primary btn-lg" onclick="restartGame()">Jogar Novamente</button>
      </div>
    `;
    return;
  }

  // Caso contrário, renderiza o estado normal do jogo
  div.innerHTML = `
    <div class="d-flex justify-content-between mb-3">
      <h3>Rodada: ${data.round}</h3>
      <h3>Pontuação: ${data.score}</h3>
    </div>

    <div class="card mb-3">
      <div class="card-body">
        <h2 class="card-title">${data.player.name}</h2>
        <p class="card-text font-weight-bold">Mana: ${data.player.mana}</p>
        <div class="d-flex">
          ${data.player.deck.map(card => `
            <div class="card mr-2" style="width: 10rem;">
              <div class="card-body">
                <h5 class="card-title">${card.name}</h5>
                <p class="card-text">Custo: ${card.mana_cost}</p>
                <p class="card-text">Dano: ${card.damage}</p>
              </div>
            </div>
          `).join("")}
        </div>
      </div>
    </div>

    <h3>Orcs em campo:</h3>
    <ul class="list-group">
      ${data.orcs.map(orc => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>${orc.name}</strong><br>
            Vida: ${orc.life} | Pontos: ${orc.points}
          </div>
          <div class="btn-group">
            ${data.player.deck.map(card => `
              <button class="btn btn-sm btn-danger ml-1" onclick="attack('${card.name}', '${orc.name}')" ${data.player.mana < card.mana_cost ? 'disabled' : ''}>
                Atacar com ${card.name}
              </button>
            `).join("")}
          </div>
        </li>
      `).join("")}
    </ul>
  `;
}

async function attack(cardName, orcName) {
  const res = await fetch("/api/attack", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ card_name: cardName, orc_name: orcName })
  });
  const data = await res.json();
  if (data.result === "not_enough_mana") {
      alert("Mana insuficiente!");
  }
  renderGame(data);
}

async function restartGame() {
  await fetch("/api/restart", { method: 'POST' });
  await updateGameState();
}

window.onload = updateGameState;
