const API_URL = "/questions?tag=python";

async function loadQuestions() {
    const res = await fetch(API_URL);
    const questions = await res.json();
    const container = document.getElementById("question-list");
    container.innerHTML = "";
    questions.forEach(q => {
        const div = document.createElement("div");
        div.className = "question";
        div.innerHTML = `
            <h3><a href="${q.link}" target="_blank">${q.title}</a></h3>
            <button onclick="this.nextElementSibling.style.display='block'; this.style.display='none'">Show Answer</button>
            <div class="answer">${q.answer}</div>
        `;
        container.appendChild(div);
    });
}

window.onload = loadQuestions;
