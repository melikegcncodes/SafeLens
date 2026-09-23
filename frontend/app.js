async function analyzeMessage() {
    const message = document.getElementById("message").value;

    if (!message.trim()) {
        alert("Lütfen analiz edilecek bir mesaj girin.");
        return;
    }

    try {
        const response = await fetch("/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        document
            .getElementById("result")
            .classList.remove("hidden");

        document.getElementById("riskScore").textContent =
            data.risk_score;

        const levelElement =
            document.getElementById("riskLevel");

        const progressBar =
            document.getElementById("progressBar");

        levelElement.textContent =
            data.risk_level;

        levelElement.className = "level";
        progressBar.className = "progress-bar";

        const levelClass =
            data.risk_level.toLowerCase();

        levelElement.classList.add(levelClass);
        progressBar.classList.add(levelClass);

        progressBar.style.width =
            data.risk_score + "%";

        const riskList =
            document.getElementById("riskList");

        riskList.innerHTML = "";

        if (data.detected_risks.length === 0) {
            const li =
                document.createElement("li");

            li.textContent =
                "Belirgin bir risk tespit edilmedi.";

            riskList.appendChild(li);
        } else {
            data.detected_risks.forEach(risk => {
                const li =
                    document.createElement("li");

                li.textContent = risk;

                riskList.appendChild(li);
            });
        }

    } catch (error) {
        alert("Analiz sırasında bir hata oluştu.");
        console.error(error);
    }
}