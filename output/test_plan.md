# Plan de Pruebas — API Alta de Envío (AltaOrden)
**Versión:** 1.0  
**Fecha:** 2025-07  
**Empresa:** Andreani  
**Autor:** QA Automation  
**Estado:** Borrador

---

## Tabla de Contenidos

1. [Objetivo](#1-objetivo)
2. [Alcance](#2-alcance)
3. [Fuera de Alcance](#3-fuera-de-alcance)
4. [Entorno y Configuración](#4-entorno-y-configuración)
5. [Estrategia de Pruebas](#5-estrategia-de-pruebas)
6. [Criterios de Entrada y Salida](#6-criterios-de-entrada-y-salida)
7. [Casos de Prueba](#7-casos-de-prueba)
8. [Áreas de Riesgo](#8-áreas-de-riesgo)
9. [Brechas de Cobertura](#9-brechas-de-cobertura)
10. [Métricas y Reportes](#10-métricas-y-reportes)

---

## 1. Objetivo

Validar el correcto funcionamiento del endpoint `POST /api/v1/AltaOrden` del servicio **Alta de Pre-envíos de Andreani**, asegurando:

- Que el endpoint acepte y procese correctamente solicitudes válidas ("camino feliz").
- Que rechace de manera apropiada (con códigos HTTP y mensajes de error descriptivos) solicitudes mal formadas, con datos inválidos o incompletos.
- Que no exponga vulnerabilidades de seguridad ante entradas maliciosas o credenciales inválidas/ausentes.
- Que responda dentro de los umbrales de tiempo aceptables para el negocio.
- Que el contrato de la API sea compatible con el esquema definido (contract testing).

---

## 2. Alcance

| Ítem | Incluido |
|------|----------|
| Endpoint `POST https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar/api/v1/AltaOrden` | ✅ |
| Contratos disponibles: `351002270`, `351002665` | ✅ |
| Autenticación vía Cookie | ✅ |
| Validación de esquema del cuerpo de la solicitud | ✅ |
| Validaciones funcionales de negocio (bultos, destinatario, etc.) | ✅ |
| Pruebas de seguridad básica (inyección, XSS, autenticación) | ✅ |
| Prueba de línea base de rendimiento | ✅ |
| Pruebas de integración con sistemas downstream (ERP, roteo, etc.) | ⚠️ Parcial |
| Pruebas de carga/estrés sostenidas | ❌ |
| Endpoints de consulta, cancelación o modificación de envíos | ❌ |

---

## 3. Fuera de Alcance

- Pruebas de UI o portales web.
- Pruebas sobre ambientes de producción.
- Validación de procesos físicos de logística (ruteo, despacho, entrega).
- Pruebas de escalabilidad con herramientas de carga (JMeter, Gatling) — se recomienda en una fase posterior.
- Integración con sistemas de facturación o CRM.

---

## 4. Entorno y Configuración

| Parámetro         | Valor                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------|
| Ambiente          | QA                                                                                          |
| Base URL          | `https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar`                          |
| Endpoint          | `/api/v1/AltaOrden`                                                                         |
| Método HTTP       | `POST`                                                                                      |
| Content-Type      | `application/json`                                                                          |
| Autenticación     | Cookie: `60bd27fe9c81a15e11372fd76131481e=105acb781b8c7e7af0905eaf8b518703`                |
| Contratos válidos | `351002270`, `351002665`                                                                    |
| Herramientas      | Python 3.10+, pytest 7+, requests, pytest-html, pytest-json-report                         |

> ⚠️ **Nota:** Las cookies de autenticación tienen tiempo de expiración. Verificar vigencia antes de ejecutar la suite.

---

## 5. Estrategia de Pruebas

### 5.1 Tipos de Prueba

```
┌─────────────────────┬────────────────────────────────────────────────────────────────┐
│ Tipo                │ Descripción                                                    │
├─────────────────────┼────────────────────────────────────────────────────────────────┤
│ Funcional           │ Verificar que el endpoint cumpla las reglas de negocio         │
│ Negativo            │ Validar respuestas ante entradas incorrectas o faltantes       │
│ Seguridad           │ Probar ausencia de auth, inyección SQL, XSS, datos sensibles   │
│ Borde (Edge Case)   │ Valores límite numéricos, arrays vacíos, strings extremos      │
│ Contrato            │ Validar que la respuesta respete el esquema JSON prometido     │
│ Rendimiento Baseline│ Tiempo de respuesta < 3000ms bajo carga unitaria               │
│ Integración         │ Flujo completo con dos contratos distintos y destinos reales   │
└─────────────────────┴────────────────────────────────────────────────────────────────┘
```

### 5.2 Prioridades

- **P1 – Crítico**: Camino feliz, autenticación, campos obligatorios.
- **P2 – Alto**: Validación de formatos, múltiples bultos, contratos.
- **P3 – Medio**: Casos de borde numéricos, destinatarios múltiples.
- **P4 – Bajo**: Seguridad ofensiva básica (inyección, XSS), rendimiento.

### 5.3 Enfoque de Automatización

- Framework: **pytest + requests** (Python).
- Organización por marcadores: `@pytest.mark.functional`, `@pytest.mark.negative`, `@pytest.mark.security`, `@pytest.mark.edge_case`.
- Los tests están habilitados únicamente cuando la variable de entorno `RUN_LIVE_TESTS=1` está definida, para evitar ejecuciones accidentales contra el ambiente QA.
- Reportes generados con `pytest-html` y `pytest-json-report`.

---

## 6. Criterios de Entrada y Salida

### Criterios de Entrada (para comenzar a ejecutar)
- El ambiente QA está activo y accesible.
- La cookie de autenticación es válida.
- Al menos un contrato válido (`351002270` ó `351002665`) está operativo.
- Los casos de prueba fueron revisados y aprobados por el equipo.

### Criterios de Salida (para considerar la prueba completa)
- 100% de los casos P1 ejecutados y pasando.
- ≥ 90% de los casos P2 ejecutados.
- Todos los defectos P1 reportados en el sistema de tracking.
- Reporte HTML generado y entregado.

---

## 7. Casos de Prueba

### Leyenda de Columnas
- **ID**: Identificador único del caso.
- **Nombre**: Nombre corto descriptivo.
- **Categoría**: `Funcional` | `Negativo` | `Seguridad` | `Borde` | `Rendimiento` | `Contrato`.
- **Descripción**: Qué se valida y por qué.
- **Entrada (Δ)**: Solo se documentan los campos que difieren del payload base válido.
- **Resultado Esperado**: Comportamiento esperado del sistema.
- **Prioridad**: P1–P4.

---

### TC01 — Camino Feliz con Contrato 351002270

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC01 |
| **Nombre**  | Happy Path – Contrato 351002270, origen Tigre, destino Avellaneda |
| **Categoría** | Funcional |
| **Descripción** | Verificar que una solicitud completamente válida con el contrato `351002270`, origen postal en Tigre (CP 1648) y destino en Avellaneda (CP 1870), con 1 bulto de 1 kg y dimensiones 20×20×20 cm, sea aceptada exitosamente. |
| **Entrada** | `contrato: "351002270"`, origen CP 1648 (Tigre), destino CP 1870 (Avellaneda), `bultos[0].kilos: 1`, `bultos[0].largocm: 20`, `valoracobrar: 1000` |
| **Resultado Esperado** | HTTP 200 o 201. Cuerpo con número de envío (`numerodeenvio`) generado. Sin errores de validación. |
| **Prioridad** | P1 |

---

### TC02 — Camino Feliz con Contrato 351002665 e idpedido

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC02 |
| **Nombre**  | Happy Path – Contrato 351002665, origen Ezeiza, destino La Plata, con idpedido |
| **Categoría** | Funcional |
| **Descripción** | Verificar el flujo exitoso usando el segundo contrato disponible, origen en aeropuerto de Ezeiza (CP 1802), destino en La Plata (CP 1900), bulto de 0.06 kg, e `idpedido="bg-test-tool-1223"` para trazabilidad. |
| **Entrada** | `contrato: "351002665"`, origen CP 1802, destino CP 1900, `bultos[0].kilos: 0.06`, `idpedido: "bg-test-tool-1223"` |
| **Resultado Esperado** | HTTP 200 o 201. Respuesta con identificador de orden creada. El `idpedido` debe poder recuperarse o estar reflejado en la respuesta. |
| **Prioridad** | P1 |

---

### TC03 — Bultos Vacíos (Array Vacío)

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC03 |
| **Nombre**  | Sin bultos – array vacío |
| **Categoría** | Negativo |
| **Descripción** | Un envío sin bultos no tiene sentido logístico. El sistema debe rechazarlo. Valida que la API no acepte `bultos: []`. |
| **Entrada** | `bultos: []` (array vacío) |
| **Resultado Esperado** | HTTP 400 o 422. Mensaje de error indicando que se requiere al menos un bulto. |
| **Prioridad** | P1 |

---

### TC04 — Email de Remitente con Formato Inválido

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC04 |
| **Nombre**  | Email inválido en remitente |
| **Categoría** | Negativo |
| **Descripción** | Verificar que la API valide el formato RFC 5321 del campo `remitente.email`. Un valor sin arroba ni dominio debe ser rechazado. |
| **Entrada** | `remitente.email: "no-es-un-email"` |
| **Resultado Esperado** | HTTP 400 o 422. Mensaje de error indicando formato de email inválido. |
| **Prioridad** | P2 |

---

### TC05 — Dos Bultos en el Array

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC05 |
| **Nombre**  | Múltiples bultos – dos bultos válidos |
| **Categoría** | Funcional |
| **Descripción** | Verificar que la API maneje correctamente un envío con más de un bulto, calculando el peso y volumen total correctamente. |
| **Entrada** | `bultos: [bulto1(1kg, 20×20×20), bulto2(2kg, 30×30×30)]` (payload base con 2 bultos válidos) |
| **Resultado Esperado** | HTTP 200 o 201. Respuesta indicando creación exitosa con ambos bultos registrados. |
| **Prioridad** | P2 |

---

### TC06 — Campo `contrato` Ausente

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC06 |
| **Nombre**  | Campo contrato faltante |
| **Categoría** | Negativo |
| **Descripción** | El contrato es un campo de negocio crítico que identifica el acuerdo comercial. Sin él, el sistema no puede procesar el envío. |
| **Entrada** | Payload sin campo `contrato` |
| **Resultado Esperado** | HTTP 400 o 422. Error indicando que `contrato` es requerido. |
| **Prioridad** | P1 |

---

### TC07 — `origen.postal.codigopostal` Ausente

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC07 |
| **Nombre**  | Código postal de origen faltante |
| **Categoría** | Negativo |
| **Descripción** | Sin código postal de origen, el sistema de ruteo no puede calcular la ruta del envío. Debe ser rechazado. |
| **Entrada** | `origen.postal.codigopostal: ""` o campo ausente |
| **Resultado Esperado** | HTTP 400 o 422. Mensaje de error descriptivo referenciando el campo faltante. |
| **Prioridad** | P2 |

---

### TC08 — Array `destinatario` Ausente

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC08 |
| **Nombre**  | Destinatario ausente |
| **Categoría** | Negativo |
| **Descripción** | Sin destinatario no es posible completar el envío. Verificar que la API requiera al menos un destinatario. |
| **Entrada** | Payload sin campo `destinatario` (o `destinatario: null`) |
| **Resultado Esperado** | HTTP 400 o 422. Error indicando que el destinatario es requerido. |
| **Prioridad** | P1 |

---

### TC09 — Sin Cookie de Autenticación

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC09 |
| **Nombre**  | Solicitud sin cookie de autenticación |
| **Categoría** | Seguridad |
| **Descripción** | Verificar que la API no permita acceso sin credenciales. Un atacante sin cookie no debe poder crear envíos. |
| **Entrada** | Payload válido (TC01) **sin** encabezado `Cookie` |
| **Resultado Esperado** | HTTP 401 (Unauthorized) o 403 (Forbidden). Sin datos de envío expuestos. |
| **Prioridad** | P1 |

---

### TC10 — Cookie de Autenticación Inválida/Expirada

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC10 |
| **Nombre**  | Cookie inválida o expirada |
| **Categoría** | Seguridad |
| **Descripción** | Verificar que tokens adulterados o expirados sean rechazados correctamente sin revelar información interna. |
| **Entrada** | Cookie: `60bd27fe9c81a15e11372fd76131481e=INVALIDO_TOKEN_FALSO_9999` |
| **Resultado Esperado** | HTTP 401 o 403. Sin stack trace ni información de sistema en la respuesta. |
| **Prioridad** | P1 |

---

### TC11 — Inyección SQL en `remitente.nombrecompleto`

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC11 |
| **Nombre**  | SQL Injection en nombre del remitente |
| **Categoría** | Seguridad |
| **Descripción** | Verificar que la API sanitice o rechace correctamente inputs con patrones de inyección SQL. No debe producir errores 500 ni alterar datos de base de datos. |
| **Entrada** | `remitente.nombrecompleto: "'; DROP TABLE envios; --"` |
| **Resultado Esperado** | HTTP 400 (rechazo) o HTTP 200/201 con el valor correctamente sanitizado/escapado. **Nunca** HTTP 500. Sin evidencia de ejecución de SQL en respuesta. |
| **Prioridad** | P2 |

---

### TC12 — Payload XSS en `bultos[0].descripcion`

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC12 |
| **Nombre**  | XSS en descripción del bulto |
| **Categoría** | Seguridad |
| **Descripción** | Verificar que scripts maliciosos embebidos en campos de texto no sean ejecutados ni almacenados sin sanitización, previniendo ataques stored-XSS en portales de consulta. |
| **Entrada** | `bultos[0].descripcion: "<script>alert('XSS')</script>"` |
| **Resultado Esperado** | HTTP 400 (rechazo) o 200/201 con el campo sanitizado (e.g., `&lt;script&gt;`). **Nunca** HTTP 500. El script no debe aparecer sin escapar en la respuesta. |
| **Prioridad** | P3 |

---

### TC13 — `valoracobrar` Negativo

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC13 |
| **Nombre**  | Valor a cobrar negativo |
| **Categoría** | Borde |
| **Descripción** | Un monto negativo a cobrar carece de sentido de negocio. La API debe rechazarlo o documentar su comportamiento explícitamente. |
| **Entrada** | `valoracobrar: -500` |
| **Resultado Esperado** | HTTP 400 o 422. Mensaje indicando que el valor no puede ser negativo. |
| **Prioridad** | P2 |

---

### TC14 — Peso de Bulto Extremadamente Alto

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC14 |
| **Nombre**  | Kilos del bulto fuera de límite operativo |
| **Categoría** | Borde |
| **Descripción** | Verificar el comportamiento ante un peso irreal (99,999 kg). Si existe un límite operativo, el sistema debería rechazarlo. Permite documentar el límite real de la API. |
| **Entrada** | `bultos[0].kilos: 99999` |
| **Resultado Esperado** | HTTP 400/422 si existe límite, o 200/201 documentando que no hay validación de límite superior (brecha). |
| **Prioridad** | P3 |

---

### TC15 — Bloque `remitente` Ausente

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC15 |
| **Nombre**  | Remitente ausente en payload |
| **Categoría** | Negativo |
| **Descripción** | Sin información del remitente no puede generarse un envío válido. Verifica que el campo sea requerido. |
| **Entrada** | Payload sin campo `remitente` |
| **Resultado Esperado** | HTTP 400 o 422. Error descriptivo indicando ausencia del remitente. |
| **Prioridad** | P1 |

---

### TC16 — Content-Type Incorrecto (`text/plain`)

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC16 |
| **Nombre**  | Header Content-Type incorrecto |
| **Categoría** | Negativo |
| **Descripción** | Verificar que la API rechace solicitudes que no declaren `application/json`, ya que no puede parsear el cuerpo correctamente. |
| **Entrada** | Header `Content-Type: text/plain`, cuerpo JSON válido |
| **Resultado Esperado** | HTTP 400 o 415 (Unsupported Media Type). |
| **Prioridad** | P3 |

---

### TC17 — `contrato` con String Vacío

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC17 |
| **Nombre**  | Contrato con valor vacío |
| **Categoría** | Negativo |
| **Descripción** | Un contrato vacío `""` es semánticamente inválido aunque el campo esté presente. La API debe distinguir entre campo ausente y campo con valor vacío. |
| **Entrada** | `contrato: ""` |
| **Resultado Esperado** | HTTP 400 o 422. Error indicando contrato inválido o vacío. |
| **Prioridad** | P2 |

---

### TC18 — `contrato` con Valor `null`

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC18 |
| **Nombre**  | Contrato null |
| **Categoría** | Negativo |
| **Descripción** | Similar a TC17 pero usando `null` explícito. Verifica manejo de nulos en campos de tipo string requerido. |
| **Entrada** | `contrato: null` |
| **Resultado Esperado** | HTTP 400 o 422. Mensaje de error. No debe producir NullPointerException (HTTP 500). |
| **Prioridad** | P2 |

---

### TC19 — Múltiples Destinatarios en el Array

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC19 |
| **Nombre**  | Más de un destinatario |
| **Categoría** | Borde |
| **Descripción** | El esquema permite un array de destinatarios. Verificar si la API acepta más de uno y cuál es el comportamiento (¿se usa el primero? ¿se rechaza?). Objetivo: documentar el comportamiento real. |
| **Entrada** | `destinatario: [destinatario1, destinatario2]` (dos destinatarios válidos) |
| **Resultado Esperado** | HTTP 200/201 si se permite, o 400/422 si solo se acepta uno. Documentar comportamiento. |
| **Prioridad** | P3 |

---

### TC20 — Tiempo de Respuesta (Línea Base de Rendimiento)

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC20 |
| **Nombre**  | Performance baseline – tiempo de respuesta |
| **Categoría** | Rendimiento |
| **Descripción** | Verificar que una solicitud válida (TC01) sea respondida en menos de 3000ms bajo condiciones normales de uso (1 solicitud concurrente). Establece la línea base para futuras pruebas de regresión de rendimiento. |
| **Entrada** | Payload idéntico a TC01 |
| **Resultado Esperado** | HTTP 200/201 con tiempo de respuesta total (wall-clock) < 3000ms. |
| **Prioridad** | P2 |

---

### TC21 — Contrato Desconocido

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC21 |
| **Nombre**  | Contrato inexistente en el sistema |
| **Categoría** | Negativo |
| **Descripción** | Usar un número de contrato que no existe en el sistema para verificar que el error sea descriptivo y no exponga información interna. |
| **Entrada** | `contrato: "999999999"` |
| **Resultado Esperado** | HTTP 400, 404 o 422. Mensaje indicando contrato inválido o no encontrado. Sin información de sistema expuesta. |
| **Prioridad** | P2 |

---

### TC22 — Código Postal de Origen Inexistente

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC22 |
| **Nombre**  | Código postal de origen no reconocido |
| **Categoría** | Negativo |
| **Descripción** | Usar un código postal que no existe en la base de datos de Andreani para verificar la respuesta del servicio de geolocalización/ruteo. |
| **Entrada** | `origen.postal.codigopostal: "00000"` |
| **Resultado Esperado** | HTTP 400 o 422 con mensaje de CP no válido. No debe generar error 500 por falla en servicio de ruteo. |
| **Prioridad** | P3 |

---

### TC23 — Cuerpo de Solicitud Vacío

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC23 |
| **Nombre**  | Body vacío (JSON vacío `{}`) |
| **Categoría** | Negativo |
| **Descripción** | Enviar un JSON vacío para verificar el manejo de la falta de todos los campos obligatorios simultáneamente. |
| **Entrada** | `{}` |
| **Resultado Esperado** | HTTP 400 o 422. Lista de campos requeridos faltantes. |
| **Prioridad** | P2 |

---

### TC24 — `bultos[0].kilos` = 0

| Campo       | Detalle |
|-------------|---------|
| **ID**      | TC24 |
| **Nombre**  | Bulto con peso cero |
| **Categoría** | Borde |
| **Descripción** | Un bulto de 0 kg podría ser un error de carga. Verificar si la API rechaza o acepta este valor límite. |
| **Entrada** | `bultos[0].kilos: 0` |
| **Resultado Esperado** | HTTP 400/422 preferiblemente. Documentar si acepta o rechaza. |
| **Prioridad** | P3 |

---

### Resumen de Casos de Prueba

| ID   | Nombre Corto                          | Categoría     | Prioridad |
|------|---------------------------------------|---------------|-----------|
| TC01 | Happy Path – 351002270                | Funcional     | P1        |
| TC02 | Happy Path – 351002665 + idpedido     | Funcional     | P1        |
| TC03 | Bultos vacíos                         | Negativo      | P1        |
| TC04 | Email inválido                        | Negativo      | P2        |
| TC05 | Dos bultos                            | Funcional     | P2        |
| TC06 | Contrato ausente                      | Negativo      | P1        |
| TC07 | CP origen ausente                     | Negativo      | P2        |
| TC08 | Destinatario ausente                  | Negativo      | P1        |
| TC09 | Sin cookie                            | Seguridad     | P1        |
| TC10 | Cookie inválida                       | Seguridad     | P1        |
| TC11 | SQL Injection en remitente            | Seguridad     | P2        |
| TC12 | XSS en descripción de bulto           | Seguridad     | P3        |
| TC13 | valoracobrar negativo                 | Borde         | P2        |
| TC14 | Kilos extremos (99999)                | Borde         | P3        |
| TC15 | Remitente ausente                     | Negativo      | P1        |
| TC16 | Content-Type incorrecto               | Negativo      | P3        |
| TC17 | Contrato string vacío                 | Negativo      | P2        |
| TC18 | Contrato null                         | Negativo      | P2        |
| TC19 | Múltiples destinatarios               | Borde         | P3        |
| TC20 | Performance baseline < 3000ms         | Rendimiento   | P2        |
| TC21 | Contrato inexistente                  | Negativo      | P2        |
| TC22 | CP origen inexistente                 | Negativo      | P3        |
| TC23 | Body vacío                            | Negativo      | P2        |
| TC24 | Bulto kilos = 0                       | Borde         | P3        |

**Total: 24 casos** | P1: 7 | P2: 10 | P3: 7

---

## 8. Áreas de Riesgo

### 8.1 Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| La cookie de autenticación expira durante la ejecución de la suite | Alta | Alto | Renovar la cookie antes de cada ejecución; parametrizar vía variable de entorno |
| El ambiente QA no está disponible (mantenimiento, deploys) | Media | Alto | Coordinación con el equipo de infraestructura; reintentos automáticos en pipeline CI |
| Respuestas HTTP 500 ante inputs no validados (bugs) | Media | Alto | Reporte inmediato al equipo de desarrollo; bloqueo de promoción a producción |
| Cambios de contrato de API sin versionado adecuado (breaking changes) | Baja | Alto | Implementar contract testing con Pact o equivalente |
| Falta de sanitización en campos de texto libre (SQL/XSS) | Media | Alto | Ejecutar TC11 y TC12 en cada ciclo de regresión |

### 8.2 Riesgos de Negocio

| Riesgo | Descripción |
|--------|-------------|
| Duplicación de órdenes | Si el endpoint no es idempotente, reintentos pueden crear envíos duplicados. Se necesita investigar comportamiento con mismo `idpedido`. |
| Validación de contratos activos | Los contratos `351002270` y `351002665` podrían tener restricciones de servicio/cobertura geográfica que generen rechazos válidos. |
| Reglas de negocio no documentadas | Pueden existir validaciones no especificadas (e.g., límites de peso por tipo de servicio, restricciones de zona). |

---

## 9. Brechas de Cobertura

Las siguientes áreas requieren información adicional o casos de prueba extendidos:

| Brecha | Descripción | Acción Recomendada |
|--------|-------------|-------------------|
| **Idempotencia** | No se verifica qué ocurre al enviar el mismo `idpedido` dos veces. | Agregar TC-IDEM-01: POST repetido con mismo idpedido. |
| **Tipos de servicio válidos** | El campo `tiposervicio` acepta cualquier string. No se conocen los valores permitidos. | Solicitar al equipo los valores válidos del catálogo; agregar casos positivos y negativos. |
| **Campo `sucursalclienteid`** | No hay casos que prueben este campo numérico con valor 0 vs. un ID real. | Investigar si 0 es válido o es placeholder. |
| **Coordenadas en origen/destino** | El esquema permite latitud/longitud. No hay casos que usen coordenadas inválidas (out of range). | Agregar TC con lat > 90 y lon > 180. |
| **Webhooks / callbacks** | No se sabe si el alta de orden dispara eventos/webhooks. | Investigar y agregar pruebas de integración asíncrona. |
| **Pruebas de carga** | Solo hay un baseline de 1 req. No hay prueba de 50/100 req concurrentes. | Planificar sprint de performance testing con Locust o k6. |
| **Campos opcionales vacíos** | No hay cobertura explícita para campos opcionales con `null`, `""` o ausentes. | Agregar matrix de casos para campos opcionales. |
| **Campo `fechaentrega`** | No se prueba con fechas pasadas, fechas en formato incorrecto o rango hora inválido. | Agregar TC-FECHA-01 a TC-FECHA-03. |
| **`pagodestino` vs `valoracobrar`** | La relación entre `pagodestino: null` y `valoracobrar > 0` no está probada consistentemente. | Clarificar regla de negocio y agregar casos cruzados. |
| **Autenticación OIDC/JWT** | Si el sistema migra de Cookie a Bearer token, los tests de seguridad quedarán desactualizados. | Monitorear roadmap de seguridad de la API. |

---

## 10. Métricas y Reportes

### KPIs de la Suite

| Métrica | Objetivo |
|---------|----------|
| Cobertura de casos P1 ejecutados | 100% |
| Tasa de éxito general de la suite | ≥ 85% (excluyendo casos documentados como "a definir") |
| Tiempo máximo de ejecución de la suite completa | < 5 minutos |
| Defectos P1 encontrados antes de pasar a producción | 100% |

### Reportes Generados

- `report.html` — Reporte visual con pytest-html.
- `report.json` — Reporte estructurado para integración CI/CD.
- Notificación de fallo en canal de Slack/Teams del equipo QA (a configurar en pipeline).

---

*Documento generado para el proyecto de automatización de pruebas API Andreani — Alta de Pre-envíos.*  
*Revisar y actualizar ante cualquier cambio en el contrato de la API o reglas de negocio.*
