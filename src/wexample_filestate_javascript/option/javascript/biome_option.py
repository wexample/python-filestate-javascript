from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from .abstract_javascript_file_content_option import AbstractJavascriptFileContentOption

if TYPE_CHECKING:
    from pathlib import Path

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
        return target.read_text()

    # Biome is RAM-hungry on large generated files; chunking avoids OOM kills
    # (SIGKILL exit 137) when rectifying suites with 100+ TypeScript files.
    _BATCH_CHUNK_SIZE: int = 30

    def _run_batch_on_paths(
        self,
        reference_target: TargetFileOrDirectoryType,
        paths: list[Path],
    ) -> None:
        self._ensure_docker_container(reference_target)
        runner = self._get_or_create_runner(reference_target)
        for i in range(0, len(paths), self._BATCH_CHUNK_SIZE):
            chunk = paths[i : i + self._BATCH_CHUNK_SIZE]
            container_paths = [runner.rebase_path(p) for p in chunk]
            runner.execute(
                cmd=[
                    "biome",
                    "format",
                    "--write",
                    "--config-path=/tmp/biome.json",
                    *container_paths,
                ]
            )
