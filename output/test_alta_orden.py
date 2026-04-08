"""
test_alta_orden.py
==================
Suite de pruebas automatizadas para el endpoint POST /api/v1/AltaOrden
de la API de Alta de Pre-envíos de Andreani.

Framework : pytest + requests
Ambiente  : QA  (https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar)
Autor     : QA Automation
Versión   : 1.0

Ejecución
---------
Los tests solo se ejecutan cuando la variable de entorno RUN_LIVE_TESTS=1
está definida, para evitar llamadas accidentales al ambiente QA.

    # Correr toda la suite
    RUN_LIVE_TESTS=1 pytest test_alta_orden.py -v

    # Solo pruebas funcionales
    RUN_LIVE_TESTS=1 pytest test_alta_orden.py -v -m functional

    # Solo pruebas de seguridad
    RUN_LIVE_TESTS=1 pytest test_alta_orden.py -v -m security

    # Con reporte HTML
    RUN_LIVE_TESTS=1 pytest test_alta_orden.py -v --html=report.html --self-contained-html

Dependencias
------------
    pip install pytest requests pytest-html pytest-json-report

Notas de Seguridad
------------------
- La cookie de autenticación se pasa como variable de entorno ANDREANI_COOKIE.
  Si no está definida, se usa el valor de la colección Postman conocida.
  NUNCA commitear credenciales en el repositorio.
- Los tests de inyección SQL y XSS documentan el comportamiento real de la API;
  no lanzan ataques sostenidos.
"""

import copy
import os
import time
import pytest
import requests

# ---------------------------------------------------------------------------
# Configuración: los tests se omiten si RUN_LIVE_TESTS != "1"
# ---------------------------------------------------------------------------
RUN_LIVE = os.environ.get("RUN_LIVE_TESTS", "0") == "1"
SKIP_REASON = (
    "Requiere acceso al ambiente QA de Andreani. "
    "Ejecutar con RUN_LIVE_TESTS=1 para habilitar."
)

# ---------------------------------------------------------------------------
# Marcadores personalizados
# ---------------------------------------------------------------------------
pytestmark = []  # Los marcadores se aplican a nivel de función


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def base_url() -> str:
    """URL base del servicio de Alta de Pre-envíos en ambiente QA."""
    return os.environ.get(
        "ANDREANI_BASE_URL",
        "https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar",
    )


@pytest.fixture(scope="session")
def auth_cookie() -> str:
    """
    Cookie de autenticación para el ambiente QA.
    Se puede sobreescribir con la variable de entorno ANDREANI_COOKIE.
    """
    return os.environ.get(
        "ANDREANI_COOKIE",
        "60bd27fe9c81a15e11372fd76131481e=105acb781b8c7e7af0905eaf8b518703",
    )


@pytest.fixture(scope="session")
def valid_headers(auth_cookie: str) -> dict:
    """
    Headers HTTP válidos para todas las solicitudes autenticadas.
    Incluye Content-Type y Cookie de sesión.
    """
    return {
        "Content-Type": "application/json",
        "Cookie": auth_cookie,
    }


@pytest.fixture(scope="session")
def endpoint(base_url: str) -> str:
    """URL completa del endpoint AltaOrden."""
    return f"{base_url}/api/v1/AltaOrden"


