from analyzers.message_analyzer import analyze_message
from analyzers.url_analyzer import analyze_urls
from services.risk_engine import calculate_risk


def test_safe_url():
    risks = analyze_urls("https://google.com")
    assert risks == []


def test_phishing_message():
    message = (
        "Hesabınız askıya alınacak. "
        "Hemen giriş yapın: "
        "http://192.168.1.50/banka-login"
    )

    message_risks = analyze_message(message)
    url_risks = analyze_urls(message)

    detected_risks = message_risks + url_risks

    result = calculate_risk(detected_risks)

    assert "Aciliyet belirten ifade" in detected_risks
    assert "Hesap veya erişim tehdidi" in detected_risks
    assert "Kişisel veya giriş bilgisi talebi" in detected_risks
    assert "Güvenli olmayan HTTP bağlantısı" in detected_risks
    assert "Bağlantıda doğrudan IP adresi kullanımı" in detected_risks

    assert result["score"] == 100
    assert result["level"] == "HIGH"


def test_normal_message():
    message = "Merhaba, bugün saat 15.00'te görüşebilir miyiz?"

    message_risks = analyze_message(message)
    url_risks = analyze_urls(message)

    detected_risks = message_risks + url_risks

    result = calculate_risk(detected_risks)

    assert detected_risks == []
    assert result["score"] == 0
    assert result["level"] == "LOW"