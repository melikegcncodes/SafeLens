// =====================================================
// SafeLens Frontend
// =====================================================


// -------------------------
// OCR TEXT CLEANING
// -------------------------

function cleanOcrText(text) {
    const ignoredPatterns = [
        /web\.whatsapp\.com/i,
        /mac için whatsapp/i,
        /bir mesaj yazın/i,
        /tüm yer işaretleri/i,
        /chrome kullanılabilir/i,
        /yeni chrome kullanılabilir/i,
        /arama yap/i,
        /okunmamış/i,
        /favoriler/i,
        /gruplar/i,
        /yeni sohbet/i
    ];

    const lines = text
        .split(/\r?\n/)
        .map(line => line.trim())
        .filter(line => line.length >= 4)
        .filter(line =>
            !ignoredPatterns.some(pattern => pattern.test(line))
        )
        .filter(line => {
            // URL'leri mutlaka koru
            if (/https?:\/\/|www\./i.test(line)) {
                return true;
            }

            // En az iki anlamlı kelime içersin
            const words =
                line.match(/[A-Za-zÇĞİÖŞÜçğıöşü]{2,}/g) || [];

            return words.length >= 2;
        });

    return [...new Set(lines)].join("\n");
}


// -------------------------
// IMAGE PREPARATION
// -------------------------

function prepareImageForOcr(file) {
    return new Promise((resolve, reject) => {
        const image = new Image();
        const objectUrl = URL.createObjectURL(file);

        image.onload = () => {
            try {
                // Mobil/dikey ekran görüntüsüne dokunma
                if (image.height >= image.width) {
                    URL.revokeObjectURL(objectUrl);
                    resolve(file);
                    return;
                }

                // Masaüstü screenshot:
                // üst browser kısmı + sol tarafın büyük bölümünü kırp
                const cropX = Math.floor(image.width * 0.34);
                const cropY = Math.floor(image.height * 0.14);
                const cropWidth = Math.floor(image.width * 0.66);
                const cropHeight = Math.floor(image.height * 0.86);

                const canvas = document.createElement("canvas");
                canvas.width = cropWidth;
                canvas.height = cropHeight;

                const ctx = canvas.getContext("2d");

                if (!ctx) {
                    throw new Error("Canvas oluşturulamadı.");
                }

                ctx.drawImage(
                    image,
                    cropX,
                    cropY,
                    cropWidth,
                    cropHeight,
                    0,
                    0,
                    cropWidth,
                    cropHeight
                );

                canvas.toBlob(blob => {
                    URL.revokeObjectURL(objectUrl);

                    if (!blob) {
                        reject(new Error("Görsel hazırlanamadı."));
                        return;
                    }

                    resolve(blob);
                }, "image/png");

            } catch (error) {
                URL.revokeObjectURL(objectUrl);
                reject(error);
            }
        };

        image.onerror = () => {
            URL.revokeObjectURL(objectUrl);
            reject(new Error("Görsel okunamadı."));
        };

        image.src = objectUrl;
    });
}


// -------------------------
// MESSAGE ANALYSIS
// -------------------------

