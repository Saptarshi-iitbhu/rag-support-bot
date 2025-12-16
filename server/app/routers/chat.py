from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid
from ..database import get_db
from ..models import ChatSession, Message
from ..services.llm_service import generate_response, analyze_escalation

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    action: str = "reply" 

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        new_session = ChatSession(id=session_id)
        db.add(new_session)
        db.commit()
    else:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session:
            new_session = ChatSession(id=session_id)
            db.add(new_session)
            db.commit()

    user_msg = Message(session_id=session_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    history = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    messages_context = [{"role": msg.role, "content": msg.content} for msg in history]

    bot_reply_content = generate_response(messages_context)

    bot_msg = Message(session_id=session_id, role="assistant", content=bot_reply_content)
    db.add(bot_msg)
    db.commit()

    action = "reply"
    if await analyze_escalation(request.message, bot_reply_content):
        action = "escalate"

    return ChatResponse(response=bot_reply_content, session_id=session_id, action=action)

@router.get("/sessions/{session_id}")
async def get_history(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        return {"session_id": session_id, "messages": []}
    
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    return {"session_id": session_id, "messages": [{"role": m.role, "content": m.content, "timestamp": m.timestamp} for m in messages]}
