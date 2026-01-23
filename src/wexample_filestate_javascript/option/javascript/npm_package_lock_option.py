from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class NpmPackageLockOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        from wexample_filestate_javascript.operation.npm_package_lock_operation import (
            NpmPackageLockOperation,
        )

        value = self.get_value()
        if value is not None and value.is_none():
            return None
        if value is not None and value.is_bool() and not value.get_bool():
            return None

        package_dir = Path(target.get_path())
        package_json = package_dir / "package.json"
        if not package_json.exists():
            return None

        package_lock = package_dir / "package-lock.json"
        if package_lock.exists():
            try:
                if package_lock.stat().st_mtime >= package_json.stat().st_mtime:
                    return None
            except OSError:
                pass

        return NpmPackageLockOperation(
            option=self,
            target=target,
            description="Generate package-lock.json from package.json",
        )
