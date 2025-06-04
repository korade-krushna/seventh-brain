
router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/close")
async def close_session(session_id: str):
    return {"message": "Session closed successfully"}


async def list_sessions():
    return {"sessions": list(user_sessions.keys())}
