import uvicorn

from agroatom.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "agroatom.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
        reload_dirs=["./agroatom/"],
    )


if __name__ == "__main__":
    main()
