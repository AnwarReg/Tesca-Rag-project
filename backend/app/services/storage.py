import boto3

from app.config import settings

# Only build a client if a bucket is configured. With no bucket (e.g. local
# dev), uploads become no-ops so nothing crashes without AWS.
_s3 = (
    boto3.client("s3", region_name=settings.aws_region) if settings.s3_bucket else None
)


def upload(key: str, data: bytes, content_type: str = "application/pdf") -> None:
    """Store raw bytes in S3 under `key`. No-op if S3 isn't configured."""
    if _s3 is None:
        return
    _s3.put_object(
        Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type
    )
