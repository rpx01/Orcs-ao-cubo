async function updateGameState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  renderGame(data);
}

function renderGame(data) {
  const div = document.getElementById("game-state");

  if (data.game_over) {
    div.innerHTML = `
      <div class="text-center">
        <h1>Fim de Jogo!</h1>
        <h2>Pontuação Final: ${data.score}</h2>
        <p>${data.log[data.log.length - 1] || ''}</p>
        <button class="btn btn-primary btn-lg" onclick="restartGame()">Jogar Novamente</button>
      </div>
    `;
    return;
  }

  let mapHtml = '<div class="row">';
  for (let lane = 1; lane <= 6; lane++) {
    mapHtml += `<div class="col-md-4 border p-2"><h4>Região ${lane}</h4>`;
    const areaNames = ['Externa', 'Meio', 'Interna'];
    for (let area = 0; area < 3; area++) {
      mapHtml += `<div><strong>${areaNames[area]}:</strong>`;
      data.map[lane][area].forEach(orc => {
        mapHtml += `<div class="d-flex justify-content-between align-items-center">`;
        mapHtml += `<span>${orc.name} (Vida: ${orc.life})</span>`;
        mapHtml += `<div>`;
        data.player.deck.forEach(card => {
          mapHtml += `<button class="btn btn-sm btn-danger ml-1" onclick="attack('${card.name}','${orc.id}',${lane},${area})" ${data.player.mana < card.mana_cost ? 'disabled' : ''}>${card.name}</button>`;
        });
        mapHtml += `</div></div>`;
      });
      mapHtml += `</div>`;
    }
    mapHtml += `</div>`;
  }
  mapHtml += `</div><button class="btn btn-primary mt-3" onclick="endTurn()">Terminar Turno</button>`;

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
    ${mapHtml}
  `;
}

async function attack(cardName, orcId, lane, area) {
  const res = await fetch("/api/attack", {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ card_name: cardName, orc_id: orcId, lane: String(lane), area })
  });
  const data = await res.json();
  if (data.result === "not_enough_mana") {
    alert("Mana insuficiente!");
  }
  renderGame(data);
}

async function endTurn() {
  const res = await fetch("/api/end_turn", { method: 'POST' });
  const data = await res.json();
  renderGame(data);
}

async function restartGame() {
  await fetch("/api/restart", { method: 'POST' });
  await updateGameState();
}

window.onload = updateGameState;
