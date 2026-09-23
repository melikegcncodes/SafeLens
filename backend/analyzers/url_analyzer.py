import re
import ipaddress
from urllib.parse import urlparse


def analyze_urls(message):
    detected_risks = []

    urls = re.findall(r"https?://[^\s]+", message)

    shortener_domains = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd",
        "cutt.ly",
    ]

    suspicious_keywords = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "confirm",
        "bank",
        "wallet",
        "giris",
        "dogrula",
        "hesap",
        "banka",
        "guvenli",
    ]

    for url in urls:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if not hostname:
            continue

        hostname = hostname.lower()

        # HTTPS kullanılmıyorsa
        if parsed_url.scheme != "https":
            if "Güvenli olmayan HTTP bağlantısı" not in detected_risks:
                detected_risks.append("Güvenli olmayan HTTP bağlantısı")

        # Domain yerine IP adresi kullanılmış mı?
        try:
            ipaddress.ip_address(hostname)

            if "Bağlantıda doğrudan IP adresi kullanımı" not in detected_risks:
                detected_risks.append(
                    "Bağlantıda doğrudan IP adresi kullanımı"
                )

        except ValueError:
            pass

        # URL kısaltma servisi kullanılmış mı?
        if hostname in shortener_domains:
            if "Kısaltılmış bağlantı kullanımı" not in detected_risks:
                detected_risks.append("Kısaltılmış bağlantı kullanımı")

        # Şüpheli kelimeler domain veya URL içinde bulunuyor mu?
        url_lower = url.lower()

        if any(keyword in url_lower for keyword in suspicious_keywords):
            if "Bağlantıda şüpheli anahtar kelime" not in detected_risks:
                detected_risks.append(
                    "Bağlantıda şüpheli anahtar kelime"
                )

        # @ işareti kullanıcıyı yanıltmak için kullanılabilir
        if "@" in parsed_url.netloc:
            if "Bağlantıda yanıltıcı @ karakteri" not in detected_risks:
                detected_risks.append(
                    "Bağlantıda yanıltıcı @ karakteri"
                )

        # Punycode domain kontrolü
        if "xn--" in hostname:
            if "Punycode alan adı kullanımı" not in detected_risks:
                detected_risks.append("Punycode alan adı kullanımı")

        # Çok uzun URL
        if len(url) > 100:
            if "Aşırı uzun bağlantı" not in detected_risks:
                detected_risks.append("Aşırı uzun bağlantı")

    return detected_risks