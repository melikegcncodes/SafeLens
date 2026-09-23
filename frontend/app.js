async function analyzeMessage() {
    const message = document.getElementById("message").value;
    const analyzeButton = document.getElementById("analyzeButton");

    if (!message.trim()) {
        alert("Lütfen analiz edilecek bir mesaj girin.");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analiz ediliyor...";

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

        if (!response.ok) {
            throw new Error("Sunucu hatası oluştu.");
        }

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

        const summaryCard =
            document.getElementById("summaryCard");

        const levelClass =
            data.risk_level.toLowerCase();

        levelElement.textContent =
            data.risk_level;

        levelElement.className =
            "level " + levelClass;

        progressBar.className =
            "progress-bar " + levelClass;

        progressBar.style.width =
            data.risk_score + "%";


        summaryCard.className =
            "summary-card " + levelClass;

        if (data.risk_level === "HIGH") {
            summaryCard.textContent =
                "⚠ Bu içerikte birden fazla güçlü phishing veya dolandırıcılık işareti tespit edildi. Bağlantılara tıklamamanız ve kişisel bilgilerinizi paylaşmamanız önerilir.";
        }

        else if (data.risk_level === "MEDIUM") {
            summaryCard.textContent =
                "⚠ Bu içerikte bazı şüpheli işaretler bulunuyor. İşlem yapmadan önce göndereni ve bağlantıları dikkatlice doğrulayın.";
        }

        else {
            summaryCard.textContent =
                "✓ Belirgin bir phishing veya dolandırıcılık işareti tespit edilmedi. Yine de bilinmeyen kaynaklardan gelen bağlantılarda dikkatli olun.";
        }


        const riskDetails =
            document.getElementById("riskDetails");

        riskDetails.innerHTML = "";

        if (data.risk_details.length === 0) {
            const safeCard =
                document.createElement("div");

            safeCard.className = "safe-card";

            safeCard.textContent =
                "✓ Belirgin bir güvenlik riski tespit edilmedi.";

            riskDetails.appendChild(safeCard);

        } else {
            data.risk_details.forEach(detail => {
                const card =
                    document.createElement("div");

                card.className = "risk-card";


                const title =
                    document.createElement("h4");

                title.className = "risk-title";

                title.textContent =
                    "⚠ " + detail.risk;


                const whyTitle =
                    document.createElement("div");

                whyTitle.className =
                    "detail-label";

                whyTitle.textContent =
                    "Neden riskli?";


                const why =
                    document.createElement("p");

                why.textContent =
                    detail.why;


                const recommendationTitle =
                    document.createElement("div");

                recommendationTitle.className =
                    "detail-label recommendation-label";

                recommendationTitle.textContent =
                    "Ne yapmalısınız?";


                const recommendation =
                    document.createElement("p");

                recommendation.textContent =
                    detail.recommendation;


                card.appendChild(title);

                card.appendChild(whyTitle);
                card.appendChild(why);

                card.appendChild(recommendationTitle);
                card.appendChild(recommendation);

                riskDetails.appendChild(card);
            });
        }

    } catch (error) {
        alert("Analiz sırasında bir hata oluştu.");

        console.error(error);

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analiz Et";
    }
}


function clearAnalysis() {
    document.getElementById("message").value = "";

    document
        .getElementById("result")
        .classList.add("hidden");

    document.getElementById("riskScore").textContent = "0";

    document.getElementById("progressBar").style.width = "0%";

    document.getElementById("riskDetails").innerHTML = "";

    document.getElementById("summaryCard").innerHTML = "";
}