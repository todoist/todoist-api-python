from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import DEFAULT_API_URL
from tests.utils.test_utils import api_headers, mock_route

if TYPE_CHECKING:
    import respx

    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
    from todoist_api_python.models import UserPlanLimits


@pytest.mark.asyncio
async def test_get_user_plan_limits(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_user_plan_limits_sync_response: dict[str, Any],
    default_user_plan_limits: UserPlanLimits,
) -> None:
    endpoint = f"{DEFAULT_API_URL}/sync"

    mock_route(
        respx_mock,
        method="POST",
        url=endpoint,
        request_headers=api_headers(),
        request_json={"sync_token": "*", "resource_types": ["user_plan_limits"]},
        response_json=default_user_plan_limits_sync_response,
        response_status=200,
    )

    plan_limits = todoist_api.get_user_plan_limits()

    assert len(respx_mock.calls) == 1
    assert plan_limits == default_user_plan_limits
    assert plan_limits.current.reminders is False
    assert plan_limits.next is not None
    assert plan_limits.next.reminders is True

    plan_limits = await todoist_api_async.get_user_plan_limits()

    assert len(respx_mock.calls) == 2
    assert plan_limits == default_user_plan_limits
