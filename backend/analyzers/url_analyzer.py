import re
import ipaddress
from urllib.parse import urlparse


def analyze_urls(message):
    detected_risks = []

    urls = re.findall(r"https?://\S+", message)

    suspicious_tlds = [
        ".xyz",
        ".top",
        ".click",
        ".work",
        ".support",
    ]

    for url in urls:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if not hostname:
            continue

        # HTTPS kontrolü
        if parsed_url.scheme != "https":
            detected_risks.append("Güvenli olmayan HTTP bağlantısı")

        # Şüpheli domain uzantısı kontrolü
        if any(hostname.endswith(tld) for tld in suspicious_tlds):
            detected_risks.append("Şüpheli alan adı uzantısı")

        # Domain yerine IP adresi kullanılmış mı?
        try:
            ipaddress.ip_address(hostname)
            detected_risks.append("Bağlantıda doğrudan IP adresi kullanımı")
        except ValueError:
            pass

        # Çok uzun URL
        if len(url) > 100:
            detected_risks.append("Aşırı uzun bağlantı")

    return detected_risks