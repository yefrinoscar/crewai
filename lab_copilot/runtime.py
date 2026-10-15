from __future__ import annotations

import asyncio
import os
from typing import Any

import copilot
from copilot.generated.rpc import PermissionDecisionReject
from copilot.session_events import AssistantMessageData


def prompt_text(messages: Any) -> str:
    if isinstance(messages, str):
        return messages
    parts = []
    for message in messages:
        if isinstance(message, dict):
            role, content = message.get("role", "user"), message.get("content", "")
        else:
            role, content = message.type, message.content
        if isinstance(content, list):
            content = "\n".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in content
            )
        parts.append(f"[{role.upper()}]\n{content}")
    return "\n\n".join(parts)


async def complete(prompt: str, model: str, timeout: float = 600) -> str:
    def deny_permission(*_: Any) -> PermissionDecisionReject:
        return PermissionDecisionReject(feedback="El laboratorio solo solicita texto al modelo.")

    logged_in = os.getenv("COPILOT_USE_LOGGED_IN_USER", "true").lower() in {"true", "1", "yes", "s"}
    async with copilot.CopilotClient(use_logged_in_user=logged_in) as client:
        async with await client.create_session(
            model=model,
            reasoning_effort=os.getenv("COPILOT_REASONING_EFFORT", "high"),
            available_tools=[], on_permission_request=deny_permission,
            system_message={"mode": "replace", "content":
                "Sigue las instrucciones del historial proporcionado por el laboratorio. "
                "Devuelve texto o archivos en el formato solicitado, sin ejecutar herramientas."},
            skip_custom_instructions=True,
            working_directory=os.getcwd(),
        ) as session:
            event = await session.send_and_wait(prompt, timeout=timeout)
            if event is None or not isinstance(event.data, AssistantMessageData) or not event.data.content:
                raise RuntimeError("Copilot terminó sin devolver una respuesta de texto.")
            return event.data.content


def complete_sync(messages: Any, model: str, timeout: float = 600) -> str:
    return asyncio.run(complete(prompt_text(messages), model, timeout))
