import re


def analyze_message(message):
    message = message.lower()

    detected_risks = []

    urgency_words = [
        "hemen",
        "acil",
        "son şans",
        "şimdi",
        "derhal",
    ]

    threat_words = [
        "hesabınız kapatılacak",
        "hesabınız askıya alınacak",
        "hesabınız bloke edildi",
        "erişiminiz engellenecek",
    ]

    credential_words = [
        "şifrenizi girin",
        "kart bilgilerinizi girin",
        "giriş yapın",
        "hesabınızı doğrulayın",
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

    if re.search(r"https?://\S+", message):
        detected_risks.append("Mesaj içerisinde bağlantı bulundu")

    return detected_risks