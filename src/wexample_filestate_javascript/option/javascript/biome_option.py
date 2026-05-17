from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from .abstract_javascript_file_content_option import AbstractJavascriptFileContentOption

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class BiomeOption(AbstractJavascriptFileContentOption):
    def get_description(self) -> str:
        return "Format and lint JavaScript/TypeScript code using Biome."

    def _apply_content_change(self, target: TargetFileOrDirectoryType) -> str:
        cache = self._get_or_build_batch_cache(target)
        path_key = str(target.get_path())
        if path_key in cache:
            return cache[path_key]
        # Target wasn't part of the batch (e.g. already rectified) → fall back.
        return target.read_text()

    def _run_batch_on_targets(
        self,
        reference_target: TargetFileOrDirectoryType,
        targets: list[TargetFileOrDirectoryType],
    ) -> None:
        self._ensure_docker_container(reference_target)
        container_paths = [self._get_container_file_path(t) for t in targets]
        self._get_or_create_runner(reference_target).execute(
            cmd=[
                "biome",
                "check",
                "--write",
                "--config-path=/tmp/biome.json",
                *container_paths,
            ]
        )
