from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, timedelta

from database import get_session
from models import DailyHabitLog, User
from auth_service import get_current_user

router = APIRouter(prefix="/habits", tags=["habits"])


class HabitLogRequest(BaseModel):
    smoked_cigarettes: bool = False
    ate_sweets: bool = False
    brushed_after_meal: bool = False
    used_floss: bool = False
    used_sensodyne: bool = False


class HabitLogResponse(BaseModel):
    id: str
    user_id: int
    date: date
    smoked_cigarettes: bool
    ate_sweets: bool
    brushed_after_meal: bool
    used_floss: bool
    used_sensodyne: bool


@router.post("/log", response_model=HabitLogResponse)
async def save_daily_habits(request: HabitLogRequest, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Save or update today's habit log for the authenticated user."""
    today = date.today()
    user_id = current_user.id

    # Check if a log already exists for today
    statement = select(DailyHabitLog).where(
        DailyHabitLog.user_id == user_id,
        DailyHabitLog.date == today
    )
    existing_log = session.exec(statement).first()

    if existing_log:
        # Update existing log
        existing_log.smoked_cigarettes = request.smoked_cigarettes
        existing_log.ate_sweets = request.ate_sweets
        existing_log.brushed_after_meal = request.brushed_after_meal
        existing_log.used_floss = request.used_floss
        existing_log.used_sensodyne = request.used_sensodyne
        session.add(existing_log)
        session.commit()
        session.refresh(existing_log)
        return existing_log
    else:
        # Create new log
        new_log = DailyHabitLog(
            user_id=user_id,
            date=today,
            smoked_cigarettes=request.smoked_cigarettes,
            ate_sweets=request.ate_sweets,
            brushed_after_meal=request.brushed_after_meal,
            used_floss=request.used_floss,
            used_sensodyne=request.used_sensodyne,
        )
        session.add(new_log)
        session.commit()
        session.refresh(new_log)
        return new_log


@router.get("/history", response_model=List[HabitLogResponse])
async def get_habit_history(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Retrieve the last 7 days of habits for the authenticated user."""
    seven_days_ago = date.today() - timedelta(days=6)

    statement = (
        select(DailyHabitLog)
        .where(
            DailyHabitLog.user_id == current_user.id,
            DailyHabitLog.date >= seven_days_ago
        )
        .order_by(DailyHabitLog.date.desc())
    )
    logs = session.exec(statement).all()
    return logs
