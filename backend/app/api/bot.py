"""
Strategy Bot API endpoints
"""

from fastapi import APIRouter, HTTPException
import logging

from app.models.schemas import (
    StrategyBotConfig,
    StrategyBotStatus,
    StrategyLearningReport,
    StrategyRecommendation,
)
from app.services.strategy_bot import strategy_bot_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/status", response_model=StrategyBotStatus)
async def get_bot_status():
    try:
        return strategy_bot_service.get_status()
    except Exception as e:
        logger.error(f"Error getting bot status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get bot status")


@router.post("/run")
async def run_bot_once():
    try:
        return await strategy_bot_service.run_cycle()
    except Exception as e:
        logger.error(f"Error running bot cycle: {e}")
        raise HTTPException(status_code=500, detail="Failed to run strategy bot")


@router.get("/recommendations", response_model=list[StrategyRecommendation])
async def get_recommendations():
    try:
        return strategy_bot_service.get_recommendations()
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")


@router.post("/config", response_model=StrategyBotStatus)
async def update_bot_config(config: StrategyBotConfig):
    try:
        return strategy_bot_service.update_config(config.model_dump())
    except Exception as e:
        logger.error(f"Error updating bot config: {e}")
        raise HTTPException(status_code=500, detail="Failed to update bot config")


@router.get("/learning-report", response_model=StrategyLearningReport)
async def get_learning_report():
    try:
        return strategy_bot_service.get_learning_report()
    except Exception as e:
        logger.error(f"Error getting learning report: {e}")
        raise HTTPException(status_code=500, detail="Failed to get learning report")
