
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from datetime import datetime, timedelta

from app.db.postgress.repositories.revoked_jwt_tokens import TokenPurgeCron
from app.db.postgress.repositories.acc_recovery import AccountRecoveryPurgeCron
from app.db.postgress.models import RevokedToken, AccountRecovery
from app.core.security.token_creation import create_token, decode_token

@pytest.mark.asyncio
async def test_token_purge_cron():
    """
    Test the TokenPurgeCron job to ensure it deletes expired revoked tokens.
    """
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalars.return_value.all.side_effect = [
        [RevokedToken(jti="expired_token", data_expires=datetime.utcnow() - timedelta(hours=1))],
        [RevokedToken(jti="valid_token", data_expires=datetime.utcnow() + timedelta(hours=1))]
    ]
    mock_session.delete = AsyncMock()

    with patch('app.services.scheduler.base_cron.Config.get_property') as mock_get_property:
        # Mock the config to have a short interval for testing
        mock_get_property.return_value = {"token_purge_interval": 1}
        
        cron_job = TokenPurgeCron()
        await cron_job.run(mock_session)

        # Should only delete the expired token
        assert mock_session.delete.call_count == 1
        deleted_token = mock_session.delete.call_args[0][0]
        assert deleted_token.jti == "expired_token"
        mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_account_recovery_purge_cron():
    """
    Test the AccountRecoveryPurgeCron job to ensure it deletes expired account recovery tokens.
    """
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalars.return_value.all.side_effect = [
        [AccountRecovery(reset_token="expired", token_expires=datetime.utcnow() - timedelta(days=1))],
        [AccountRecovery(reset_token="valid", token_expires=datetime.utcnow() + timedelta(days=1))]
    ]
    mock_session.delete = AsyncMock()

    with patch('app.services.scheduler.base_cron.Config.get_property') as mock_get_property:
        mock_get_property.return_value = {"password_reset_purge_interval": 1}

        cron_job = AccountRecoveryPurgeCron()
        await cron_job.run(mock_session)

        assert mock_session.delete.call_count == 1
        deleted_recovery = mock_session.delete.call_args[0][0]
        assert deleted_recovery.reset_token == "expired"
        mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_expired_token_scenario():
    """
    Test that an expired token is correctly identified and handled.
    This involves temporarily modifying the token expiration settings.
    """
    with patch('app.core.security.token_creation.S') as mock_settings:
        # Set token expiration to 1 second for this test
        mock_settings.jwt_access_token_expires = 1
        mock_settings.jwt_refresh_token_expires = 1
        mock_settings.aes_key = b'\x00' * 32
        mock_settings.authjwt_algorithm = "HS256"

        mock_settings.authjwt_secret_key = "test_secret"
        mock_settings.nonce_size = 12

        # Create an access token that will expire quickly
        access_token = create_token(1, 1, refresh=False)
        
        # Wait for the token to expire
        await asyncio.sleep(2)

        mock_session = AsyncMock()
        # Mock is_token_revoked to return False, so we only test expiration
        with patch('app.core.security.token_creation.is_token_revoked', new_callable=AsyncMock) as mock_is_revoked:
            mock_is_revoked.return_value = False

            with pytest.raises(Exception) as excinfo:
                await decode_token(mock_session, access_token)
            
            assert "Token has expired" in str(excinfo.value)