@pytest.fixture
def valid_payload_351002270() -> dict:
    """
    Payload base válido usando el contrato 351002270.
    Origen: Tigre (CP 1648) — Destino: Avellaneda (CP 1870).
    Basado en el escenario 'Happy path' de la colección Postman.
    """
    return {
        "contrato": "351002270",
        "tiposervicio": "AND",
        "sucursalclienteid": 0,
        "origen": {
            "postal": {
                "codigopostal": "1648",
                "calle": "Av. Cazón",
                "numero": "1500",
                "localidad": "Tigre",
                "piso": "",
                "departamento": "",
                "region": "GBA Norte",
                "pais": "AR",
                "casilladecorreo": "",
                "componentesdedireccion": [],
            },
            "sucursal": None,
            "coordenadas": None,
        },
        "destino": {
            "postal": {
                "codigopostal": "1870",
                "calle": "Av. Mitre",
                "numero": "800",
                "localidad": "Avellaneda",
                "piso": "",
                "departamento": "",
                "region": "GBA Sur",
                "pais": "AR",
                "casilladecorreo": "",
                "componentesdedireccion": [],
            },
            "sucursal": None,
            "coordenadas": None,
        },
        "idpedido": "",
        "remitente": {
            "nombrecompleto": "Juan Pérez",
            "email": "juan.perez@empresa.com.ar",
            "documentotipo": "CUIT",
            "documentonumero": "20304050601",
            "telefonos": [],
        },
        "destinatario": [
            {
                "nombrecompleto": "María García",
                "email": "maria.garcia@cliente.com.ar",
                "documentotipo": "CUIT",
                "documentonumero": "27304050602",
                "telefonos": [{"tipo": 2, "numero": "1145678901"}],
            }
        ],
        "remito": {"numeroremito": "REM-001", "complementarios": None},
        "centrodecostos": "CC-001",
        "productoaentregar": "",
        "productoaretirar": "",
        "tipoproducto": "",
        "categoriafacturacion": "",
        "pagodestino": None,
        "valoracobrar": 1000,
        "fechaentrega": {
            "fecha": "",
            "horadesde": "",
            "horahasta": "",
        },
        "codigoverificadordeentrega": "",
        "bultos": [
            {
                "kilos": 1,
                "largocm": 20,
                "altocm": 20,
                "anchocm": 20,
                "volumencm3": 8000,
                "valordeclaradosinimpuestos": 2000000,
                "valordeclaradoconimpuestos": 0,
                "descripcion": "Paquete de prueba",
                "referencias": [{"meta": "orden", "contenido": "ORD-001"}],
                "numerodeenvio": "",
                "valordeclarado": 0,
                "componentes": {"numeroAgrupador": "", "componentesHijos": []},
                "ean": "",
            }
        ],
        "pagopendienteenmostrador": False,
    }


@pytest.fixture
def valid_payload_351002665() -> dict:
    """
    Payload base válido usando el contrato 351002665.
    Origen: Aeropuerto Ezeiza (CP 1802) — Destino: La Plata (CP 1900).
    Incluye idpedido para trazabilidad.
    Basado en el escenario 'otros datos' de la colección Postman.
    """
    return {
        "contrato": "351002665",
        "tiposervicio": "AND",
        "sucursalclienteid": 0,
        "origen": {
            "postal": {
                "codigopostal": "1802",
                "calle": "Autopista Ezeiza-Cañuelas",
                "numero": "1",
                "localidad": "Ezeiza",
                "piso": "",
                "departamento": "",
                "region": "GBA Sur",
                "pais": "AR",
                "casilladecorreo": "",
                "componentesdedireccion": [],
            },
            "sucursal": None,
            "coordenadas": None,
        },
        "destino": {
            "postal": {
                "codigopostal": "1900",
                "calle": "Calle 7",
                "numero": "1000",
                "localidad": "La Plata",
                "piso": "",
                "departamento": "",
                "region": "GBA Sur",
                "pais": "AR",
                "casilladecorreo": "",
                "componentesdedireccion": [],
            },
            "sucursal": None,
            "coordenadas": None,
        },
        "idpedido": "bg-test-tool-1223",
        "remitente": {
            "nombrecompleto": "Carlos López",
            "email": "carlos.lopez@empresa.com.ar",
            "documentotipo": "CUIT",
            "documentonumero": "20405060703",
            "telefonos": [],
        },
        "destinatario": [
            {
                "nombrecompleto": "Ana Rodríguez",
                "email": "ana.rodriguez@cliente.com.ar",
                "documentotipo": "CUIT",
                "documentonumero": "27405060704",
                "telefonos": [{"tipo": 2, "numero": "2214567890"}],
            }
        ],
        "remito": {"numeroremito": "REM-002", "complementarios": None},
        "centrodecostos": "CC-002",
        "productoaentregar": "",
        "productoaretirar": "",
        "tipoproducto": "",
        "categoriafacturacion": "",
        "pagodestino": None,
        "valoracobrar": 0,
        "fechaentrega": {
            "fecha": "",
            "horadesde": "",
            "horahasta": "",
        },
        "codigoverificadordeentrega": "",
        "bultos": [
            {
                "kilos": 0.06,
                "largocm": 10,
                "altocm": 5,
                "anchocm": 5,
                "volumencm3": 250,
                "valordeclaradosinimpuestos": 500,
                "valordeclaradoconimpuestos": 0,
                "descripcion": "Sobre documento",
                "referencias": [],
                "numerodeenvio": "",
                "valordeclarado": 0,
                "componentes": {"numeroAgrupador": "", "componentesHijos": []},
                "ean": "",
            }
        ],
        "pagopendienteenmostrador": False,
    }


