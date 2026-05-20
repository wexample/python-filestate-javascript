from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.shell import shell_run

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class NpmPackageLockOperation(AbstractOperation):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.CONTENT]

    def apply_operation(self) -> None:
        package_dir = Path(self.target.get_path())
        lockfile = package_dir / "package-lock.json"
        if lockfile.exists():
            lockfile.unlink()
        shell_run(
            [
                "npm",
                "install",
                "--package-lock-only",
                "--ignore-scripts",
                "--prefer-online",
            ],
            inherit_stdio=True,
            cwd=package_dir,
        )

    def undo(self) -> None:
        # No-op: lockfile creation is not reversible automatically.
        return None
