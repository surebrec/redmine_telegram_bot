import asyncio

from aiohttp import ClientSession
from aiohttp_client_cache import CachedSession, SQLiteBackend
from django.conf import settings


class APIClient:
    def create_session(self, *args, **kwargs):
        raise NotImplemented('Session client is not implemented!')

    async def fetch_html(self, url: str, session: ClientSession,
                         **kwargs) -> tuple:
        async with session.request(method="GET", url=url,
                                   **kwargs) as request:
            return await request.json()

    async def make_requests(self, urls: set, **kwargs):
        async with self.create_session() as session:
            tasks = []
            for url in urls:
                tasks.append(
                    self.fetch_html(url=url,
                                    session=session,
                                    verify_ssl=False,
                                    **kwargs)
                )
            responses = await asyncio.gather(*tasks)
            await session.close()
            return responses


class RedmineAPIClient(APIClient):
    def __init__(self):
        self.url = settings.REDMINE_URL
        self.token = settings.REDMINE_TOKEN
        self.groups_endpoint = settings.REDMINE_GROUPS_ENDPOINT
        self.time_entries_endpoint = settings.REDMINE_TIME_ENTRIES_ENDPOINT

    def create_session(self):
        cache = SQLiteBackend(
            cache_name=settings.CACHE_NAME,
            expire_after=settings.CACHE_TIME,
        )
        client_session = CachedSession(cache=cache)
        client_session.headers.update({
            "X-Redmine-API-Key": settings.REDMINE_TOKEN
        })
        return client_session

    def get_group_data(self, group_ids, **kwargs):
        urls = {
            self.groups_endpoint.format(url=self.url,
                                        group_id=group_id,
                                        format='json')
            for group_id in group_ids}
        return asyncio.run(self.make_requests(urls=urls, **kwargs))

    def get_time_entries_data(self, **kwargs):
        urls = {self.time_entries_endpoint.format(url=self.url,
                                                  format='json')}
        return asyncio.run(self.make_requests(urls=urls, **kwargs))
