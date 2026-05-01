# Historias de Usuario
## Sistema de Clasificacion Automatica de Tickets

---

## HU-001: Envio de ticket por parte del usuario

**Como** usuario con un problema
**Quiero** poder enviar un ticket describiendo mi situacion
**Para** recibir ayuda del equipo de soporte

### Criterios de aceptacion
- El usuario puede enviar un titulo y descripcion del problema
- El sistema confirma la recepcion del ticket con un ID unico
- El ticket queda registrado con estado OPEN
- El tiempo de respuesta del endpoint es menor a 2 segundos

---

## HU-002: Clasificacion automatica del ticket

**Como** sistema de IA
**Quiero** clasificar automaticamente cada ticket recibido
**Para** dirigirlo al equipo correcto sin intervencion humana

### Criterios de aceptacion
- El modelo clasifica el ticket en: Billing, Technical Support, Cancellations, Sales, General
- La clasificacion se realiza con una confianza mayor al 60%
- El resultado se almacena en la base de datos
- El proceso es asincrono y no bloquea la respuesta al usuario

---

## HU-003: Asignacion de prioridad automatica

**Como** agente de soporte
**Quiero** que cada ticket tenga una prioridad asignada automaticamente
**Para** atender primero los casos mas urgentes

### Criterios de aceptacion
- El sistema asigna prioridad: HIGH, MEDIUM o LOW
- Los tickets con estado del sistema caido se marcan como HIGH
- Los tickets de consultas generales se marcan como LOW
- La prioridad es visible al consultar el ticket

---

## HU-004: Consulta de tickets

**Como** agente de soporte
**Quiero** poder consultar todos los tickets y sus detalles
**Para** gestionar la cola de atencion

### Criterios de aceptacion
- Se puede obtener la lista completa de tickets
- Se puede consultar un ticket por su ID
- Cada ticket muestra: id, titulo, descripcion, estado, categoria IA, prioridad IA, confianza y fecha
- El endpoint retorna 404 si el ticket no existe

---

## HU-005: Escalabilidad del sistema

**Como** administrador del sistema
**Quiero** que el sistema escale automaticamente ante alta demanda
**Para** garantizar disponibilidad en momentos de alto trafico

### Criterios de aceptacion
- El sistema tiene minimo 2 replicas de cada servicio
- El HPA escala automaticamente hasta 5 replicas al 70% de CPU
- El sistema soporta multiples solicitudes simultaneas
- La base de datos mantiene consistencia bajo carga

---

## HU-006: Monitoreo del pipeline CI/CD

**Como** desarrollador
**Quiero** que cada cambio en el codigo ejecute pruebas automaticamente
**Para** detectar errores antes de llegar a produccion

### Criterios de aceptacion
- Cada push a main ejecuta el pipeline de GitHub Actions
- El pipeline entrena los modelos ML/DL
- El pipeline ejecuta las 12 pruebas automaticas
- El pipeline construye las imagenes Docker
- Si alguna prueba falla, el despliegue se detiene