async function analyzeMessage() {
    const messageBox = document.getElementById("message");
    const analyzeButton = document.getElementById("analyzeButton");

    const message = messageBox.value.trim();

    if (!message) {
        alert(
            "Lütfen analiz edilecek bir mesaj girin veya ekran görüntüsü yükleyin."
        );
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

        const resultSection = document.getElementById("result");
        const scoreElement = document.getElementById("riskScore");
        const levelElement = document.getElementById("riskLevel");
        const progressBar = document.getElementById("progressBar");
        const summaryCard = document.getElementById("summaryCard");
        const riskDetails = document.getElementById("riskDetails");

        resultSection.classList.remove("hidden");

        scoreElement.textContent = data.risk_score;

        const levelClass = data.risk_level.toLowerCase();

        levelElement.textContent = data.risk_level;
        levelElement.className = "level " + levelClass;

        progressBar.className = "progress-bar " + levelClass;
        progressBar.style.width = data.risk_score + "%";

        summaryCard.className = "summary-card " + levelClass;

        if (data.risk_level === "HIGH") {
            summaryCard.textContent =
                "⚠ Bu içerikte birden fazla güçlü phishing veya dolandırıcılık işareti tespit edildi. Bağlantılara tıklamamanız ve kişisel bilgilerinizi paylaşmamanız önerilir.";

        } else if (data.risk_level === "MEDIUM") {
            summaryCard.textContent =
                "⚠ Bu içerikte bazı şüpheli işaretler bulunuyor. İşlem yapmadan önce göndereni ve bağlantıları dikkatlice doğrulayın.";

        } else {
            summaryCard.textContent =
                "✓ Belirgin bir phishing veya dolandırıcılık işareti tespit edilmedi. Yine de bilinmeyen kaynaklardan gelen bağlantılarda dikkatli olun.";
        }

        riskDetails.innerHTML = "";

        const details = data.risk_details || [];

        if (details.length === 0) {
            const safeCard = document.createElement("div");

            safeCard.className = "safe-card";
            safeCard.textContent =
                "✓ Belirgin bir güvenlik riski tespit edilmedi.";

            riskDetails.appendChild(safeCard);

        } else {
            details.forEach(detail => {
                const card = document.createElement("div");
                card.className = "risk-card";

                const title = document.createElement("h4");
                title.className = "risk-title";
                title.textContent = "⚠ " + detail.risk;

                const whyTitle = document.createElement("div");
                whyTitle.className = "detail-label";
                whyTitle.textContent = "Neden riskli?";

                const why = document.createElement("p");
                why.textContent = detail.why;

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

        resultSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {
        console.error(error);

        alert(
            "Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin."
        );

    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analiz Et";
    }
}


// -------------------------
// CLEAR EVERYTHING
// -------------------------

function clearAnalysis() {
    const messageBox = document.getElementById("message");
    const result = document.getElementById("result");
    const progressBar = document.getElementById("progressBar");
    const riskLevel = document.getElementById("riskLevel");
    const summaryCard = document.getElementById("summaryCard");
    const riskDetails = document.getElementById("riskDetails");
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementById("imagePreview");
    const ocrStatus = document.getElementById("ocrStatus");

    messageBox.value = "";

    document.getElementById("riskScore").textContent = "0";

    riskLevel.textContent = "LOW";
    riskLevel.className = "level";

    progressBar.style.width = "0%";
    progressBar.className = "progress-bar";

    summaryCard.textContent = "";
    summaryCard.className = "summary-card";

    riskDetails.innerHTML = "";

    result.classList.add("hidden");

    imageInput.value = "";

    imagePreview.removeAttribute("src");
    imagePreview.classList.add("hidden");

    ocrStatus.textContent = "";
    ocrStatus.classList.add("hidden");

    messageBox.focus();
}


// -------------------------
// OCR / SCREENSHOT UPLOAD
// -------------------------

const imageInput = document.getElementById("imageInput");

imageInput.addEventListener("change", async event => {
    const file = event.target.files[0];

    if (!file) {
        return;
    }

    const preview = document.getElementById("imagePreview");
    const ocrStatus = document.getElementById("ocrStatus");
    const messageBox = document.getElementById("message");
    const resultSection = document.getElementById("result");

    resultSection.classList.add("hidden");

    // Original image preview
    const previewUrl = URL.createObjectURL(file);

    preview.src = previewUrl;
    preview.classList.remove("hidden");

    preview.onload = () => {
        URL.revokeObjectURL(previewUrl);
    };

    ocrStatus.classList.remove("hidden");
    ocrStatus.textContent =
        "📖 Görsel OCR için hazırlanıyor...";

    try {
        if (typeof Tesseract === "undefined") {
            throw new Error("Tesseract yüklenemedi.");
        }

        const ocrImage =
            await prepareImageForOcr(file);

        ocrStatus.textContent =
            "📖 Görseldeki metin okunuyor...";

        const result =
            await Tesseract.recognize(
                ocrImage,
                "tur+eng",
                {
                    logger: info => {
                        if (
                            info.status ===
                            "recognizing text"
                        ) {
                            const percent =
                                Math.round(
                                    info.progress * 100
                                );

                            ocrStatus.textContent =
                                `📖 Metin okunuyor... %${percent}`;
                        }
                    }
                }
            );

        const extractedText =
            cleanOcrText(result.data.text);

        if (!extractedText) {
            messageBox.value = "";

            ocrStatus.textContent =
                "⚠ Görselde yeterli miktarda okunabilir metin bulunamadı.";

            return;
        }

        messageBox.value = extractedText;

        ocrStatus.textContent =
            "✓ Metin başarıyla çıkarıldı. Gerekirse metni düzenleyip Analiz Et butonuna basabilirsiniz.";

    } catch (error) {
        console.error(error);

        ocrStatus.textContent =
            "⚠ Görsel okunurken bir hata oluştu. Daha net bir ekran görüntüsü deneyin.";
    }
});