from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class JavascriptOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_docker_image_name(cls) -> str | None:
        from wexample_filestate_javascript.option.javascript.abstract_javascript_file_content_option import (
            AbstractJavascriptFileContentOption,
        )

        return AbstractJavascriptFileContentOption.DOCKER_IMAGE_NAME

    @classmethod
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        from wexample_filestate_javascript.option.javascript_option import (
            JavascriptOption,
        )

        return [
            JavascriptOption,
        ]
