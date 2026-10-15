"""Orden de ejecución de los seis agentes y contexto aprobado."""

from agents import architect, backend, frontend, testing, security, chapter

ROLES = (architect, backend, frontend, testing, security, chapter)
STEPS = tuple(
    (role.KEY, role.LABEL, role.agent, role.SPEC_FILE, role.EXTRACT_CODE)
    for role in ROLES
)


def build_tasks(feature: dict) -> dict:
    return {role.KEY: role.build_task(feature) for role in ROLES}
