def calculate_risk(detected_risks):
    risk_weights = {
        "Aciliyet belirten ifade": 15,
        "Hesap veya erişim tehdidi": 25,
        "Kişisel veya giriş bilgisi talebi": 30,
        "Mesaj içerisinde bağlantı bulundu": 20,
    }

    score = 0

    for risk in detected_risks:
        score += risk_weights.get(risk, 0)

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }
def calculate_risk(detected_risks):
    risk_weights = {
        "Aciliyet belirten ifade": 15,
        "Hesap veya erişim tehdidi": 25,
        "Kişisel veya giriş bilgisi talebi": 30,
        "Mesaj içerisinde bağlantı bulundu": 20,

        "Güvenli olmayan HTTP bağlantısı": 20,
        "Şüpheli alan adı uzantısı": 25,
        "Bağlantıda doğrudan IP adresi kullanımı": 30,
        "Aşırı uzun bağlantı": 15,
    }

    score = 0

    for risk in detected_risks:
        score += risk_weights.get(risk, 0)

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"
def calculate_risk(detected_risks):
    risk_weights = {
        "Aciliyet belirten ifade": 15,
        "Hesap veya erişim tehdidi": 25,
        "Kişisel veya giriş bilgisi talebi": 30,
        "Şüpheli ödül veya kazanç vaadi": 20,

        "Güvenli olmayan HTTP bağlantısı": 20,
        "Bağlantıda doğrudan IP adresi kullanımı": 30,
        "Kısaltılmış bağlantı kullanımı": 15,
        "Bağlantıda şüpheli anahtar kelime": 20,
        "Bağlantıda yanıltıcı @ karakteri": 25,
        "Punycode alan adı kullanımı": 20,
        "Aşırı uzun bağlantı": 10,
    }

    score = 0

    for risk in detected_risks:
        score += risk_weights.get(risk, 0)

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }
    