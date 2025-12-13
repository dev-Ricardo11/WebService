# Inicio Rápido - Web Service de Validación de Límite de Crédito

## Pasos para Ejecutar el Servicio

### 1. Verificar Python

Asegúrate de tener Python 3.8 o superior instalado:

```bash
python --version
```

### 2. Configurar Variables de Entorno

Asegúrate de configurar la base de datos PostgreSQL local y actualizar el archivo `.env`.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Iniciar el Servicio

**Opción A - Script automático:**
```bash
./start_service.sh
```

**Opción B - Comando directo:**
```bash
python -m uvicorn app:app --reload
```

El servicio estará disponible en: `http://localhost:8000`

### 5. Verificar que Funciona

Abre en tu navegador: `http://localhost:8000/health`

Deberías ver:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-12T...",
  "database": "connected"
}
```

## Solución de Problemas

### Error: "Database error"

Verifica que el servicio de PostgreSQL esté corriendo y las credenciales en `.env` sean correctas.
## Probar el Web Service

### Opción 1 - Script de Prueba Automático

```bash
python test_service.py
```

### Opción 2 - Usando cURL

```bash
curl -X POST http://localhost:8000/validateCreditLimit \
  -H "Content-Type: application/xml" \
  -d @data/creditlimitrq.xml
```

### Opción 3 - Usando Postman

1. Método: `POST`
2. URL: `http://localhost:8000/validateCreditLimit`
3. Headers: `Content-Type: application/xml`
4. Body (raw): Copiar el contenido de `data/creditlimitrq.xml`

## Ejemplo de Respuesta Exitosa

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CreditLimitRS>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <status>OK</status>
  <Message>Transaccion aprobada</Message>
</CreditLimitRS>
```

## Ejemplo de Respuesta Rechazada

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CreditLimitRS>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <status>NO-OK</status>
  <Message>El limite de credito ha sido excedido...</Message>
</CreditLimitRS>
```

## Estructura del Request XML

```xml
<CreditLimitRQ>
  <CodeClientBackOffice>6252</CodeClientBackOffice>
  <CodeClientOBT>627</CodeClientOBT>
  <Name>Pedro Vargas</Name>
  <locValidacion>AAAKDJ3</locValidacion>
  <value>450000</value>
  <Currency>COP</Currency>
  <product>AIR</product>                    <!-- AIR|CAR|HOTEL|OTHER -->
  <description>Compra de boleto aereo</description>
  <paymentType>CASH</paymentType>            <!-- TC|CASH -->
  <mailUser>pedro@ts.cl</mailUser>
</CreditLimitRQ>
```

## Casos de Uso Comunes

### 1. Validar Compra de Boleto Aéreo

```xml
<product>AIR</product>
<value>450000</value>
<paymentType>CASH</paymentType>
```

### 2. Validar Reserva de Hotel

```xml
<product>HOTEL</product>
<value>350000</value>
<paymentType>TC</paymentType>
```

### 3. Validar Alquiler de Auto

```xml
<product>CAR</product>
<value>200000</value>
<paymentType>CASH</paymentType>
```


Verifica que las credenciales en `.env` sean correctas y que tengas acceso a Internet.

### Puerto 8000 Ya en Uso

Cambia el puerto en `app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Próximos Pasos

- Revisa `README.md` para documentación completa
- Lee `CONFIGURACION.md` para personalizar las reglas de validación
- Consulta los logs en la base de datos para auditoría

## Soporte

Para más información sobre el flujo de validación, consulta el diagrama `limitecredito.png`
