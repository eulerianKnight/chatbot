import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import Optional, List

from models.user import User
from models.configurations import Configuration
from dependencies import get_db
from schemas.schema import ConfigurationCreate
from dependencies import get_current_user

# Directory to store uploaded files
UPLOAD_DIRECTORY = "./uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

config_router = APIRouter()


def is_admin(user: User):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

@config_router.post("/admin/configurations", response_model=dict)
def create_configuration(
    agent_name: str = Form(...),
    model: str = Form(...),
    temperature: Optional[float] = Form(0.0),
    system_message: Optional[str] = Form(""),
    tools: Optional[str] = Form(""),
    presence_penalty: Optional[float] = Form(0.0),
    frequency_penalty: Optional[float] = Form(0.0),
    top_p: Optional[float] = Form(0.0),
    max_tokens: Optional[int] = Form(8192),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_admin(current_user)

    configs = Configuration(
        agent_name=agent_name, 
        max_tokens=max_tokens, 
        top_p=top_p, 
        model=model, 
        tools=tools, 
        temperature=temperature, 
        presence_penalty=presence_penalty, 
        frequency_penalty=frequency_penalty, 
        system_prompt=system_message, 
        agent_url=f"http://localhost:3000?agentName={agent_name}"
    )
    db.add(configs)
    db.commit()
    db.refresh(configs)
    return {"message": "Configuration created", "url": configs.agent_url}
