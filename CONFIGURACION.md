# Guía de Configuración y Despliegue

## Configuración de Variables de Entorno

El servicio requiere las siguientes variables de entorno configuradas en el archivo `.env`:

```
SUPABASE_URL=tu_url_de_supabase
SUPABASE_ANON_KEY=tu_clave_anonima_de_supabase
```

### Obtener las Credenciales de Supabase

La base de datos ya está configurada. Las credenciales están disponibles en el archivo `.env` del proyecto.

## Estructura de la Base de Datos

La tabla `credit_limit_rq` almacena todas las peticiones de validación:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_credit_limit_rq | SERIAL | ID único de la petición |
| code_client_backoffice | VARCHAR(20) | Código del cliente en backoffice |
| code_client_obt | VARCHAR(20) | Código del cliente en OBT |
| name | VARCHAR(200) | Nombre del cliente |
| loc_validacion | VARCHAR(10) | Localizador de reserva |
| value | DECIMAL(15,2) | Valor de la transacción |
| currency | VARCHAR(3) | Moneda (COP, USD, etc.) |
| product | VARCHAR(10) | Tipo de producto (AIR, CAR, HOTEL, OTHER) |
| description | VARCHAR(300) | Descripción de la transacción |
| payment_type | VARCHAR(10) | Tipo de pago (TC, CASH) |
| mail_user | VARCHAR(100) | Email del usuario |
| status | VARCHAR(10) | Estado (OK, NO-OK, PENDING) |
| message_validation | VARCHAR(300) | Mensaje de validación |
| created_at | TIMESTAMPTZ | Fecha de creación |
| updated_at | TIMESTAMPTZ | Fecha de actualización |

## Reglas de Negocio

### 1. Límite de Crédito Total

El servicio valida que el total de transacciones pendientes más la nueva transacción no exceda el límite de crédito configurado (por defecto: 1,000,000).

```python
CREDIT_LIMIT = 1000000.0
```

### 2. Límite para Tarjetas de Crédito

Las transacciones con tarjeta de crédito (`paymentType=TC`) tienen un límite máximo de 500,000.

### 3. Validación de Transacciones Pendientes

El sistema suma todas las transacciones con `status=PENDING` del cliente para calcular el crédito disponible.

## Flujo de Procesamiento

1. **Recepción**: El servicio recibe un XML `CreditLimitRQ`
2. **Parsing**: Se extrae la información del XML
3. **Almacenamiento**: Se guarda en BD con status PENDING
4. **Validación**: Se aplican las reglas de negocio
5. **Actualización**: Se actualiza el status (OK o NO-OK)
6. **Respuesta**: Se genera y retorna el XML `CreditLimitRS`

## Personalización

### Modificar Límites de Crédito

Editar en `app.py`, función `validate_credit_limit_logic()`:

```python
CREDIT_LIMIT = 2000000.0  # Nuevo límite
```

### Agregar Nuevas Reglas de Validación

Agregar lógica adicional en la función `validate_credit_limit_logic()`:

```python
def validate_credit_limit_logic(request_data: dict) -> dict:
    # Reglas existentes...

    # Nueva regla personalizada
    if request_data.get('product') == 'HOTEL' and value > 800000:
        return {
            'status': 'NO-OK',
            'message': 'Las reservas de hotel no pueden exceder 800,000'
        }

    # Más reglas...
```

## Monitoreo y Logs

El servicio registra todas las transacciones en la base de datos, permitiendo:

- Auditoría completa de validaciones
- Análisis de patrones de consumo
- Reportes de crédito por cliente
- Seguimiento de transacciones rechazadas

## Consultas Útiles

### Ver todas las transacciones de un cliente:

```sql
SELECT * FROM credit_limit_rq
WHERE code_client_backoffice = '6252'
ORDER BY created_at DESC;
```

### Ver transacciones pendientes:

```sql
SELECT code_client_backoffice, name, SUM(value) as total_pending
FROM credit_limit_rq
WHERE status = 'PENDING'
GROUP BY code_client_backoffice, name;
```

### Ver transacciones rechazadas:

```sql
SELECT * FROM credit_limit_rq
WHERE status = 'NO-OK'
ORDER BY created_at DESC;
```

## Seguridad

- Row Level Security (RLS) está habilitado en la tabla
- Solo usuarios autenticados pueden acceder a los datos
- Las credenciales deben mantenerse en el archivo `.env` (no versionado)
