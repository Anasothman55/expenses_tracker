from app.core.config import settings

if __name__ == '__main__':
  import uvicorn

  uvicorn.run(
    app='app.main:app',
    port=settings.SERVER_PORT,
    reload=settings.DEVELOP_MODE,
    host=settings.SERVER_HOST,
    workers= settings.SERVER_WORKER if not settings.DEVELOP_MODE else 1,
    log_config=None,
    log_level=None,
  )







