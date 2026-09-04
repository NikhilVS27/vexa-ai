from fastapi import APIRouter

from backend.app.services.discovery_service import run_discovery


# ==========================================
# DISCOVERY ROUTER
# ==========================================

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"]
)


# ==========================================
# RUN DISCOVERY
# ==========================================

@router.post("/run")
def run_brand_discovery():

    result = run_discovery()

    return result