from tempfile import SpooledTemporaryFile
from typing import Any, Optional

import aioboto3

from agroatom.settings import settings


class FileStorage:
    @staticmethod
    async def get_file(file_name: str, prefix: str = ""):
        obj = None

        async with aioboto3.resource(
            "s3",
            endpoint_url=settings.s3_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        ) as s3:
            try:
                obj = await s3.meta.client.get_object(
                    Bucket=settings.s3_bucket_name,
                    Key=f"{settings.environment}/{prefix}/{file_name}",
                )
            except Exception:
                pass

        return obj

    @staticmethod
    async def get_temp_file(file_name: str, prefix: str = ""):
        obj = None

        async with aioboto3.resource(
            "s3",
            endpoint_url=settings.s3_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        ) as s3:
            try:
                obj = await s3.meta.client.get_object(
                    Bucket=settings.s3_bucket_name,
                    Key=f"{settings.environment}/{prefix}/{file_name}",
                )

            except Exception:
                pass

            else:
                obj = SpooledTemporaryFile()

                await s3.meta.client.download_fileobj(
                    Bucket=settings.s3_bucket_name,
                    Key=f"{settings.environment}/{prefix}/{file_name}",
                    Fileobj=obj,
                )

                obj.seek(0)

        return obj

    @staticmethod
    async def upload_file(body: str, file_name: str, prefix: str = "") -> str:
        async with aioboto3.resource(
            "s3",
            endpoint_url=settings.s3_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        ) as s3:
            bucket = await s3.Bucket(settings.s3_bucket_name)

            path = f"{settings.environment}/{prefix}/{file_name}"

            await bucket.put_object(
                Body=body,
                Key=path,
            )

            return f"/{path}"

    @staticmethod
    async def get_url(
        file_name: str,
        default: Any = None,
        prefix: str = "",
        expiration: Optional[int] = None,
        with_check: bool = False,
    ):
        async with aioboto3.resource(
            "s3",
            endpoint_url=settings.s3_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        ) as s3:
            params = {
                "Bucket": settings.s3_bucket_name,
                "Key": f"{settings.environment}/{prefix}/{file_name}",
            }
            url = await s3.meta.client.generate_presigned_url(
                "get_object",
                Params=params,
                ExpiresIn=expiration,
            )

            return url
