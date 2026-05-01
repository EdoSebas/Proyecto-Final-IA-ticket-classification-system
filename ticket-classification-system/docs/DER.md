# DER - Diagrama Entidad-Relacion
## Sistema de Clasificacion Automatica de Tickets

## Entidad: Ticket

| Campo | Tipo | Restriccion | Descripcion |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador unico del ticket |
| title | VARCHAR(255) | NOT NULL | Titulo del problema |
| description | TEXT | NOT NULL | Descripcion detallada |
| status | VARCHAR(50) | DEFAULT OPEN | Estado: OPEN, IN_PROGRESS, CLOSED |
| ai_category | VARCHAR(100) | NULLABLE | Categoria asignada por IA |
| ai_priority | VARCHAR(50) | NULLABLE | Prioridad asignada por IA: HIGH, MEDIUM, LOW |
| ai_confidence | FLOAT | NULLABLE | Nivel de confianza del modelo (0.0 - 1.0) |
| created_at | DATETIME | DEFAULT NOW() | Fecha y hora de creacion |

## Representacion visual
## Valores permitidos

### status
- OPEN: Ticket recien creado
- IN_PROGRESS: Ticket siendo atendido
- CLOSED: Ticket resuelto

### ai_category
- Billing
- Technical Support
- Cancellations
- Sales
- General

### ai_priority
- HIGH: Prioridad alta
- MEDIUM: Prioridad media
- LOW: Prioridad baja

## Flujo de datos
