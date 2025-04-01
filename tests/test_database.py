from unittest.mock import AsyncMock, patch

import pytest
from odmantic.session import AIOSession

from src.database import get_session


@pytest.mark.asyncio
async def test_get_session():
    mock_session = AsyncMock(spec=AIOSession)

    with patch('src.database.engine.session', return_value=mock_session):
        session_generator = get_session()
        session = await anext(session_generator)
        assert session == mock_session

        mock_session.start.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_session_exception():
    mock_session = AsyncMock(spec=AIOSession)
    exception = Exception('Test Exception')

    with patch('src.database.engine.session', return_value=mock_session):
        session_generator = get_session()
        mock_session.start.side_effect = exception

        with pytest.raises(Exception, match='Test Exception') as exc_info:
            await anext(session_generator)

        assert exc_info.value == exception
        mock_session.start.assert_awaited_once()
