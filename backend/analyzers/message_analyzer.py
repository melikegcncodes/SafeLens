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

    credential_words = [
        "şifrenizi girin",
        "kart bilgilerinizi girin",
        "giriş yapın",
        "hesabınızı doğrulayın",
        "kimlik bilgilerinizi girin",
        "kart numaranızı girin",
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

    for word in credential_words:
        if word in message:
            detected_risks.append("Kişisel veya giriş bilgisi talebi")
            break

    for word in reward_words:
        if word in message:
            detected_risks.append("Şüpheli ödül veya kazanç vaadi")
            break

    return detected_risks