# ---------------------------------------------------------------------------
# Helper: deep copy de payload para mutación segura en cada test
# ---------------------------------------------------------------------------
def _clone(payload: dict) -> dict:
    """Retorna una copia profunda del payload para evitar efectos secundarios entre tests."""
    return copy.deepcopy(payload)


# ---------------------------------------------------------------------------
# ✅ PRUEBAS FUNCIONALES
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.functional
def test_tc01_happy_path_contrato_351002270(endpoint, valid_headers, valid_payload_351002270):
    """
    TC01 — Camino feliz con contrato 351002270.

    Verifica que una solicitud completamente válida con contrato 351002270,
    origen en Tigre (CP 1648) y destino en Avellaneda (CP 1870), con 1 bulto
    de 1 kg y valoracobrar=1000, retorne HTTP 2xx y un cuerpo de respuesta
    con información de la orden creada.
    """
    payload = _clone(valid_payload_351002270)

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code in (200, 201), (
        f"[TC01] Se esperaba 2xx pero se obtuvo {response.status_code}. "
        f"Body: {response.text}"
    )
    body = response.json()
    assert body is not None, "[TC01] El cuerpo de la respuesta no debe ser nulo."
    # La API debe retornar algún identificador de la orden/envío
    assert any(
        key in body for key in ("numerodeenvio", "id", "numeroDeEnvio", "ordenId", "data")
    ), f"[TC01] No se encontró identificador de orden en la respuesta: {body}"


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.functional
def test_tc02_happy_path_contrato_351002665_con_idpedido(
    endpoint, valid_headers, valid_payload_351002665
):
    """
    TC02 — Camino feliz con contrato 351002665 e idpedido definido.

    Verifica el flujo exitoso con el segundo contrato disponible, origen en
    Ezeiza (CP 1802), destino en La Plata (CP 1900), bulto de 0.06 kg, e
    idpedido='bg-test-tool-1223' para trazabilidad.
    """
    payload = _clone(valid_payload_351002665)
    assert payload["idpedido"] == "bg-test-tool-1223"

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code in (200, 201), (
        f"[TC02] Se esperaba 2xx pero se obtuvo {response.status_code}. "
        f"Body: {response.text}"
    )
    body = response.json()
    assert body is not None, "[TC02] El cuerpo de la respuesta no debe ser nulo."


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.functional
def test_tc05_dos_bultos(endpoint, valid_headers, valid_payload_351002270):
    """
    TC05 — Dos bultos en el array.

    Verifica que la API acepte correctamente un envío con dos bultos válidos,
    cada uno con distintas dimensiones y pesos, retornando HTTP 2xx.
    """
    payload = _clone(valid_payload_351002270)
    payload["bultos"] = [
        {
            "kilos": 1,
            "largocm": 20,
            "altocm": 20,
            "anchocm": 20,
            "volumencm3": 8000,
            "valordeclaradosinimpuestos": 1000000,
            "valordeclaradoconimpuestos": 0,
            "descripcion": "Primer bulto",
            "referencias": [],
            "numerodeenvio": "",
            "valordeclarado": 0,
            "componentes": {"numeroAgrupador": "", "componentesHijos": []},
            "ean": "",
        },
        {
            "kilos": 2,
            "largocm": 30,
            "altocm": 30,
            "anchocm": 30,
            "volumencm3": 27000,
            "valordeclaradosinimpuestos": 1500000,
            "valordeclaradoconimpuestos": 0,
            "descripcion": "Segundo bulto",
            "referencias": [],
            "numerodeenvio": "",
            "valordeclarado": 0,
            "componentes": {"numeroAgrupador": "", "componentesHijos": []},
            "ean": "",
        },
    ]

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code in (200, 201), (
        f"[TC05] Se esperaba 2xx pero se obtuvo {response.status_code}. "
        f"Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.functional
def test_tc19_multiples_destinatarios(endpoint, valid_headers, valid_payload_351002270):
    """
    TC19 — Más de un destinatario en el array.

    El esquema permite un array de destinatarios. Este test documenta el
    comportamiento real de la API ante dos destinatarios válidos: si acepta
    ambos (2xx) o si solo permite uno (4xx). El test pasa en cualquier caso
    2xx o 4xx, pero falla si devuelve 5xx (error de servidor no esperado).
    """
    payload = _clone(valid_payload_351002270)
    payload["destinatario"] = [
        {
            "nombrecompleto": "Destinatario Uno",
            "email": "dest.uno@empresa.com.ar",
            "documentotipo": "CUIT",
            "documentonumero": "20111222331",
            "telefonos": [{"tipo": 2, "numero": "1100000001"}],
        },
        {
            "nombrecompleto": "Destinatario Dos",
            "email": "dest.dos@empresa.com.ar",
            "documentotipo": "CUIT",
            "documentonumero": "20111222332",
            "telefonos": [{"tipo": 2, "numero": "1100000002"}],
        },
    ]

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code < 500, (
        f"[TC19] La API devolvió error de servidor {response.status_code} "
        f"ante múltiples destinatarios. Body: {response.text}"
    )
    # Documentar comportamiento sin falla binaria
    if response.status_code in (200, 201):
        pytest.skip("[TC19] La API acepta múltiples destinatarios (comportamiento documentado).")
    else:
        pytest.skip(
            f"[TC19] La API rechaza múltiples destinatarios con {response.status_code} "
            f"(comportamiento documentado)."
        )


# ---------------------------------------------------------------------------
# ❌ PRUEBAS NEGATIVAS
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc03_bultos_vacios(endpoint, valid_headers, valid_payload_351002270):
    """
    TC03 — Array de bultos vacío.

    Un envío sin bultos es inválido desde el punto de vista logístico.
    La API debe rechazarlo con HTTP 4xx y un mensaje descriptivo.
    """
    payload = _clone(valid_payload_351002270)
    payload["bultos"] = []

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC03] Se esperaba error 4xx para bultos vacíos pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc04_email_invalido_remitente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC04 — Email de formato inválido en remitente.

    El campo remitente.email debe seguir el formato RFC 5321.
    Un valor como 'no-es-un-email' debe ser rechazado con HTTP 4xx.
    """
    payload = _clone(valid_payload_351002270)
    payload["remitente"]["email"] = "no-es-un-email"

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC04] Se esperaba error 4xx para email inválido pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc06_contrato_ausente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC06 — Campo 'contrato' ausente del payload.

    El contrato es un campo de negocio crítico. Sin él, la API no puede
    determinar el acuerdo comercial y debe rechazar la solicitud con 4xx.
    """
    payload = _clone(valid_payload_351002270)
    del payload["contrato"]

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC06] Se esperaba error 4xx para contrato ausente pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc07_codigopostal_origen_ausente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC07 — Código postal de origen vacío o ausente.

    Sin código postal de origen el sistema de ruteo no puede operar.
    La API debe rechazar la solicitud con HTTP 4xx.
    """
    payload = _clone(valid_payload_351002270)
    payload["origen"]["postal"]["codigopostal"] = ""

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC07] Se esperaba error 4xx para CP origen vacío pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc08_destinatario_ausente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC08 — Campo 'destinatario' ausente del payload.

    Sin destinatario no puede generarse un envío válido.
    La API debe rechazar la solicitud con HTTP 4xx.
    """
    payload = _clone(valid_payload_351002270)
    del payload["destinatario"]

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC08] Se esperaba error 4xx para destinatario ausente pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc15_remitente_ausente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC15 — Bloque 'remitente' ausente del payload.

    Sin información del remitente no puede generarse un envío.
    La API debe rechazar la solicitud con HTTP 4xx y nunca devolver 5xx.
    """
    payload = _clone(valid_payload_351002270)
    del payload["remitente"]

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code != 500, (
        f"[TC15] La API devolvió HTTP 500 (error no controlado) ante remitente ausente. "
        f"Body: {response.text}"
    )
    assert 400 <= response.status_code < 500, (
        f"[TC15] Se esperaba error 4xx para remitente ausente pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc16_content_type_incorrecto(endpoint, valid_headers, valid_payload_351002270):
    """
    TC16 — Content-Type incorrecto (text/plain en lugar de application/json).

    La API no puede parsear un JSON con Content-Type text/plain.
    Se espera HTTP 400 o 415 (Unsupported Media Type).
    """
    payload = _clone(valid_payload_351002270)

    # Sobreescribir Content-Type con valor incorrecto
    wrong_headers = dict(valid_headers)
    wrong_headers["Content-Type"] = "text/plain"

    # Enviar el payload como string (como lo haría un cliente mal configurado)
    import json
    response = requests.post(
        endpoint,
        data=json.dumps(payload),  # data= en lugar de json= para respetar el header manual
        headers=wrong_headers,
        timeout=10,
    )

    assert response.status_code in (400, 415), (
        f"[TC16] Se esperaba 400 o 415 para Content-Type incorrecto pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc17_contrato_string_vacio(endpoint, valid_headers, valid_payload_351002270):
    """
    TC17 — Campo 'contrato' con valor string vacío ("").

    Un contrato vacío es semánticamente inválido aunque el campo esté presente.
    La API debe distinguir entre campo ausente y campo con valor vacío.
    Se espera HTTP 4xx.
    """
    payload = _clone(valid_payload_351002270)
    payload["contrato"] = ""

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC17] Se esperaba error 4xx para contrato vacío pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc18_contrato_null(endpoint, valid_headers, valid_payload_351002270):
    """
    TC18 — Campo 'contrato' con valor null.

    Similar a TC17 pero con null explícito. Verifica manejo de nulos en
    campos de tipo string requerido. Nunca debe producir HTTP 500
    (NullPointerException o similar).
    """
    payload = _clone(valid_payload_351002270)
    payload["contrato"] = None

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code != 500, (
        f"[TC18] La API devolvió HTTP 500 ante contrato null (posible NPE). "
        f"Body: {response.text}"
    )
    assert 400 <= response.status_code < 500, (
        f"[TC18] Se esperaba error 4xx para contrato null pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc21_contrato_inexistente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC21 — Contrato que no existe en el sistema.

    Usar un número de contrato desconocido para verificar que el sistema
    devuelva un error apropiado sin exponer detalles internos del sistema.
    """
    payload = _clone(valid_payload_351002270)
    payload["contrato"] = "999999999"

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC21] Se esperaba error 4xx para contrato inexistente pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )
    # Verificar que no se filtren detalles internos
    body_text = response.text.lower()
    sensitive_keywords = ["stack trace", "exception", "sql", "hibernate", "internal error"]
    for keyword in sensitive_keywords:
        assert keyword not in body_text, (
            f"[TC21] La respuesta de error puede exponer información interna: "
            f"se encontró '{keyword}' en el body."
        )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.negative
