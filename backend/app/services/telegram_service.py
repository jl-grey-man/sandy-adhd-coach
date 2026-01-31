"""Telegram bot service for ADHD Coach."""
import os
import logging
import re
import json
from typing import Optional
from datetime import datetime, time
import pytz

from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)


class TelegramService:
    """Service for managing Telegram bot interactions."""
    
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token)
        self.application = None
        
    async def initialize(self):
        """Initialize the Telegram application."""
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("explore", self.explore_command))
        self.application.add_handler(CommandHandler("patterns", self.patterns_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Initialize the application
        await self.application.initialize()
        await self.application.start()
        
        logger.info("Telegram bot initialized successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        
        # Link this Telegram account to user
        db = next(get_db())
        try:
            # For now, link to the test user (user@example.com)
            # Later: implement proper linking flow
            user = db.query(User).filter(User.email == "user@example.com").first()
            if user:
                user.telegram_chat_id = chat_id
                user.telegram_username = username
                db.commit()
                
                await update.message.reply_text(
                    "🤖 *ADHD Coach Connected!*\n\n"
                    f"Morning briefing set for {user.morning_briefing_time}\n"
                    "I'll send you:\n"
                    "• Daily focus recommendations\n"
                    "• Task confirmations\n"
                    "• Smart reminders\n\n"
                    "Just message me anytime!",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "⚠️ Could not find your account. Please log in to the web app first."
                )
        finally:
            db.close()
    
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command."""
        chat_id = update.effective_chat.id
        
        db = next(get_db())
        try:
            user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if user:
                user.telegram_chat_id = None
                user.telegram_username = None
                db.commit()
                
                await update.message.reply_text(
                    "👋 Disconnected. Use /start to reconnect anytime."
                )
        finally:
            db.close()
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "*ADHD Coach Commands:*\n\n"
            "/start - Connect your account\n"
            "/stop - Disconnect\n"
            "/explore - Dive into specific patterns I'm learning\n"
            "/patterns - See what I know about you\n"
            "/help - Show this message\n\n"
            "Just message me naturally - I understand conversation!",
            parse_mode='Markdown'
        )
    
    async def explore_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /explore command - learn about specific pattern categories."""
        chat_id = update.effective_chat.id
        args = context.args or []
        
        db = next(get_db())
        try:
            user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not user:
                await update.message.reply_text("⚠️ Please use /start first.")
                return
            
            from app.services.exploration import ExplorationService
            
            explorer = ExplorationService(user.id, db)
            
            # Check if user specified a category
            if args:
                category_name = " ".join(args)
                category = explorer.get_category_by_name(category_name)
                
                if not category:
                    await update.message.reply_text(
                        f"❌ Couldn't find category matching '{category_name}'\n\n"
                        "Try: /explore task_initiation or just /explore to let me pick!"
                    )
                    return
            else:
                # Pick next category to explore
                category = explorer.pick_next_category()
                
                if not category:
                    await update.message.reply_text(
                        "✅ You're doing great! No urgent areas to explore right now."
                    )
                    return
            
            # Get questions for this category
            questions = explorer.get_exploration_guidance(category['category_name'])
            
            # Build message
            message = f"Let's explore: *{category['description']}*\n\n"
            message += f"Current understanding: {category['confidence']}%\n"
            message += f"Observations so far: {category['observations']}\n\n"
            
            if category['hypothesis']:
                message += f"💭 Working hypothesis:\n_{category['hypothesis']}_\n\n"
            
            message += "Here are some questions to explore:\n"
            for q in questions[:3]:  # First 3 questions
                message += f"• {q}\n"
            
            message += "\nJust answer naturally - I'll learn from our conversation!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
        
        finally:
            db.close()
    
    async def patterns_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /patterns command - show what Sandy knows."""
        chat_id = update.effective_chat.id
        
        db = next(get_db())
        try:
            user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not user:
                await update.message.reply_text("⚠️ Please use /start first.")
                return
            
            # Use shared service (same as API)
            from app.services.pattern_learning import PatternLearningService
            from app.services.exploration import ExplorationService
            
            learner = PatternLearningService(user.id, db)
            explorer = ExplorationService(user.id, db)
            
            # Get confirmed patterns
            confirmed = learner.get_confirmed_patterns(min_confidence=80)
            
            if not confirmed:
                await update.message.reply_text(
                    "I'm still learning about you! 📚\n\n"
                    "We need more conversations before I can identify solid patterns.\n"
                    "Keep chatting with me and I'll start to understand what works for you!"
                )
                return
            
            message = "🧠 *What I know about you* (80%+ confidence):\n\n"
            
            for pattern in confirmed:
                cat_name = pattern['category'].replace('_', ' ').title()
                message += f"✅ *{cat_name}*\n"
                message += f"   {pattern['hypothesis']}\n"
                message += f"   _(Confidence: {pattern['confidence']}%)_\n\n"
            
            # Get categories still learning
            all_status = explorer.get_all_categories_status()
            learning = [c for c in all_status if c['confidence'] < 80]
            
            if learning:
                message += "📖 *Still learning about:*\n"
                for cat in learning[:5]:  # Show first 5
                    cat_name = cat['category'].replace('_', ' ').title()
                    message += f"• {cat_name} ({cat['confidence']}%)\n"
                
                if len(learning) > 5:
                    message += f"...and {len(learning) - 5} more\n"
            
            message += "\nUse /explore to dive deeper into any area!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
        
        finally:
            db.close()
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        chat_id = update.effective_chat.id
        user_message = update.message.text
        
        # Find user by Telegram chat_id
        db = next(get_db())
        try:
            user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not user:
                await update.message.reply_text(
                    "⚠️ Please use /start to connect your account first."
                )
                return
            
            # Get AI response
            from app.services.ai import get_ai_response
            from app.services.ai_actions import extract_actions_from_response, execute_action
            from app.services.context import build_context_for_ai, format_context_for_prompt
            
            # Get user profile
            user_profile = user.adhd_profile or {}
            
            # Get current context (projects, tasks, etc.)
            context_data = build_context_for_ai(user.id, db)
            context_str = format_context_for_prompt(context_data)
            
            # Get relevant long-term memories using Pinecone (SAME AS WEB CHAT)
            from app.services.memory import get_memory_service
            memory_service = get_memory_service()
            
            relevant_memories = memory_service.search_relevant_memories(
                query=user_message,
                user_id=user.id,
                top_k=3,
                exclude_session=f"user_{user.id}_global"
            )
            
            # Get recent conversation history (last 10 messages from ANY interface)
            from app.models.conversation import Conversation
            from datetime import datetime, timedelta
            from app.services.pattern_learning import PatternLearningService  # CORRECT learning system
            
            # FIXED: Removed 2-hour time limit - get ALL recent conversations
            recent_convos = db.query(Conversation).filter(
                Conversation.user_id == user.id
            ).order_by(Conversation.created_at.desc()).limit(10).all()
            
            # Build conversation history (most recent first, so reverse it)
            conversation_history = []
            for conv in reversed(recent_convos):
                conversation_history.append({"role": "user", "content": conv.user_message})
                conversation_history.append({"role": "assistant", "content": conv.ai_response})
            
            # Call AI service with context data (includes learned patterns) AND relevant memories
            response = get_ai_response(
                user_message=user_message,
                user_id=user.id,
                db=db,
                conversation_history=conversation_history,
                context=context_data,  # This now includes learned_patterns and exploration_status
                relevant_memories=relevant_memories  # Long-term memory from Pinecone
            )
            
            # DEBUG: Log the raw response
            logger.info(f"Raw AI response: {response}")
            
            # DETECT AND APPLY FEEDBACK (if user is giving Sandy instructions)
            from app.services.feedback import detect_feedback, apply_feedback
            
            feedback_data = detect_feedback(user_message)
            feedback_confirmation = None
            
            if feedback_data['is_feedback']:
                feedback_confirmation = apply_feedback(feedback_data, user.id, db)
                logger.info(f"Applied feedback: {feedback_data['instruction']}")
            
            # Extract and execute any actions from response
            actions = extract_actions_from_response(response)
            logger.info(f"Extracted actions: {actions}")
            
            # Also try to parse raw JSON if AI didn't use code blocks
            if not actions:
                # Look for raw JSON objects at start of response
                json_pattern = r'^[✅❌]?\s*[A-Z_]+\s*\{.*?\}\s*\n'
                match = re.match(json_pattern, response, re.DOTALL)
                if match:
                    try:
                        json_str = match.group(0).strip()
                        # Remove emoji and label
                        json_str = re.sub(r'^[✅❌]?\s*[A-Z_]+\s*', '', json_str)
                        action = json.loads(json_str)
                        actions = [action]
                    except:
                        pass
            
            # Clean response FIRST - remove action blocks
            clean_response = response
            
            # Remove ```action blocks (with proper newlines)
            clean_response = re.sub(r'```action\s*\n.*?\n```', '', clean_response, flags=re.DOTALL)
            
            # Remove any remaining ```action blocks without closing
            clean_response = re.sub(r'```action\s*\n.*', '', clean_response, flags=re.DOTALL)
            
            # Remove raw JSON at start
            clean_response = re.sub(r'^[✅❌]?\s*[A-Z_]+\s*\{.*?\}\s*\n', '', clean_response, flags=re.DOTALL)
            
            clean_response = clean_response.strip()
            
            # Add feedback confirmation if user gave feedback
            if feedback_confirmation:
                clean_response = f"{feedback_confirmation}\n\n{clean_response}" if clean_response else feedback_confirmation
            
            logger.info(f"Cleaned response: {clean_response}")
            
            # HANDLE AI ACTIONS (like reminder creation)
            from app.services.context import handle_ai_actions
            clean_response = await handle_ai_actions(clean_response, user.id, db)
            
            # SEND HUMAN RESPONSE FIRST
            if clean_response:
                await update.message.reply_text(clean_response)
            
            # THEN send action confirmations
            action_result = None
            for action in actions:
                result = execute_action(action, user.id, db)
                action_result = result  # Store for learning
                
                if result["success"]:
                    # Send confirmation message
                    await self.send_action_confirmation(
                        user_id=user.id,
                        action_type=result["action_type"],
                        details=result["details"]
                    )
            
            # REAL-TIME LEARNING - Extract and save patterns immediately
            from app.services.learning_extraction import extract_and_save_learnings
            
            learnings = extract_and_save_learnings(
                user_message=user_message,
                ai_response=clean_response or response,
                user_id=user.id,
                db=db,
                action_result=action_result
            )
            
            if learnings:
                logger.info(f"Extracted {len(learnings)} learnings from interaction")
            
            # Save conversation to database for history
            # Use user-based session_id for cross-platform sync
            from app.models.conversation import Conversation
            conversation = Conversation(
                user_id=user.id,
                user_message=user_message,
                ai_response=clean_response or response,
                session_id=f"user_{user.id}_global",  # SHARED session across all interfaces
                input_type="telegram"
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            # Store to Pinecone for long-term memory (SAME AS WEB CHAT)
            try:
                memory_service.store_conversation(
                    conversation_id=conversation.id,
                    user_id=user.id,
                    user_message=user_message,
                    ai_response=clean_response or response,
                    session_id=f"user_{user.id}_global"
                )
            except Exception as e:
                logger.error(f"Failed to store conversation in Pinecone: {e}")
            
        finally:
            db.close()
    
    async def send_message(self, chat_id: int, message: str, parse_mode: Optional[str] = None):
        """Send a message to a specific chat."""
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info(f"Sent message to chat {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send message to chat {chat_id}: {e}")
    
    async def send_morning_briefing(self, user_id: int):
        """Send morning briefing to a user."""
        db = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.telegram_chat_id:
                return
            
            # Generate briefing content
            from app.services.ai import generate_morning_briefing
            briefing = await generate_morning_briefing(user_id, db)
            
            # Format with emojis
            formatted_briefing = (
                "🌅 *GOOD MORNING*\n\n"
                f"{briefing}\n\n"
                "_Reply to add tasks or ask questions_"
            )
            
            await self.send_message(
                chat_id=user.telegram_chat_id,
                message=formatted_briefing,
                parse_mode='Markdown'
            )
            
        finally:
            db.close()
    
    async def send_action_confirmation(self, user_id: int, action_type: str, details: dict):
        """Send action confirmation message."""
        db = next(get_db())
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.telegram_chat_id:
                return
            
            # Format based on action type
            if action_type == "create_reminder":
                message = (
                    "⏰ *REMINDER SET*\n"
                    f"💬 {details.get('message')}\n"
                    f"🕐 Will remind you at {details.get('remind_at')}\n"
                )
            
            elif action_type == "calendar_event":
                message = (
                    "✅ *ADDED TO CALENDAR*\n"
                    f"📅 {details.get('title')}\n"
                    f"🕐 {details.get('start_time')}\n"
                )
                if details.get('location'):
                    message += f"📍 {details.get('location')}\n"
            
            elif action_type == "create_task":
                message = (
                    "✅ *ADDED TASK*\n"
                    f"🎯 {details.get('title')}\n"
                )
                if details.get('priority'):
                    message += f"🔥 Priority: {details.get('priority')}\n"
                if details.get('estimated_minutes'):
                    message += f"⏱️ Est. time: {details.get('estimated_minutes')} min\n"
            
            elif action_type == "create_project":
                message = (
                    "✅ *CREATED PROJECT*\n"
                    f"📋 {details.get('title')}\n"
                )
                if details.get('deadline'):
                    message += f"⏰ Deadline: {details.get('deadline')}\n"
                if details.get('estimated_hours'):
                    message += f"📊 Est. hours: {details.get('estimated_hours')}\n"
            
            elif action_type == "move_to_backburner":
                message = (
                    "💡 *MOVED TO BACKBURNER*\n"
                    f"🗂️ {details.get('title')}\n"
                    "📝 I'll remind you when the time is right\n"
                )
            
            else:
                message = f"✅ *{action_type.upper()}*\n{details}"
            
            await self.send_message(
                chat_id=user.telegram_chat_id,
                message=message,
                parse_mode='Markdown'
            )
            
        finally:
            db.close()


# Global telegram service instance
_telegram_service: Optional[TelegramService] = None


def get_telegram_service() -> TelegramService:
    """Get or create Telegram service instance."""
    global _telegram_service
    if _telegram_service is None:
        from app.config import get_settings
        settings = get_settings()
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in settings")
        _telegram_service = TelegramService(settings.telegram_bot_token)
    return _telegram_service
