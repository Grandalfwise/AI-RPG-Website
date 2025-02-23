async function startGame(storyKey) {
    let response = await fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_key: storyKey })
    });

    let data = await response.json();
    const outputElement = document.getElementById("story-text");
    typeText(outputElement, data.story, 8)
    document.getElementById("story-selection").style.display = "none";
    document.getElementById("restart-button").style.display = "flex";
    document.getElementById("story-output").style.display = "block";
    generateChoices(data.choices);
}

async function makeChoice(choiceText) {
    document.getElementById("choices").style.display = "none";
    let response = await fetch('/next_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice: choiceText })
    });

    let data = await response.json();
    const outputElement = document.getElementById("story-text");
    typeText(outputElement, data.story_update, 8)
    generateChoices(data.choices);
    document.getElementById("choices").style.display = "";
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

function typeText(element, text, speed = 100) {
    let index = 0;
    element.textContent = '';
    
    function type() {
        if (index < text.length) {
            element.textContent += text[index];
            index++;
            setTimeout(type, speed);
        }
    }
    
    type();
}