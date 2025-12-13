import requests
import xml.etree.ElementTree as ET

def test_validate_credit_limit():
    url = "http://localhost:8000/validateCreditLimit"

    xml_request = """<?xml version="1.0" encoding="UTF-8"?>
<CreditLimitRQ>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <Name>Pedro Vargas</Name>
  <locValidacion>AAAKDJ3</locValidacion>
  <value>450000</value>
  <Currency>COP</Currency>
  <product>AIR</product>
  <description>Compra de boleto aereo</description>
  <paymentType>CASH</paymentType>
  <mailUser>pedro@ts.cl</mailUser>
</CreditLimitRQ>"""

    headers = {'Content-Type': 'application/xml'}

    print("Enviando peticion al web service...")
    print(f"URL: {url}")
    print(f"\nXML Request:\n{xml_request}")

    try:
        response = requests.post(url, data=xml_request, headers=headers)

        print(f"\nEstado de respuesta: {response.status_code}")
        print(f"\nXML Response:\n{response.text}")

        if response.status_code == 200:
            root = ET.fromstring(response.text)
            status = root.find('status').text
            message = root.find('Message').text

            print(f"\nStatus: {status}")
            print(f"Message: {message}")

    except Exception as e:
        print(f"\nError: {str(e)}")

def test_health_check():
    url = "http://localhost:8000/health"

    print("\nVerificando estado del servicio...")

    try:
        response = requests.get(url)
        print(f"Estado: {response.status_code}")
        print(f"Respuesta: {response.json()}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("=== Test del Web Service de Validacion de Credito ===\n")

    test_health_check()

    print("\n" + "="*50 + "\n")

    test_validate_credit_limit()
