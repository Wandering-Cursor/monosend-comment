import json
from typing import Any
from src.schemas.link import Link
from src.settings import S3_BUCKET_NAME
import boto3
from botocore.exceptions import ClientError


def s3_client() -> Any:
    if not S3_BUCKET_NAME:
        raise RuntimeError("S3_BUCKET_NAME is not configured")

    return boto3.client(
        "s3",
    )


def get_links(chat_id: int | str) -> list[Link]:
    s3 = s3_client()

    try:
        links = s3.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=str(chat_id),
        )
    except ClientError:
        return []

    data = json.loads(links["Body"].read())

    all_links = [Link(**item) for item in data]

    return sorted(all_links, key=lambda x: x["created_at"], reverse=True)


def add_link(chat_id: int | str, link: Link) -> None:
    s3 = s3_client()

    links = get_links(chat_id)
    links.append(link)

    links = sorted(links, key=lambda x: x["created_at"], reverse=True)

    s3.put_object(
        Key=str(chat_id),
        Body=json.dumps([item for item in links]),
        Bucket=S3_BUCKET_NAME,
    )
