async function startGame(storyKey) {
    let response = await fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_key: storyKey })
    });

    let data = await response.json();
    document.getElementById("story-text").innerText = data.story;
    document.getElementById("story-selection").style.display = "none";
    document.getElementById("restart-button").style.display = "flex";
    document.getElementById("story-output").style.display = "block";
    generateChoices(data.choices);
}

async function makeChoice(choiceText) {
    let response = await fetch('/next_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice: choiceText })
    });

    let data = await response.json();
    document.getElementById("story-text").innerText = data.story_update;
    generateChoices(data.choices);

    // Show the restart button
}

function generateChoices(choices) {
    let choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    choices.forEach(choice => {
        let button = document.createElement("button");
        button.innerText = choice;
        button.onclick = () => makeChoice(choice);
        button.className = "glow-on-hover";
        choicesDiv.appendChild(button);
    });
}