# Trabajar en equipo

## Crear el repositorio del equipo

El líder crea el repositorio en su cuenta personal desde esta plantilla:

```sh
gh repo create crewai --template NTTData-Academy/crewai --public --clone
```

Agrega a tus compañeros como colaboradores con permiso de escritura en el repo del equipo.
Los demás integrantes clonan ese mismo repo:

```sh
gh repo clone <CAPTAIN>/crewai
cd crewai
```

## Repartir los archivos

Anota un responsable por archivo. El equipo tiene seis personas y cada una edita su propio agente.

- `agents/architect.py`: responsable pendiente. Define la solución y el contrato de API.
- `agents/backend.py`: responsable pendiente. Implementa el backend.
- `agents/frontend.py`: responsable pendiente. Implementa el frontend.
- `agents/testing.py`: responsable pendiente. Diseña las pruebas y sus comandos de ejecución.
- `agents/security.py`: responsable pendiente. Revisa riesgos y propone correcciones verificables.
- `agents/chapter.py`: responsable pendiente. Revisa todas las entregas y emite el veredicto final.

## Registrar responsables para el dashboard

Copia `team.example.json` a `team.json`, reemplaza los seis valores por usuarios reales de GitHub distintos y publica ese archivo en `main`. El dashboard lee `roles` para asociar cada agente con su responsable. Los nombres de ejemplo no son participantes.

## Entregar un cambio

1. Acuerden un requerimiento y sus criterios de aceptación.
2. Crea tu rama, por ejemplo `git switch -c agents/backend`.
3. Edita las instrucciones de tu agente en su archivo. Coordina los cambios de contratos con el arquitecto.
4. Ejecuta `python tools/verify.py`.
5. Publica tu rama y abre un PR hacia `main` del repo del líder. No envíes el PR al template de la organización.
6. Pide a un compañero que revise el cambio antes de integrarlo.

Una persona ejecuta el pipeline integrado desde `main`. El equipo participa en las aprobaciones
humanas y aporta feedback en cada etapa. Cada integrante conserva su propia `.env`, autenticación
y entorno virtual. No compartan checkpoints entre ejecuciones de distintas computadoras.

Los agentes generan texto y archivos. El agente de pruebas propone tests y comandos;
una persona los ejecuta y adjunta la salida real al PR. Un informe del modelo no demuestra que las pruebas pasaron.
