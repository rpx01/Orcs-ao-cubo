window.onload = async () => {
  const res = await fetch("/api/state");
  const data = await res.json();

  const div = document.getElementById("game-state");
  div.innerHTML = `
    <h2>${data.player.name}</h2>
    <p>Mana: ${data.player.mana}</p>
    <p>Deck: ${data.player.deck.join(", ")}</p>
    <h3>Orcs em campo:</h3>
    <ul>
      ${data.orcs.map(orc => `<li>${orc.name} - Vida: ${orc.life} - Pontos: ${orc.points}</li>`).join("")}
    </ul>
  `;
};
