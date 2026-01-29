from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.dependencies import CurrentUser
from app.models import Conversation, User
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.ai import get_ai_response
from app.services.memory import get_memory_service
from app.services.documents import get_document_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
) -> ChatMessageResponse:
    """
    Send a text message to the AI coach.

    Requires authentication. Stores the conversation in the database
    and returns the AI response with suggestions.
    """
    memory_service = get_memory_service()
    
    relevant_memories = memory_service.search_relevant_memories(
        query=request.message,
        user_id=current_user.id,
        top_k=3,
        exclude_session=request.session_id
    )
    
    conversation_history = []
    
    if current_user.id:
        recent_conversations = (
            db.query(Conversation)
            .filter(
                Conversation.user_id == current_user.id
            )
            .order_by(desc(Conversation.created_at))
            .limit(10)
            .all()
        )
        
        for conv in reversed(recent_conversations):
            conversation_history.append({"role": "user", "content": conv.user_message})
            conversation_history.append({"role": "assistant", "content": conv.ai_response})

    from app.services.context import build_context_for_ai
    context_data = build_context_for_ai(current_user.id, db)

    if request.message.strip().startswith('/'):
        command = request.message.strip().lower()
        
        if command == '/patterns':
            from app.services.pattern_learning import PatternLearningService
            from app.services.exploration import ExplorationService
            
            learner = PatternLearningService(current_user.id, db)
            explorer = ExplorationService(current_user.id, db)
            
            confirmed = learner.get_confirmed_patterns(min_confidence=80)
            
            if not confirmed:
                ai_response = (
                    "I'm still learning about you! 📚\n\n"
                    "We need more conversations before I can identify solid patterns. "
                    "Keep chatting with me and I'll start to understand what works for you!"
                )
            else:
                ai_response = "🧠 **What I know about you** (80%+ confidence):\n\n"
                
                for pattern in confirmed:
                    cat_name = pattern['category'].replace('_', ' ').title()
                    ai_response += f"✅ **{cat_name}**\n"
                    ai_response += f"   {pattern['hypothesis']}\n"
                    ai_response += f"   _(Confidence: {pattern['confidence']}%)_\n\n"
                
                all_status = explorer.get_all_categories_status()
                learning = [c for c in all_status if c['confidence'] < 80]
                
                if learning:
                    ai_response += "📖 **Still learning about:**\n"
                    for cat in learning[:5]:
                        cat_name = cat['category'].replace('_', ' ').title()
                        ai_response += f"• {cat_name} ({cat['confidence']}%)\n"
                    
                    if len(learning) > 5:
                        ai_response += f"...and {len(learning) - 5} more\n"
                
                ai_response += "\nUse /explore to dive deeper into any area!"
            
            suggestions = []
            
        elif command.startswith('/explore'):
            from app.services.exploration import ExplorationService
            
            explorer = ExplorationService(current_user.id, db)
            
            parts = request.message.strip().split(maxsplit=1)
            category = parts[1] if len(parts) > 1 else None
            
            if category:
                category_data = explorer.get_category_by_name(category)
                if not category_data:
                    ai_response = f"❌ Couldn't find category matching '{category}'\n\nTry: /explore task_initiation or just /explore to let me pick!"
                    suggestions = []
                else:
                    questions = explorer.get_exploration_guidance(category_data['category_name'])
                    
                    ai_response = f"Let's explore: **{category_data['description']}**\n\n"
                    ai_response += f"Current understanding: {category_data['confidence']}%\n"
                    ai_response += f"Observations so far: {category_data['observations']}\n\n"
                    
                    if category_data['hypothesis']:
                        ai_response += f"💭 Working hypothesis:\n_{category_data['hypothesis']}_\n\n"
                    
                    ai_response += "Here are some questions to explore:\n"
                    for q in questions[:3]:
                        ai_response += f"• {q}\n"
                    
                    ai_response += "\nJust answer naturally - I'll learn from our conversation!"
                    suggestions = []
            else:
                category_data = explorer.pick_next_category()
                
                if not category_data:
                    ai_response = "✅ You're doing great! No urgent areas to explore right now."
                    suggestions = []
                else:
                    questions = explorer.get_exploration_guidance(category_data['category_name'])
                    
                    ai_response = f"Let's explore: **{category_data['description']}**\n\n"
                    ai_response += f"Current understanding: {category_data['confidence']}%\n"
                    ai_response += f"Observations so far: {category_data['observations']}\n\n"
                    
                    if category_data['hypothesis']:
                        ai_response += f"💭 Working hypothesis:\n_{category_data['hypothesis']}_\n\n"
                    
                    ai_response += "Here are some questions to explore:\n"
                    for q in questions[:3]:
                        ai_response += f"• {q}\n"
                    
                    ai_response += "\nJust answer naturally - I'll learn from our conversation!"
                    suggestions = []
        else:
            ai_response = get_ai_response(
                user_message=request.message,
                user_id=current_user.id,
                db=db,
                conversation_history=conversation_history,
                context=context_data,
                relevant_memories=relevant_memories,
            )
            suggestions = []
    else:
        # DETECT AND APPLY FEEDBACK (if user is giving Sandy instructions)
        from app.services.feedback import detect_feedback, apply_feedback
        
        feedback_data = detect_feedback(request.message)
        feedback_confirmation = None
        
        if feedback_data['is_feedback']:
            feedback_confirmation = apply_feedback(feedback_data, current_user.id, db)
            print(f"Applied feedback: {feedback_data['instruction']}")
        
        ai_response = get_ai_response(
            user_message=request.message,
            user_id=current_user.id,
            db=db,
            conversation_history=conversation_history,
            context=context_data,
            relevant_memories=relevant_memories,
        )
        
        # Add feedback confirmation to response if present
        if feedback_confirmation:
            ai_response = f"{feedback_confirmation}\n\n{ai_response}" if ai_response else feedback_confirmation
        
        suggestions = []

    # REAL-TIME LEARNING - Extract and save patterns immediately (SAME AS TELEGRAM)
    from app.services.learning_extraction import extract_and_save_learnings
    from app.services.ai_actions import extract_actions_from_response
    
    # Check if any actions were executed
    actions_taken = extract_actions_from_response(ai_response)
    action_result = {'success': bool(actions_taken), 'actions': actions_taken} if actions_taken else None
    
    learnings = extract_and_save_learnings(
        user_message=request.message,
        ai_response=ai_response,
        user_id=current_user.id,
        db=db,
        action_result=action_result
    )
    
    if learnings:
        print(f"Web chat: Extracted {len(learnings)} learnings from interaction")

    conversation = Conversation(
        user_id=current_user.id,
        session_id=f"user_{current_user.id}_global",
        user_message=request.message,
        ai_response=ai_response,
        input_type="web",
        context=None,
        suggestions=suggestions,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    try:
        memory_service.store_conversation(
            conversation_id=conversation.id,
            user_id=current_user.id,
            user_message=request.message,
            ai_response=ai_response,
            session_id=f"user_{current_user.id}_global"
        )
    except Exception as e:
        print(f"Failed to store conversation in Pinecone: {e}")

    return ChatMessageResponse(
        conversation_id=conversation.id,
        ai_response=ai_response,
        suggestions=suggestions,
        created_at=conversation.created_at,
    )


@router.post("/upload-document")
async def upload_document(
    current_user: CurrentUser,
    file: UploadFile = File(...),
):
    allowed_extensions = ['pdf', 'docx', 'doc', 'txt', 'md']
    file_ext = file.filename.split('.')[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    file_bytes = await file.read()
    doc_type = "research" if file_ext == 'pdf' else "personal"
    
    doc_service = get_document_service()
    result = doc_service.process_document(
        file_bytes=file_bytes,
        filename=file.filename,
        user_id=current_user.id,
        doc_type=doc_type
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to process document")
        )
    
    message = f"**Document uploaded!** I've learned from `{file.filename}`.\n\n"
    message += f"- Stored {result['chunks_stored']} chunks\n"
    message += f"- {result['total_chars']} characters\n"
    message += f"- Type: {doc_type}\n\n"
    message += "I can now reference this information in our conversations."
    
    return {"message": message}


@router.post("/upload-url")
async def upload_url(
    request: dict,
    current_user: CurrentUser,
):
    url = request.get("url")
    
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL is required"
        )
    
    if not url.startswith(('http://', 'https://')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL format. Must start with http:// or https://"
        )
    
    doc_service = get_document_service()
    result = doc_service.process_url(
        url=url,
        user_id=current_user.id,
        doc_type="research"
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to process URL")
        )
    
    message = f"**URL content loaded!** I've learned from:\n\n"
    message += f"**{result['title']}**\n\n"
    message += f"- Stored {result['chunks_stored']} chunks\n"
    message += f"- {result['total_chars']} characters\n"
    message += f"- Source: {url}\n\n"
    message += "I can now reference this information in our conversations."
    
    return {"message": message}


@router.get("/get-prompt")
async def get_prompt(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    from app.services.ai import build_system_prompt
    
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    prompt = build_system_prompt(user.adhd_profile or {})
    
    return {"prompt": prompt}


@router.post("/update-prompt")
async def update_prompt(
    request: dict,
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
):
    new_prompt = request.get("prompt")
    
    if not new_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt is required"
        )
    
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.adhd_profile:
        user.adhd_profile = {}
    
    user.adhd_profile["custom_system_prompt"] = new_prompt
    db.commit()
    
    return {"message": "Prompt updated successfully"}
