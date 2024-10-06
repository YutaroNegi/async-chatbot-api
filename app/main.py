import logging
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
from app.routers import health, users


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("app.main")


async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