def test_tc23_body_vacio(endpoint, valid_headers):
    """
    TC23 — Cuerpo de solicitud con JSON vacío {}.

    Enviar un JSON vacío debe provocar un error 4xx con la lista de campos
    requeridos faltantes o un mensaje descriptivo de validación.
    """
    response = requests.post(endpoint, json={}, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC23] Se esperaba error 4xx para body vacío pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


# ---------------------------------------------------------------------------
# 🔒 PRUEBAS DE SEGURIDAD
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.security
def test_tc09_sin_cookie_autenticacion(endpoint, valid_payload_351002270):
    """
    TC09 — Solicitud sin cookie de autenticación.

    Un atacante sin credenciales no debe poder crear órdenes de envío.
    La API debe rechazar la solicitud con HTTP 401 o 403.
    El cuerpo de la respuesta no debe contener información de órdenes.
    """
    payload = _clone(valid_payload_351002270)

    # Enviar sin header Cookie
    headers_sin_auth = {"Content-Type": "application/json"}

    response = requests.post(
        endpoint, json=payload, headers=headers_sin_auth, timeout=10
    )

    assert response.status_code in (401, 403), (
        f"[TC09] Se esperaba 401 o 403 sin autenticación pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.security
def test_tc10_cookie_invalida(endpoint, valid_payload_351002270):
    """
    TC10 — Cookie de autenticación adulterada/inválida.

    Un token adulterado o expirado debe ser rechazado sin revelar
    información interna del sistema (stack traces, nombres de clases, etc.).
    """
    payload = _clone(valid_payload_351002270)

    headers_cookie_invalida = {
        "Content-Type": "application/json",
        "Cookie": "60bd27fe9c81a15e11372fd76131481e=INVALIDO_TOKEN_FALSO_XXXXXXXXXXX",
    }

    response = requests.post(
        endpoint, json=payload, headers=headers_cookie_invalida, timeout=10
    )

    assert response.status_code in (401, 403), (
        f"[TC10] Se esperaba 401 o 403 con cookie inválida pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )

    # Verificar que no se filtren detalles internos en respuesta de error de auth
    body_text = response.text.lower()
    internal_keywords = ["stack trace", "at com.", "at org.", "caused by", "exception"]
    for keyword in internal_keywords:
        assert keyword not in body_text, (
            f"[TC10] La respuesta de error de autenticación filtra información "
            f"interna (encontrado: '{keyword}')."
        )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.security
def test_tc11_sql_injection_remitente_nombre(endpoint, valid_headers, valid_payload_351002270):
    """
    TC11 — Inyección SQL en el campo remitente.nombrecompleto.

    Verificar que la API sanitice o rechace correctamente un input con
    patrón de inyección SQL clásico. La API no debe devolver HTTP 500
    ni evidencias de ejecución de SQL en la respuesta.

    Patrón probado: "'; DROP TABLE envios; --"
    """
    payload = _clone(valid_payload_351002270)
    payload["remitente"]["nombrecompleto"] = "'; DROP TABLE envios; --"

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    # La API no debe devolver 500 (error de base de datos no controlado)
    assert response.status_code != 500, (
        f"[TC11] La API devolvió HTTP 500 ante input de SQL injection. "
        f"Posible vulnerabilidad. Body: {response.text}"
    )

    # Verificar que la respuesta no contenga fragmentos de errores SQL
    body_text = response.text.lower()
    sql_error_keywords = [
        "sql syntax", "mysql_fetch", "ora-", "pg_query",
        "sqlexception", "syntax error", "unterminated",
    ]
    for keyword in sql_error_keywords:
        assert keyword not in body_text, (
            f"[TC11] La respuesta parece contener un error SQL (encontrado: '{keyword}'). "
            f"Posible vulnerabilidad de inyección SQL."
        )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.security
def test_tc12_xss_en_descripcion_bulto(endpoint, valid_headers, valid_payload_351002270):
    """
    TC12 — Payload XSS en el campo bultos[0].descripcion.

    Verificar que scripts maliciosos no sean almacenados sin sanitización.
    La respuesta no debe devolver el script sin escapar (stored-XSS).
    La API no debe devolver HTTP 500.

    Patrón probado: "<script>alert('XSS')</script>"
    """
    xss_payload = "<script>alert('XSS')</script>"
    payload = _clone(valid_payload_351002270)
    payload["bultos"][0]["descripcion"] = xss_payload

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    # No debe producir error de servidor
    assert response.status_code != 500, (
        f"[TC12] La API devolvió HTTP 500 ante payload XSS. "
        f"Body: {response.text}"
    )

    # Si la API acepta el valor, el script no debe aparecer sin escapar en respuesta
    if response.status_code in (200, 201):
        body_text = response.text
        assert "<script>" not in body_text, (
            f"[TC12] El payload XSS aparece sin sanitizar en la respuesta. "
            f"Posible vulnerabilidad de stored XSS."
        )


# ---------------------------------------------------------------------------
# 🔬 PRUEBAS DE BORDE (EDGE CASES)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.edge_case
def test_tc13_valoracobrar_negativo(endpoint, valid_headers, valid_payload_351002270):
    """
    TC13 — valoracobrar con valor negativo.

    Un monto negativo a cobrar carece de sentido de negocio.
    La API debe rechazarlo con HTTP 4xx.
    """
    payload = _clone(valid_payload_351002270)
    payload["valoracobrar"] = -500

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert 400 <= response.status_code < 500, (
        f"[TC13] Se esperaba error 4xx para valoracobrar negativo pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.edge_case
def test_tc14_kilos_bulto_extremadamente_alto(endpoint, valid_headers, valid_payload_351002270):
    """
    TC14 — Peso de bulto con valor extremadamente alto (99,999 kg).

    Verifica el comportamiento ante un peso operativamente imposible.
    Si existe un límite operativo, el sistema debe rechazarlo con 4xx.
    Si no existe validación, se documenta como brecha (el test pasa
    con advertencia mediante pytest.skip para documentar el hallazgo).
    La API nunca debe devolver HTTP 500.
    """
    payload = _clone(valid_payload_351002270)
    payload["bultos"][0]["kilos"] = 99999

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    # Lo crítico: no debe producir error no controlado
    assert response.status_code != 500, (
        f"[TC14] La API devolvió HTTP 500 ante peso extremo. Body: {response.text}"
    )

    if response.status_code in (200, 201):
        pytest.skip(
            "[TC14] BRECHA DOCUMENTADA: La API acepta 99,999 kg sin validación de "
            "límite superior. Se recomienda agregar validación de peso máximo operativo."
        )
    else:
        # 4xx: comportamiento esperado, hay validación
        assert 400 <= response.status_code < 500, (
            f"[TC14] Código inesperado {response.status_code}. Body: {response.text}"
        )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.edge_case
def test_tc22_codigopostal_origen_inexistente(endpoint, valid_headers, valid_payload_351002270):
    """
    TC22 — Código postal de origen con valor inexistente en la base de datos.

    Usar CP '00000' para verificar que el servicio de ruteo/geolocalización
    responda apropiadamente sin generar error 500.
    """
    payload = _clone(valid_payload_351002270)
    payload["origen"]["postal"]["codigopostal"] = "00000"

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code != 500, (
        f"[TC22] La API devolvió HTTP 500 para CP de origen inexistente. "
        f"Posible error no controlado en servicio de ruteo. Body: {response.text}"
    )
    assert 400 <= response.status_code < 500, (
        f"[TC22] Se esperaba 4xx para CP inexistente pero se obtuvo "
        f"{response.status_code}. Body: {response.text}"
    )


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.edge_case
def test_tc24_bulto_kilos_cero(endpoint, valid_headers, valid_payload_351002270):
    """
    TC24 — Bulto con peso igual a cero (kilos=0).

    Un bulto de 0 kg podría ser un error de carga de datos.
    Este test documenta si la API acepta o rechaza este valor límite.
    La API no debe devolver HTTP 500 en ningún caso.
    """
    payload = _clone(valid_payload_351002270)
    payload["bultos"][0]["kilos"] = 0

    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)

    assert response.status_code != 500, (
        f"[TC24] La API devolvió HTTP 500 para bulto con kilos=0. Body: {response.text}"
    )

    if response.status_code in (200, 201):
        pytest.skip(
            "[TC24] BRECHA DOCUMENTADA: La API acepta bultos con peso=0. "
            "Se recomienda validar que kilos > 0."
        )


# ---------------------------------------------------------------------------
# ⚡ PRUEBAS DE RENDIMIENTO
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not RUN_LIVE, reason=SKIP_REASON)
@pytest.mark.performance
def test_tc20_performance_baseline_respuesta_menor_3000ms(
    endpoint, valid_headers, valid_payload_351002270
):
    """
    TC20 — Línea base de rendimiento: tiempo de respuesta < 3000ms.

    Verifica que una solicitud válida (camino feliz, TC01) sea respondida
    en menos de 3000 milisegundos bajo condiciones normales (1 solicitud
    concurrente). Establece la línea base para regresiones de rendimiento.

    Si el sistema consistentemente supera 3000ms bajo una sola solicitud,
    se recomienda revisión de timeouts en la cadena de servicios.
    """
    payload = _clone(valid_payload_351002270)

    start_time = time.monotonic()
    response = requests.post(endpoint, json=payload, headers=valid_headers, timeout=10)
    elapsed_ms = (time.monotonic() - start_time) * 1000

    # El endpoint debe haber respondido exitosamente
    assert response.status_code in (200, 201), (
        f"[TC20] La solicitud base falló con {response.status_code}. "
        f"No se puede medir rendimiento. Body: {response.text}"
    )

    # Verificar umbral de tiempo
    assert elapsed_ms < 3000, (
        f"[TC20] La respuesta tardó {elapsed_ms:.0f}ms, superando el umbral de 3000ms. "
        f"Revisar rendimiento del servicio o dependencias (ruteo, base de datos)."
    )

    print(f"\n[TC20] Tiempo de respuesta: {elapsed_ms:.0f}ms (umbral: 3000ms)")


# ---------------------------------------------------------------------------
# Punto de entrada para ejecución directa (debugging)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
