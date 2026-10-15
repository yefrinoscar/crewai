# CrewAI para equipos

Los agentes parten con instrucciones básicas. Sigue [Mejora tu agente](MEJORA_TU_AGENTE.md) para completar el ejercicio y consultar resultados desde el portal.

Base de trabajo del Lab 4, S1. Lee una funcionalidad del backlog mediante MCP Projects
y genera una solución Quarkus 3.x y Angular 17 con seis agentes de CrewAI.
Cada agente tiene su definición y la tarea en un archivo propio.

## Editar tu agente

Los agentes son básicos: un objetivo breve, una responsabilidad por rol y una salida concreta.
Usa un requisito pequeño, por ejemplo crear una tarea con título.
Ajusta ese ejemplo al requisito del backlog de tu equipo.
Testing propone un caso válido y otro inválido; Security revisa entradas y secretos;
Chapter compara las entregas con el requisito. Los prompts conservan los formatos
que necesita el flujo para guardar código y revisar resultados.

Cada participante edita el archivo de su rol:

- `agents/architect.py`
- `agents/backend.py`
- `agents/frontend.py`
- `agents/testing.py`
- `agents/security.py`
- `agents/chapter.py`

El orden es `architect → backend → frontend → testing → security → chapter`.
Chapter reemplaza al LT como revisor final. La aprobación humana se conserva entre etapas.
Consulta [TEAM.md](TEAM.md) para crear el repo de tu equipo y repartir los archivos.

## Preparar el entorno

Requiere Python 3.11 a 3.13, Git y acceso a GitHub Copilot.
Usa Python 3.12 durante el taller y ejecuta los comandos en Bash. En Windows, abre Git Bash.

```bash
python -m venv .venv
if [ -f .venv/Scripts/activate ]; then
  source .venv/Scripts/activate
else
  source .venv/bin/activate
fi
python -m pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
```

Si en macOS o Linux tu instalación se llama `python3.12`, úsala para crear el entorno. Una vez activado, ejecuta `python`.

Instala [Copilot CLI](https://github.com/features/copilot/cli), abre `copilot` y ejecuta `/login`.
El SDK usa esa sesión con `COPILOT_USE_LOGGED_IN_USER=true`.
El modelo predeterminado es `gpt-6-luna` con esfuerzo `high`. Cada llamada consume uso del plan de Copilot.
Puedes descargar su runtime antes del taller con `python -m copilot download-runtime`.

## Conectar el backlog

Configura `.env` con el owner y repo del producto de tu equipo, `PROJECTS_MCP_URL`
y `PROJECTS_MCP_API_KEY`. Estos valores apuntan al servicio MCP del taller.
El repo del producto contiene el backlog; este repo contiene el código del Crew.

Si usas el MCP local del Lab 4, levántalo en otra terminal desde
`support/mcp-local` con el script `start-mcp.sh`.
Ese servicio requiere la imagen `localhost/mcp-github-project-manager:latest`, preparada por el instructor, y Podman o Docker. Si no tienes esa imagen, solicita al instructor un endpoint MCP del taller.
En macOS o Linux:

```sh
cd support/mcp-local
gh auth refresh -s project
bash start-mcp.sh --owner TU_OWNER --repo TU_PRODUCTO
```

Mantén esa terminal Bash abierta y ejecuta `python main.py` en otra terminal desde la raíz del repo. La URL de S1 es `http://localhost:8081`.

## Ejecutar el Crew

Desde la raíz de este repo, con el entorno virtual activado:

```sh
python main.py
```

Selecciona el proyecto y la funcionalidad. Cada paso ejecuta un mini-Crew de un agente.
En la aprobación humana puedes usar `s` para aprobar, `r` para reintentar con feedback,
o `n` para rechazar y detener el flujo. El checkpoint permite retomar los pasos aprobados.

Los artefactos se guardan en `output/`:

- `specs/user_story.md`: especificación del arquitecto.
- `specs/backend_spec.md` y `specs/frontend_spec.md`: implementaciones.
- `specs/testing_report.md`: casos, tests y comandos. Los resultados quedan pendientes de ejecución humana.
- `specs/security_report.md`: hallazgos y verificaciones de seguridad.
- `specs/chapter_review.md`: revisión final del Chapter.
- `backend-quarkus/` y `frontend-angular/`: código extraído y configuración de arranque.
- `.checkpoint.json`: estado local de la ejecución.

## Probar la solución generada

Con Java 17 o superior y Maven instalados, abre una terminal en `output/backend-quarkus`:

```sh
mvn test
mvn compile quarkus:dev
```

Con Node.js 18.19 o superior y npm, abre otra terminal en `output/frontend-angular`:

```sh
npm install
npm start
```

La API se inicia en `http://localhost:8080` y Angular en `http://localhost:4200`.
Revisa los comandos adicionales del informe de pruebas y registra sus resultados reales.

## Verificar cambios en los agentes

```sh
python tools/verify.py
```

Los checks recorren los seis roles, verifican artefactos, contexto y reanudación.
Sustituyen las llamadas al modelo y a MCP para ejecutarse sin credenciales.
La ejecución real de Copilot y MCP requiere el entorno del taller.

Consulta [SOURCE.md](SOURCE.md) para ver el origen de esta copia.
