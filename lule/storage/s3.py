from contextlib import asynccontextmanager

import aioboto3

from ..settings import (
    BUCKET_NAME,
    S3_ACCESS_KEY_ID,
    S3_ENDPOINT_URL,
    S3_SECRET_ACCESS_KEY,
)


class _S3Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_S3Client, cls).__new__(cls)
            cls._instance.s3 = None
        return cls._instance

    @asynccontextmanager
    async def _client(self):
        session = aioboto3.Session(region_name="auto")
        async with session.client(
            "s3",
            endpoint_url=S3_ENDPOINT_URL,
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        ) as s3:
            yield s3

    async def upload(self, content: bytes, object_key: str) -> None:
        async with self._client() as s3:
            await s3.put_object(
                Bucket=BUCKET_NAME, Key=object_key, Body=content
            )

    async def generate_signed_url(self, object_key: str, expiration=3600):
        async with self._client() as s3:
            url = await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_NAME, "Key": object_key},
                ExpiresIn=expiration,
            )

            return url


S3Client = _S3Client()
