async function updateGameState() {
  const res = await fetch("/api/state");
  const data = await res.json();
  renderGame(data);
}

function renderGame(data) {
  // Se o jogo terminou, mostra a tela de Fim de Jogo (lógica pode ser melhorada)
  if (data.game_over) {
    document.getElementById('game-container').innerHTML = `
      <div style="background-color: rgba(0,0,0,0.8); text-align: center; padding: 50px;">
        <h1>Fim de Jogo!</h1>
        <h2>Pontuação Final: ${data.score}</h2>
        <button onclick="restartGame()">Jogar Novamente</button>
      </div>
    `;
    return;
  }

  // Renderiza a barra superior
  document.getElementById('round-info').innerText = `Rodada: ${data.round}`;
  document.getElementById('score-info').innerText = `Pontuação: ${data.score}`;

  // Renderiza o mapa
  const mapArea = document.getElementById('map-area');
  let mapHtml = '';
  for (let lane = 1; lane <= 6; lane++) {
    mapHtml += `<div class="region-lane"><h4>Região ${lane}</h4>`;
    ['Externa', 'Meio', 'Interna'].forEach((areaName, areaIndex) => {
        mapHtml += `<div><strong>${areaName}:</strong>`;
        data.map[lane][areaIndex].forEach(orc => {
            mapHtml += `<div class="orc-item">${orc.name} (Vida: ${orc.life})</div>`;
        });
        mapHtml += `</div>`;
    });
    mapHtml += '</div>';
  }
  mapArea.innerHTML = mapHtml;

  // Renderiza a área do jogador
  document.getElementById('player-stats').innerHTML = `
    <h2>${data.player.name}</h2>
    <p>Mana: ${data.player.mana}</p>
  `;

  const playerHand = document.getElementById('player-hand');
  playerHand.innerHTML = data.player.deck.map(card => `
    <div class="card-item">
      <h5>${card.name}</h5>
      <p>Custo: ${card.mana_cost}</p>
      <p>Dano: ${card.damage}</p>
      </div>
  `).join('');

  // Renderiza o botão de terminar turno
  document.getElementById('end-turn-container').innerHTML = `
    <button onclick="endTurn()">Terminar Turno</button>
  `;
}

// Função de ataque permanece, mas os botões precisam ser adicionados ao mapa futuramente
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
