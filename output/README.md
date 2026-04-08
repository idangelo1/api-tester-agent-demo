# Suite de Pruebas Automatizadas — API Alta de Envío (AltaOrden)

Suite de pruebas con **pytest + requests** para el endpoint `POST /api/v1/AltaOrden`
del servicio de Alta de Pre-envíos de **Andreani**.

---

## Índice

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Prerrequisitos](#2-prerrequisitos)
3. [Instalación](#3-instalación)
4. [Configuración](#4-configuración)
5. [Ejecución de Tests](#5-ejecución-de-tests)
6. [Categorías de Tests](#6-categorías-de-tests)
7. [Casos de Prueba](#7-casos-de-prueba)
8. [Reportes](#8-reportes)
9. [Integración CI/CD](#9-integración-cicd)
10. [Solución de Problemas](#10-solución-de-problemas)

---

## 1. Estructura del Proyecto

```
output/
├── test_alta_orden.py    # Suite de pruebas automatizadas (pytest + requests)
├── test_plan.md          # Plan de pruebas completo en español
├── requirements.txt      # Dependencias Python
└── README.md             # Este archivo
```

---

## 2. Prerrequisitos

| Requisito | Versión Mínima |
|-----------|---------------|
| Python    | 3.10+         |
| pip       | 23+           |
| Acceso a la red QA de Andreani | — |
| Cookie de sesión válida | — |

---

## 3. Instalación

```bash
# 1. Clonar el repositorio (o descomprimir el artefacto)
git clone <repo-url>
cd api-tester-agent-demo

# 2. Crear y activar un entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r output/requirements.txt
```

---

## 4. Configuración

Los tests utilizan variables de entorno para evitar hardcodear credenciales.

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `RUN_LIVE_TESTS` | Habilita la ejecución real contra el ambiente QA. Debe ser `1`. | `0` (tests skipped) |
| `ANDREANI_BASE_URL` | URL base del servicio QA. | `https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar` |
| `ANDREANI_COOKIE` | Cookie de autenticación en formato `nombre=valor`. | Valor de la colección Postman |

### Archivo `.env` (Opcional)

Podés crear un archivo `.env` en la raíz del proyecto para definir las variables localmente:

```dotenv
# .env — NO commitear este archivo al repositorio
RUN_LIVE_TESTS=1
ANDREANI_BASE_URL=https://alta-preenvios-api-apiode-qa.apps.ocpqa.andreani.com.ar
ANDREANI_COOKIE=60bd27fe9c81a15e11372fd76131481e=<TU_TOKEN_AQUI>
```

> ⚠️ **Importante**: Agregar `.env` al `.gitignore` para no exponer credenciales.

Para cargar las variables desde `.env`:

```bash
# Con python-dotenv instalado, los tests lo cargan automáticamente
# O bien exportar manualmente:
export $(cat .env | xargs)
```

---

## 5. Ejecución de Tests

### Ejecución Básica (todos los tests)

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v
```

### Sin Habilitar Tests (verificar que se skipean correctamente)

```bash
pytest output/test_alta_orden.py -v
# Todos los tests deben aparecer como SKIPPED
```

### Con Reporte HTML

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v \
  --html=output/report.html \
  --self-contained-html
```

Abrir `output/report.html` en el navegador para ver el reporte visual.

### Con Reporte JSON (para CI/CD)

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v \
  --json-report \
  --json-report-file=output/report.json
```

### Con Timeout por Test

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v --timeout=15
```

---

## 6. Categorías de Tests

Los tests están organizados con marcadores de pytest para ejecución selectiva:

| Marcador | Descripción |
|----------|-------------|
| `functional` | Pruebas del camino feliz y flujos de negocio válidos |
| `negative` | Pruebas con datos inválidos o campos faltantes |
| `security` | Pruebas de autenticación, inyección y XSS |
| `edge_case` | Valores límite y casos de borde |
| `performance` | Línea base de tiempo de respuesta |

### Ejecutar Solo una Categoría

```bash
# Solo funcionales
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m functional

# Solo seguridad
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m security

# Solo negativos
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m negative

# Solo edge cases
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m edge_case

# Funcionales Y negativos
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m "functional or negative"

# Excluir performance
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v -m "not performance"
```

---

## 7. Casos de Prueba

| ID | Test Function | Marcador | Descripción |
|----|---------------|----------|-------------|
| TC01 | `test_tc01_happy_path_contrato_351002270` | functional | Camino feliz — Tigre → Avellaneda, contrato 351002270 |
| TC02 | `test_tc02_happy_path_contrato_351002665_con_idpedido` | functional | Camino feliz — Ezeiza → La Plata, contrato 351002665 |
| TC03 | `test_tc03_bultos_vacios` | negative | Array de bultos vacío |
| TC04 | `test_tc04_email_invalido_remitente` | negative | Email de remitente inválido |
| TC05 | `test_tc05_dos_bultos` | functional | Dos bultos en el array |
| TC06 | `test_tc06_contrato_ausente` | negative | Campo 'contrato' ausente |
| TC07 | `test_tc07_codigopostal_origen_ausente` | negative | CP de origen vacío |
| TC08 | `test_tc08_destinatario_ausente` | negative | Campo 'destinatario' ausente |
| TC09 | `test_tc09_sin_cookie_autenticacion` | security | Sin cookie → 401/403 |
| TC10 | `test_tc10_cookie_invalida` | security | Cookie adulterada → 401/403 |
| TC11 | `test_tc11_sql_injection_remitente_nombre` | security | SQL injection en nombre del remitente |
| TC12 | `test_tc12_xss_en_descripcion_bulto` | security | XSS en descripción del bulto |
| TC13 | `test_tc13_valoracobrar_negativo` | edge_case | valoracobrar negativo |
| TC14 | `test_tc14_kilos_bulto_extremadamente_alto` | edge_case | Peso de bulto = 99,999 kg |
| TC15 | `test_tc15_remitente_ausente` | negative | Bloque 'remitente' ausente |
| TC16 | `test_tc16_content_type_incorrecto` | negative | Content-Type: text/plain |
| TC17 | `test_tc17_contrato_string_vacio` | negative | contrato="" (string vacío) |
| TC18 | `test_tc18_contrato_null` | negative | contrato=null |
| TC19 | `test_tc19_multiples_destinatarios` | functional | Dos destinatarios en el array |
| TC20 | `test_tc20_performance_baseline_respuesta_menor_3000ms` | performance | Tiempo respuesta < 3000ms |
| TC21 | `test_tc21_contrato_inexistente` | negative | Contrato "999999999" (no existe) |
| TC22 | `test_tc22_codigopostal_origen_inexistente` | edge_case | CP origen = "00000" |
| TC23 | `test_tc23_body_vacio` | negative | Body JSON vacío {} |
| TC24 | `test_tc24_bulto_kilos_cero` | edge_case | kilos=0 en bulto |

**Total: 20 tests implementados** (TC01–TC24, con TC19 documentando comportamiento)

---

## 8. Reportes

### Reporte HTML (Recomendado para QA)

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py \
  --html=output/report.html \
  --self-contained-html \
  -v
# Abrir output/report.html en el navegador
```

### Reporte JSON (Para CI/CD y dashboards)

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py \
  --json-report \
  --json-report-file=output/report.json \
  -v
```

### Salida de Consola Verbosa con Duración

```bash
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v --durations=10
```

---

## 9. Integración CI/CD

### GitHub Actions

```yaml
# .github/workflows/api-tests.yml
name: API Tests - AltaOrden

on:
  schedule:
    - cron: '0 8 * * 1-5'  # Lunes a viernes a las 8am UTC
  workflow_dispatch:        # Ejecución manual

jobs:
  api-tests:
    runs-on: ubuntu-latest
    environment: qa          # Usar secrets del environment 'qa'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r output/requirements.txt

      - name: Run API Tests
        env:
          RUN_LIVE_TESTS: '1'
          ANDREANI_BASE_URL: ${{ secrets.ANDREANI_BASE_URL }}
          ANDREANI_COOKIE: ${{ secrets.ANDREANI_COOKIE }}
        run: |
          pytest output/test_alta_orden.py -v \
            --html=output/report.html \
            --self-contained-html \
            --json-report \
            --json-report-file=output/report.json \
            --timeout=15

      - name: Upload Test Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-test-report
          path: output/report.html
```

> ⚠️ **Secrets requeridos** en el repositorio/environment de GitHub:
> - `ANDREANI_BASE_URL`
> - `ANDREANI_COOKIE`

### Jenkins (Declarative Pipeline)

```groovy
pipeline {
    agent any
    environment {
        RUN_LIVE_TESTS = '1'
        ANDREANI_BASE_URL = credentials('andreani-qa-url')
        ANDREANI_COOKIE   = credentials('andreani-qa-cookie')
    }
    stages {
        stage('Install') {
            steps {
                sh 'pip install -r output/requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    pytest output/test_alta_orden.py -v \
                      --html=output/report.html \
                      --self-contained-html \
                      --timeout=15
                '''
            }
            post {
                always {
                    publishHTML(target: [
                        reportDir: 'output',
                        reportFiles: 'report.html',
                        reportName: 'API Test Report'
                    ])
                }
            }
        }
    }
}
```

---

## 10. Solución de Problemas

### Todos los tests aparecen como SKIPPED

**Causa:** La variable `RUN_LIVE_TESTS` no está definida o no es `"1"`.

```bash
# Verificar la variable
echo $RUN_LIVE_TESTS

# Ejecutar correctamente
RUN_LIVE_TESTS=1 pytest output/test_alta_orden.py -v
```

### Error de Conexión (ConnectionError / Timeout)

**Causa:** No hay acceso a la red QA de Andreani.

**Solución:**
- Verificar conectividad VPN si aplica.
- Confirmar que la URL en `ANDREANI_BASE_URL` es correcta.
- Aumentar el timeout: agregar `--timeout=30` al comando pytest.

### Error 401/403 en Tests Funcionales

**Causa:** La cookie de autenticación expiró.

**Solución:**
- Obtener una nueva cookie desde el portal o la colección Postman actualizada.
- Actualizar la variable `ANDREANI_COOKIE`.

```bash
export ANDREANI_COOKIE="60bd27fe9c81a15e11372fd76131481e=NUEVA_COOKIE_AQUI"
```

### Tests TC14 / TC24 Aparecen como SKIPPED con Advertencia

**Comportamiento esperado.** Estos tests documentan brechas de validación cuando la API acepta valores que deberían ser rechazados. El mensaje del skip explica el hallazgo.

### Warning: `PytestUnknownMarkWarning`

Agregar un archivo `pytest.ini` en la raíz del proyecto:

```ini
# pytest.ini
[pytest]
markers =
    functional: Pruebas del camino feliz y flujos de negocio válidos
    negative: Pruebas con datos inválidos o campos faltantes
    security: Pruebas de autenticación e inyección
    edge_case: Valores límite y casos de borde
    performance: Línea base de tiempo de respuesta
```

---

## Contacto y Contribuciones

Para reportar falsos positivos, proponer nuevos casos de prueba o actualizar el contrato de la API, abrir un issue en el repositorio o contactar al equipo de QA Automation.

---

*Generado para el proyecto de automatización de pruebas API Andreani — Alta de Pre-envíos.*
