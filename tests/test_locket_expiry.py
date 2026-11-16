import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from app.services import locket


class Response:
    def __init__(self, body, status=200):
        self.body, self.status = body, status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def json(self):
        return self.body


class Session:
    def __init__(self, response):
        self.response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def get(self, *args, **kwargs):
        return self.response

    def post(self, *args, **kwargs):
        return self.response


class ExpiryTests(unittest.IsolatedAsyncioTestCase):
    async def check(self, gold, status=200):
        body = {"subscriber": {"entitlements": {"Gold": gold} if gold is not None else {}}}
        with patch.object(locket.aiohttp, 'ClientSession', return_value=Session(Response(body, status))):
            with patch.object(locket, 'datetime', create=True) as clock:
                clock.fromisoformat = datetime.fromisoformat
                clock.now.return_value = datetime(2024, 1, 10, tzinfo=timezone.utc)
                return await locket.check_status('test-user')

    async def test_refunded_expired_gold_is_inactive(self):
        result = await self.check({'expires_date': '2024-01-06T00:00:00Z'})
        self.assertFalse(result['active'])
        self.assertEqual(result['reason'], 'expired')

    async def test_future_expiry_with_offset_is_active(self):
        result = await self.check({'expires_date': '2024-01-10T08:00:00+07:00'})
        self.assertTrue(result['active'])

    async def test_exact_expiry_is_inactive(self):
        result = await self.check({'expires_date': '2024-01-10T00:00:00Z'})
        self.assertFalse(result['active'])

    async def test_explicit_null_is_lifetime(self):
        self.assertTrue((await self.check({'expires_date': None}))['active'])

    async def test_missing_expiry_is_not_lifetime(self):
        result = await self.check({'product_identifier': 'test'})
        self.assertFalse(result['active'])
        self.assertEqual(result['reason'], 'invalid_expiry')

    async def test_malformed_expiry_fails_closed(self):
        result = await self.check({'expires_date': 'not-a-date'})
        self.assertFalse(result['active'])
        self.assertEqual(result['reason'], 'invalid_expiry')

    async def test_timezone_missing_fails_closed(self):
        result = await self.check({'expires_date': '2025-01-01T00:00:00'})
        self.assertFalse(result['active'])

    async def test_current_grace_period_preserves_access(self):
        result = await self.check({'expires_date': '2024-01-06T00:00:00Z',
                                   'grace_period_expires_date': '2024-01-14T00:00:00Z'})
        self.assertTrue(result['active'])

    async def test_expired_grace_period_is_inactive(self):
        result = await self.check({'expires_date': '2024-01-06T00:00:00Z',
                                   'grace_period_expires_date': '2024-01-07T00:00:00Z'})
        self.assertFalse(result['active'])

    async def test_missing_gold_is_inactive(self):
        self.assertFalse((await self.check(None))['active'])

    async def test_http_failure_is_unknown(self):
        self.assertIsNone(await self.check(None, 503))

    async def test_accepted_receipt_with_expired_gold_is_failure(self):
        expired = {'active': False, 'expires': '2024-01-06T00:00:00Z', 'reason': 'expired'}
        with patch.object(locket.aiohttp, 'ClientSession', return_value=Session(Response({}))):
            with patch.object(locket, 'check_status', new=AsyncMock(return_value=expired)):
                with patch.object(locket.asyncio, 'sleep', new=AsyncMock()):
                    result = await locket.inject_gold('test-user', {
                        'fetch_token': 'test', 'app_transaction': 'test', 'is_sandbox': True})
        self.assertFalse(result[0])
        self.assertIn('Gold expired at', result[1])

    async def test_accepted_receipt_with_unknown_status_is_not_expired(self):
        with patch.object(locket.aiohttp, 'ClientSession', return_value=Session(Response({}))):
            with patch.object(locket, 'check_status', new=AsyncMock(return_value=None)):
                with patch.object(locket.asyncio, 'sleep', new=AsyncMock()):
                    result = await locket.inject_gold('test-user', {
                        'fetch_token': 'test', 'app_transaction': 'test', 'is_sandbox': True})
        self.assertFalse(result[0])
        self.assertIn('could not be verified', result[1])

    async def test_entitlement_can_become_active_after_retry(self):
        with patch.object(locket.aiohttp, 'ClientSession', return_value=Session(Response({}))):
            with patch.object(locket, 'check_status', new=AsyncMock(side_effect=[{'active': False}, {'active': True}])):
                with patch.object(locket.asyncio, 'sleep', new=AsyncMock()):
                    result = await locket.inject_gold('test-user', {
                        'fetch_token': 'test', 'app_transaction': 'test', 'is_sandbox': True})
        self.assertEqual(result, (True, 'SUCCESS'))


if __name__ == '__main__':
    unittest.main()
