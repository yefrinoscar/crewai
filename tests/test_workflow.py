"""Exercise the six-role pipeline without calling Copilot or GitHub."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import main as app
from crew.workflow import ROLES, STEPS, build_tasks


FEATURE = {
    "title": "Transfer funds",
    "description": "Transfer funds between accounts",
    "acceptance_criteria": ["Reject a transfer with insufficient funds"],
}


class WorkflowTests(unittest.TestCase):
    def test_each_role_builds_its_own_task(self):
        tasks = build_tasks(FEATURE)
        self.assertEqual(
            list(tasks),
            ["architect", "backend", "frontend", "testing", "security", "chapter"],
        )
        for role in ROLES:
            self.assertIs(tasks[role.KEY].agent, role.agent)
            self.assertIn("Transfer funds", tasks[role.KEY].description)
            self.assertIn(FEATURE["description"], tasks[role.KEY].description)
            for criterion in FEATURE["acceptance_criteria"]:
                self.assertIn(criterion, tasks[role.KEY].description)
            self.assertTrue(Path(role.__file__).is_file())

    def test_pipeline_saves_all_roles_and_resumes(self):
        calls = []

        def run(agent, task):
            key = next(role.KEY for role in ROLES if role.agent is agent)
            calls.append((key, task.description))
            if key == "backend":
                return "```java\n// BalanceService.java\npackage pe.bcp.login.service;\npublic class BalanceService {}\n```"
            if key == "frontend":
                return "```typescript\n// balance.service.ts\nexport class BalanceService {}\n```"
            if key == "testing":
                return "Coverage report. NO EJECUTADO.\n```java\n// BalanceTest.java\npackage pe.bcp.login;\npublic class BalanceTest {}\n```"
            return f"Approved output from {key}. No model was called."

        with tempfile.TemporaryDirectory() as tmp, contextlib.ExitStack() as stack:
            output = Path(tmp)
            stack.enter_context(patch.object(app, "OUTPUT_DIR", output))
            stack.enter_context(
                patch.object(app, "CHECKPOINT_FILE", output / ".checkpoint.json")
            )
            stack.enter_context(patch.object(app, "proj_tools", return_value=[]))
            stack.enter_context(
                patch.object(
                    app,
                    "list_projects",
                    return_value=[{"id": "P1", "title": "Team backlog"}],
                )
            )
            stack.enter_context(
                patch.object(
                    app,
                    "list_project_items",
                    return_value=[{"title": FEATURE["title"]}],
                )
            )
            stack.enter_context(
                patch.object(app, "get_feature_from_item", return_value=FEATURE)
            )
            stack.enter_context(patch.object(app, "run_step", side_effect=run))
            stack.enter_context(
                patch.object(app, "hitl_approve", return_value=("s", ""))
            )
            stack.enter_context(patch("builtins.input", return_value="1"))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            app.main()

            self.assertEqual([key for key, _ in calls], [role.KEY for role in ROLES])
            for key, _, _, spec, _ in STEPS:
                self.assertTrue((output / "specs" / spec).is_file(), key)
            self.assertTrue(
                (
                    output
                    / "backend-quarkus/src/test/java/pe/bcp/login/BalanceTest.java"
                ).is_file()
            )
            chapter_prompt = calls[-1][1]
            self.assertIn("Coverage report", chapter_prompt)
            self.assertIn("Approved output from security", chapter_prompt)
            checkpoint = json.loads((output / ".checkpoint.json").read_text())
            self.assertEqual(len(checkpoint["steps"]), 6)
            self.assertTrue(
                all(
                    step["status"] == "approved"
                    for step in checkpoint["steps"].values()
                )
            )

            app.main()
            self.assertEqual(
                len(calls), 6, "Approved steps must not call the model again"
            )


if __name__ == "__main__":
    unittest.main()
