async function restartGame() {
    await fetch('/restart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });
}

async function startGame(storyKey) {
    document.getElementById("story-selection").style.display = "none";
    document.getElementById("loader").style.display = "";

    let response = await fetch('/start_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story_key: storyKey })
    });

    let data = await response.json();
    
    document.getElementById("loader").style.display = "none";
    document.getElementById("restart-button").style.display = "flex";
    document.getElementById("story-output").style.display = "block";
    const outputElement = document.getElementById("story-text");
    formattedText = formatStoryText(data.story);
    await typeText(outputElement, formattedText, 8)
    generateChoices(data.choices);
}

async function makeChoice(choiceText) {
    document.getElementById("choices").style.display = "none";
    document.getElementById("loader").style.display = "";

    let response = await fetch('/next_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice: choiceText })
    });

    let data = await response.json();
    document.getElementById("loader").style.display = "none";
    const outputElement = document.getElementById("story-text");
    formattedText = formatStoryText(data.story_update);
    await typeText(outputElement, formattedText, 8)
    generateChoices(data.choices);
    document.getElementById("choices").style.display = "";
}

function generateChoices(choices) {
    let choicesDiv = document.getElementById("choices");
    choicesDiv.innerHTML = "";

    choices.forEach(choice => {
        let button = document.createElement("button");
        button.innerText = choice;
        if (choice == " ") {
            showPopup('That choice does not exist. Please try again.')
        }
        else if (choice == "") {
            showPopup('That choice does not exist. Please try again.')
        }
        else {
            button.onclick = () => makeChoice(choice);
            button.className = "glow-on-hover";
            choicesDiv.appendChild(button);
        }
    });
}

function typeText(element, text, speed = 100) {
    return new Promise((resolve) => {
        let index = 0;
        element.textContent = '';

        function type() {
            if (index < text.length) {
                element.textContent += text[index];
                index++;
                setTimeout(type, speed); // Continue typing with setTimeout
            } else {
                resolve(); // Resolve the promise when typing is complete
            }
        }

        type();
    });
}

function formatStoryText(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, "$1");
    text = text.replace(/\*(.*?)\*/g, "$1");
    
    return text;
}




function showPopup(message) {
    const popup = document.getElementById("popup");
    const messageElement = document.getElementById("popup-message");

    messageElement.innerText = message;
    popup.style.display = "flex";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}
