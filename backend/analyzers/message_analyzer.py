def analyze_message(message):
    message = message.lower()

    detected_risks = []

    urgency_words = [
        "hemen",
        "acil",
        "son şans",
        "şimdi",
        "derhal",
        "24 saat içinde",
    ]

    threat_words = [
        "hesabınız kapatılacak",
        "hesabınız askıya alınacak",
        "hesabınız bloke edildi",
        "erişiminiz engellenecek",
        "hesabınız kilitlenecek",
    ]

    credential_terms = [
        "şifre",
        "şifreniz",
        "şifrenizi",
        "sifre",
        "parola",
        "pin",
        "cvv",
        "kart numarası",
        "kart numaranızı",
        "kimlik bilgisi",
        "kimlik bilgilerinizi",
        "tc kimlik",
    ]

    request_terms = [
        "gönder",
        "gönderin",
        "yolla",
        "yollayın",
        "paylaş",
        "paylaşın",
        "gir",
        "girin",
        "ver",
        "verin",
        "ilet",
        "iletin",
        "yaz",
        "yazın",
    ]

    reward_words = [
        "ödül kazandınız",
        "hediye kazandınız",
        "para kazandınız",
        "ücretsiz hediye",
        "çekiliş kazandınız",
    ]

    for word in urgency_words:
        if word in message:
            detected_risks.append("Aciliyet belirten ifade")
            break

    for word in threat_words:
        if word in message:
            detected_risks.append("Hesap veya erişim tehdidi")
            break

    credential_detected = any(
        term in message
        for term in credential_terms
    )

    request_detected = any(
        term in message
        for term in request_terms
    )

    if credential_detected and request_detected:
        detected_risks.append(
            "Kişisel veya giriş bilgisi talebi"
        )

    for word in reward_words:
        if word in message:
            detected_risks.append(
                "Şüpheli ödül veya kazanç vaadi"
            )
            break

    return detected_risks