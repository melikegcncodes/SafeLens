from analyzers.message_analyzer import analyze_message
from analyzers.url_analyzer import analyze_urls
from services.risk_engine import calculate_risk


print("\n🛡️ SafeLens - Phishing & Scam Detector")
print("---------------------------------------")

message = input("\nAnaliz etmek istediğiniz mesajı girin:\n> ")

message_risks = analyze_message(message)
url_risks = analyze_urls(message)

detected_risks = message_risks + url_risks

result = calculate_risk(detected_risks)

print("\n--- SafeLens Analysis ---")
print(f"Risk Score: {result['score']}/100")
print(f"Risk Level: {result['level']}")

if detected_risks:
    print("\nTespit edilen riskler:")

    for risk in detected_risks:
        print(f"- {risk}")
else:
    print("\nBelirgin bir risk tespit edilmedi.")

print("\n-------------------------")