from unittest.mock import AsyncMock, patch

import pytest
from odmantic.session import AIOSession

from src.database import get_session


@pytest.mark.asyncio
async def test_get_session():
    mock_session = AsyncMock(spec=AIOSession)
    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = None

    with patch('src.database.engine.session', return_value=mock_context_manager):
        session_generator = get_session()
        session = await anext(session_generator)
        assert session == mock_session

        mock_context_manager.__aenter__.assert_awaited_once()
