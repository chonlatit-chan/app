from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from pymongo import ReturnDocument
from app.config import settings
from app.database import form_collection, counter_collection
from app.schemas.form import (
    Form, CreateFormRequest, CreateFormResponse, UpdateFormRequest,
    UpdateForm, SubmitFormRequest, SubmitForm)
from app.schemas.user import User
from app.routers.user import get_current_active_user


router = APIRouter()



@router.post("/request-drafts", response_model=CreateFormResponse)
async def create_form(input: CreateFormRequest):
    counter = counter_collection.find_one_and_update(
            {'collection': "forms"},
            {'$inc': {'seq_value' : 1}},
            upsert = True,
            return_document = ReturnDocument.AFTER)

    form_id = f"{settings.form_id_prefix}{counter['seq_value']}"

    drafting_form = Form(**input.model_dump(exclude = "status"),
                id = form_id,
                status = "DRAFT",
                last_updated = datetime.now(timezone.utc))

    form_collection.insert_one(drafting_form.model_dump())

    return {
        "id": drafting_form.id,
        "status": drafting_form.status
    }


@router.get("/request-drafts/{id}", response_model = Form | None)
async def read_form(id: str):
    return form_collection.find_one({"id": id, "status": "DRAFT"}, {"_id": False})


@router.put("/request-drafts/{id}")
async def update_form(id: str, input: UpdateFormRequest):
    updating_form = UpdateForm(**input.model_dump(),
                last_updated = datetime.now(timezone.utc))

    form_collection.update_one({"id": id, "status": "DRAFT"}, {"$set": updating_form.model_dump()})


@router.post("/request")
async def submit_form(input: SubmitFormRequest):
    submitting_form = SubmitForm(**input.model_dump(),
                last_updated = datetime.now(timezone.utc))

    form_collection.update_one({"id": input.id, "status": "DRAFT"},
                               {"$set": submitting_form.model_dump()})


@router.get("/request", response_model = list[Form])
async def list_form(___current_user: Annotated[User, Depends(get_current_active_user)]):
    docs = form_collection.find({"status": "SUBMITTED"}, {"_id": False})
    return list(docs)
