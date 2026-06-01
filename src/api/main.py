"""LinkSnap — URL shortener API.

FastAPI application hosted on Azure Container Apps with Cosmos DB for NoSQL.
Authenticates to Cosmos DB using managed identity (DefaultAzureCredential).
"""

import os
import string
import secrets
from datetime import datetime, timezone

from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.identity import DefaultAzureCredential
from fastapi import FastAPI, HTTPException, status
from pydantic import HttpUrl

from .models import CreateLinkRequest, LinkResponse, ErrorResponse

app = FastAPI(
    title="LinkSnap",
    description="URL shortener API — OMO Teams Quickstart",
    version="0.1.0",
)

# Cosmos DB configuration from environment (set by ACA)
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
DATABASE_NAME = os.environ.get("COSMOS_DATABASE", "linksnap")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER", "shortlinks")


def _get_container():
    """Get the Cosmos DB container using managed identity auth."""
    credential = DefaultAzureCredential()
    client = CosmosClient(url=COSMOS_ENDPOINT, credential=credential)
    database = client.get_database_client(DATABASE_NAME)
    return database.get_container_client(CONTAINER_NAME)


def _generate_short_code(length: int = 7) -> str:
    """Generate a cryptographically random base62 short code."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Health check. ACA probes use this for liveness."""
    return {"status": "ok"}


@app.post(
    "/links",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {"model": ErrorResponse},
    },
)
async def create_link(body: CreateLinkRequest):
    """Create a new shortened URL."""
    container = _get_container()
    short_code = _generate_short_code()
    now = datetime.now(timezone.utc).isoformat()

    item = {
        "id": short_code,
        "tenant_id": body.tenant_id,
        "short_code": short_code,
        "destination_url": str(body.destination_url),
        "created_at": now,
        "created_by": body.created_by or "anonymous",
        "click_count": 0,
        "is_active": True,
    }

    container.create_item(body=item)
    return LinkResponse(
        short_code=short_code,
        destination_url=str(body.destination_url),
        created_at=now,
    )


@app.get(
    "/links/{short_code}",
    response_model=LinkResponse,
    responses={
        404: {"model": ErrorResponse},
    },
)
async def resolve_link(short_code: str, tenant_id: str = "default"):
    """Resolve a short code to its destination URL."""
    container = _get_container()
    try:
        item = container.read_item(item=short_code, partition_key=tenant_id)
    except CosmosResourceNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": f"Short code '{short_code}' not found"},
        )

    # Increment click count
    item["click_count"] += 1
    container.replace_item(item=item, body=item)

    return LinkResponse(
        short_code=item["short_code"],
        destination_url=item["destination_url"],
        created_at=item["created_at"],
        click_count=item["click_count"],
    )
