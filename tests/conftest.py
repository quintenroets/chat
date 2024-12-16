import pytest

from chat.context import Context, context


@pytest.fixture
def test_context() -> Context:
    context.config.pause_time = 0.1
    context.options.system_prompt = "Be friendly"
    return context
