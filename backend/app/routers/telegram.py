"""Telegram bot router."""
import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from telegram import Update

from app.services.telegram_service import get_telegram_service
from app.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates."""
    try:
        telegram_service = get_telegram_service()
        
        # Parse update
        json_data = await request.json()
        update = Update.de_json(json_data, telegram_service.bot)
        
        # Process update
        if telegram_service.application:
            await telegram_service.application.process_update(update)
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send")
async def send_message(
    chat_id: int,
    message: str,
    current_user = Depends(get_current_user)
):
    """Send a message via Telegram bot."""
    try:
        telegram_service = get_telegram_service()
        await telegram_service.send_message(chat_id, message)
        return {"status": "sent"}
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/action-confirmation")
async def send_action_confirmation(
    action_type: str,
    details: dict,
    current_user = Depends(get_current_user)
):
    """Send action confirmation to user's Telegram."""
    try:
        telegram_service = get_telegram_service()
        await telegram_service.send_action_confirmation(
            user_id=current_user.id,
            action_type=action_type,
            details=details
        )
        return {"status": "sent"}
    except Exception as e:
        logger.error(f"Error sending action confirmation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
