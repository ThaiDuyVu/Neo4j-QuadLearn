"""Page specs registry for learning_geometry feature."""

from typing import Any, Callable, List, Optional
from app.shared.models.dto import PageSpec as SharedPageSpec
from app.features.learning_geometry.pages.overview import render_overview_page


class NavigationPageAdapter:
    """Adapter class wrapping PageSpec to bridge page_id/render_fn with path/render interface required by navigation.py."""

    def __init__(
        self,
        page_id: str,
        title: str,
        render_fn: Callable[..., Any],
        requires_auth: bool = False,
        allowed_roles: Optional[List[str]] = None,
    ):
        self._shared_spec = SharedPageSpec(
            page_id=page_id,
            title=title,
            render_fn=render_fn,
            requires_auth=requires_auth,
            allowed_roles=allowed_roles,
        )

    @property
    def path(self) -> str:
        return self._shared_spec.page_id

    @property
    def render(self) -> Callable[..., Any]:
        return self._shared_spec.render_fn

    @property
    def page_id(self) -> str:
        return self._shared_spec.page_id

    @property
    def title(self) -> str:
        return self._shared_spec.title

    @property
    def render_fn(self) -> Callable[..., Any]:
        return self._shared_spec.render_fn

    @property
    def requires_auth(self) -> bool:
        return self._shared_spec.requires_auth

    @property
    def allowed_roles(self) -> Optional[List[str]]:
        return self._shared_spec.allowed_roles


PAGE_SPECS = [
    NavigationPageAdapter(
        page_id="learning",
        title="Tổng quan Nội dung & Hình học",
        render_fn=render_overview_page,
    ),
]

PAGES = PAGE_SPECS