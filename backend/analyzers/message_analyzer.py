def analyze_message(message):
    message = message.lower()

    detected_risks = []

    urgency_words = [
        "hemen",
        "acil",
        "acilen",
        "derhal",
        "hemen kontrol edin",
        "bugün içinde",
        "bugun icinde",
        "gecikmeden",
    ]

    threat_words = [
        "hesabınız askıya alınacak",
        "hesabiniz askiya alinacak",
        "hesabınız kapatılacak",
        "hesabiniz kapatilacak",
        "erişiminiz engellenecek",
        "erisiminiz engellenecek",
        "erişiminiz kısıtlanacak",
        "erisiminiz kisitlanacak",
        "erişiminiz geçici olarak kısıtlanabilir",
        "erisiminiz gecici olarak kisitlanabilir",
        "hesabınız bloke edilecek",
        "hesabiniz bloke edilecek",
        "işlemleriniz durdurulacak",
        "islemleriniz durdurulacak",
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
    ]

    reward_words = [
        "ödül",
        "kazandınız",
        "kazandiniz",
        "hediye",
        "çekiliş",
        "cekilis",
        "ücretsiz",
        "ucretsiz",
        "para kazandınız",
        "para kazandiniz",
    ]

    # Aciliyet kontrolü
    for word in urgency_words:
        if word in message:
            detected_risks.append("Aciliyet belirten ifade")
            break

    # Hesap / erişim tehdidi
    for word in threat_words:
        if word in message:
            detected_risks.append("Hesap veya erişim tehdidi")
            break

    # Şifre veya kişisel bilgi talebi
    credential_detected = any(
        term in message for term in credential_terms
    )

    request_detected = any(
        term in message for term in request_terms
    )

    if credential_detected and request_detected:
        detected_risks.append(
            "Kişisel veya giriş bilgisi talebi"
        )

    # Ödül / kazanç vaadi
    for word in reward_words:
        if word in message:
            detected_risks.append(
                "Şüpheli ödül veya kazanç vaadi"
            )
            break

    return detected_risks