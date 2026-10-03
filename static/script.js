
const scenarioCards = document.querySelectorAll(".scenario-card");

scenarioCards.forEach((card) => {
    card.addEventListener("click", () => {
        const scenario = card.querySelector(".scenario-title").textContent;

        const params = new URLSearchParams({
            scenario: scenario
        });

        window.location.href = `/chat?${params.toString()}`;
    });
});