from  datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel


class FormStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"

class FormFields(BaseModel):
    field1: Any
    field2: Any
    field3: Any

class Form(BaseModel):
    id: str
    form: FormFields
    status: FormStatus
    last_updated: datetime | None = None

class CreateFormRequest(BaseModel):
    form: FormFields
    status: FormStatus = FormStatus.DRAFT

class CreateFormResponse(BaseModel):
    id: str
    status: FormStatus = FormStatus.DRAFT

class UpdateFormRequest(BaseModel):
    form: FormFields

class UpdateForm(UpdateFormRequest):
    last_updated: datetime | None = None

class SubmitFormRequest(BaseModel):
    id: str
    form: FormFields

class SubmitForm(SubmitFormRequest):
    status: FormStatus = FormStatus.SUBMITTED
    last_updated: datetime | None = None
