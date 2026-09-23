RISK_EXPLANATIONS = {
    "Aciliyet belirten ifade": {
        "why": "Dolandırıcılık mesajları kullanıcıyı düşünmeden hızlı hareket etmeye zorlayabilir.",
        "recommendation": "Mesajdaki baskıya kapılmadan göndereni ve bağlantıyı doğrulayın."
    },

    "Hesap veya erişim tehdidi": {
        "why": "Hesabın kapatılacağı veya erişimin engelleneceği tehdidi phishing mesajlarında sık kullanılır.",
        "recommendation": "Mesajdaki bağlantıya basmak yerine hizmetin resmi sitesine kendiniz gidin."
    },

    "Kişisel veya giriş bilgisi talebi": {
        "why": "Şifre, kart veya kimlik bilgilerinin istenmesi ciddi bir güvenlik riski oluşturabilir.",
        "recommendation": "Şifre, kart ve kimlik bilgilerinizi mesaj üzerinden paylaşmayın."
    },

    "Şüpheli ödül veya kazanç vaadi": {
        "why": "Beklenmeyen ödül ve para vaatleri kullanıcıyı sahte sayfalara yönlendirmek için kullanılabilir.",
        "recommendation": "Ödülü ilgili kurumun resmi sitesi üzerinden doğrulayın."
    },

    "Güvenli olmayan HTTP bağlantısı": {
        "why": "HTTP bağlantıları HTTPS'in sağladığı şifreli iletişimi kullanmaz.",
        "recommendation": "Özellikle kişisel bilgi isteyen HTTP sayfalarına bilgi girmeyin."
    },

    "Bağlantıda doğrudan IP adresi kullanımı": {
        "why": "Güvenilir hizmetler genellikle kullanıcılarını doğrudan IP adreslerine yönlendirmez.",
        "recommendation": "Bağlantının gerçekten ilgili kuruma ait olduğunu doğrulayın."
    },

    "Kısaltılmış bağlantı kullanımı": {
        "why": "Kısaltılmış bağlantılar gerçek hedef adresini kullanıcıdan gizleyebilir.",
        "recommendation": "Bağlantının gerçek hedefini doğrulamadan açmayın."
    },

    "Bağlantıda şüpheli anahtar kelime": {
        "why": "Login, verify, account ve benzeri kelimeler sahte giriş sayfalarında sık kullanılabilir.",
        "recommendation": "Alan adını dikkatlice kontrol edin ve resmi siteyle karşılaştırın."
    },

    "Bağlantıda yanıltıcı @ karakteri": {
        "why": "@ karakteri bazı bağlantılarda gerçek hedef adresini gizlemek için kötüye kullanılabilir.",
        "recommendation": "URL'nin gerçek alan adını dikkatlice kontrol edin."
    },

    "Punycode alan adı kullanımı": {
        "why": "Punycode gerçek markalara benzeyen sahte alan adları oluşturmak için kullanılabilir.",
        "recommendation": "Alan adını resmi adresle karşılaştırın."
    },

    "Aşırı uzun bağlantı": {
        "why": "Aşırı uzun bağlantılar gerçek alan adını veya yönlendirmeleri gizleyebilir.",
        "recommendation": "Bağlantının alan adını dikkatlice inceleyin."
    },
}


def explain_risks(detected_risks):
    details = []

    for risk in detected_risks:
        explanation = RISK_EXPLANATIONS.get(
            risk,
            {
                "why": "Bu özellik güvenlik açısından şüpheli olabilir.",
                "recommendation": "İşlem yapmadan önce kaynağı doğrulayın."
            }
        )

        details.append({
            "risk": risk,
            "why": explanation["why"],
            "recommendation": explanation["recommendation"]
        })

    return details