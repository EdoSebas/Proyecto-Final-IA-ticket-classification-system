# Documentacion de Endpoints
## Ticket Service API v1.0.0

Base URL: http://localhost:9090

---

## POST /tickets/

Crea un nuevo ticket de soporte. El sistema lo clasifica automaticamente con IA.

### Request

**Headers**
**Body**
```json
{
  "title": "No puedo acceder a mi cuenta",
  "description": "Desde ayer no puedo iniciar sesion, me aparece error 401"
}
```

| Campo | Tipo | Requerido | Descripcion |
|-------|------|-----------|-------------|
| title | string | Si | Titulo corto del problema (max 255 chars) |
| description | string | Si | Descripcion detallada del problema |

### Response 201 Created

```json
{
  "id": 1,
  "title": "No puedo acceder a mi cuenta",
  "description": "Desde ayer no puedo iniciar sesion, me aparece error 401",
  "status": "OPEN",
  "ai_category": null,
  "ai_priority": null,
  "ai_confidence": null,
  "created_at": "2026-04-30T22:00:00"
}
```

> Nota: Los campos ai_category, ai_priority y ai_confidence se rellenan de forma asincrona por el ai-service via Kafka.

### Response 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## GET /tickets/

Retorna la lista de todos los tickets registrados.

### Query Parameters

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| skip | integer | 0 | Numero de registros a omitir |
| limit | integer | 100 | Numero maximo de registros a retornar |

### Ejemplo
### Response 200 OK

```json
[
  {
    "id": 1,
    "title": "No puedo acceder a mi cuenta",
    "description": "Desde ayer no puedo iniciar sesion",
    "status": "OPEN",
    "ai_category": "Technical Support",
    "ai_priority": "HIGH",
    "ai_confidence": 0.9234,
    "created_at": "2026-04-30T22:00:00"
  }
]
```

---

## GET /tickets/{ticket_id}

Retorna el detalle de un ticket especifico.

### Path Parameters

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| ticket_id | integer | ID unico del ticket |

### Ejemplo
### Response 200 OK

```json
{
  "id": 1,
  "title": "No puedo acceder a mi cuenta",
  "description": "Desde ayer no puedo iniciar sesion",
  "status": "OPEN",
  "ai_category": "Technical Support",
  "ai_priority": "HIGH",
  "ai_confidence": 0.9234,
  "created_at": "2026-04-30T22:00:00"
}
```

### Response 404 Not Found

```json
{
  "detail": "Ticket not found"
}
```

---

## Categorias posibles (ai_category)

| Categoria | Descripcion |
|-----------|-------------|
| Billing | Problemas de facturacion, cobros, pagos |
| Technical Support | Errores tecnicos, fallas del sistema |
| Cancellations | Solicitudes de cancelacion o baja |
| Sales | Consultas comerciales, planes, precios |
| General | Consultas generales o sin categoria clara |

## Prioridades posibles (ai_priority)

| Prioridad | Descripcion |
|-----------|-------------|
| HIGH | Urgente, afecta operacion del usuario |
| MEDIUM | Importante pero no critico |
| LOW | Consulta o solicitud no urgente |
