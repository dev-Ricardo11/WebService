# Credit Limit Validation Web Service

Web service en Python para validar límites de crédito de clientes mediante peticiones XML.

## Características

- API REST con FastAPI
- Procesamiento de peticiones XML (CreditLimitRQ)
- Validación de límites de crédito
- Almacenamiento en base de datos Supabase
- Respuestas en formato XML (CreditLimitRS)

## Requisitos

- Python 3.8 o superior
- Cuenta de Supabase (ya configurada)

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
```

Editar el archivo `.env` con tus credenciales de Supabase.

3. Ejecutar el servicio:
```bash
python app.py
```

El servicio estará disponible en `http://localhost:8000`

## Endpoints

### POST /validateCreditLimit

Valida el límite de crédito de un cliente.

**Request (XML):**
```xml
<CreditLimitRQ>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <Name>Pedro vargas</Name>
  <locValidacion>AAAKDJ3</locValidacion>
  <value>450000</value>
  <Currency>COP</Currency>
  <product>AIR</product>
  <description>Compra de boleto aereo</description>
  <paymentType>CASH</paymentType>
  <mailUser>pedro@ts.cl</mailUser>
</CreditLimitRQ>
```

**Response (XML):**
```xml
<CreditLimitRS>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <status>OK</status>
  <Message>Transaccion aprobada</Message>
</CreditLimitRS>
```

### GET /health

Verifica el estado del servicio.

## Reglas de Validación

1. **Límite de crédito total**: 1,000,000 (configurable)
2. **Transacciones con tarjeta de crédito**: Máximo 500,000
3. Se valida el total de transacciones pendientes del cliente

## Estructura del Proyecto

```
.
├── app.py              # Aplicación principal FastAPI
├── database.py         # Gestión de base de datos Supabase
├── xml_processor.py    # Procesamiento de XML
├── requirements.txt    # Dependencias Python
├── .env.example        # Ejemplo de variables de entorno
└── data/              # Ejemplos XML
    ├── creditlimitrq.xml
    └── creditlimitrs.xml
```

## Pruebas con cURL

```bash
curl -X POST http://localhost:8000/validateCreditLimit \
  -H "Content-Type: application/xml" \
  -d @data/creditlimitrq.xml
```
