# api-tester-agent-demo
Desploy de un custom agent para tests de APIs

## Uso compartido en VS Code

Este repositorio expone un agente compartido de Copilot en `.github/agents/api-tester.agent.md`.

Para disponibilizarlo al equipo:

1. Versiona estos archivos en Git y compártelos en el repositorio.
2. Pide a tus compañeros que abran este repo en VS Code con GitHub Copilot Chat habilitado.
3. El agente `API Tester` debería aparecer en el selector de agentes o poder invocarse por nombre desde el chat.

La skill complementaria está en `.github/skills/api-testing-specialist/SKILL.md` para cargar el workflow de testing bajo demanda.

## Integracion k6 (load testing)

El flujo de k6 quedo integrado en el agente principal `API Tester` para evitar duplicidad de agentes.

Archivos relevantes:

1. Agente integrado: `.github/agents/api-tester.agent.md`
2. Skill integrada: `.github/skills/api-testing-specialist/SKILL.md`
3. Instrucciones para scripts k6: `.github/instructions/k6-script-generation/k6-script-generation.instructions.md`

### Como usarlo

1. En Copilot Chat, selecciona el agente `API Tester`.
2. Pidele generar o revisar un script k6 con endpoint, auth, perfil de carga y thresholds.
3. Si faltan parametros obligatorios, el flujo esta configurado para pedirlos antes de avanzar.

### Ejemplo de prompt

`Genera un script k6 para POST /api/v1/AltaOrden con 50 VUs, ramp-up de 2 minutos, 10 minutos de duracion, p95 < 800ms y error rate < 1%.`

## Reportes automaticos de k6

Si, k6 puede generar reportes de cada ejecucion.

1. Resumen en JSON con `--summary-export`.
2. Reporte HTML con dashboard integrado usando `K6_WEB_DASHBOARD=true` y `K6_WEB_DASHBOARD_EXPORT`.

### Ejecucion recomendada en PowerShell

```powershell
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$outDir = "output"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$env:K6_WEB_DASHBOARD = "true"
$env:K6_WEB_DASHBOARD_EXPORT = "$outDir/k6-report-$timestamp.html"

k6 run output/alta-orden-post-V2.k6.js --summary-export "$outDir/k6-summary-$timestamp.json"
```

Con este comando, cada corrida deja archivos versionados por fecha en `output/`.

### Recomendacion para tus .md de flujo

En cualquier guia de ejecucion de carga, agrega esta regla:

`Toda ejecucion de k6 debe incluir export de resumen JSON y reporte HTML con timestamp.`
