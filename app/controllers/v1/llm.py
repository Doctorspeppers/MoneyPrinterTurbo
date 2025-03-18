from fastapi import Request
from fastapi import Header, HTTPException, Depends

from app.controllers.v1.base import new_router
from app.models.schema import (
    VideoScriptRequest,
    VideoScriptResponse,
    VideoTermsRequest,
    VideoTermsResponse,
)
from app.services import llm
from app.utils import utils
from app.config import config


# authentication dependency
# router = new_router(dependencies=[Depends(base.verify_token)])
router = new_router()

API_KEY = config.app.get("api_key", "meu_super_secreto_token")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


@router.post(
    "/scripts",
    response_model=VideoScriptResponse,
    summary="Create a script for the video",
    dependencies=[Depends(verify_api_key)]
)
def generate_video_script(request: Request, body: VideoScriptRequest):
    video_script = llm.generate_script(
        video_subject=body.video_subject,
        language=body.video_language,
        paragraph_number=body.paragraph_number,
    )
    response = {"video_script": video_script}
    return utils.get_response(200, response)


@router.post(
    "/terms",
    response_model=VideoTermsResponse,
    summary="Generate video terms based on the video script",
    dependencies=[Depends(verify_api_key)]
)
def generate_video_terms(request: Request, body: VideoTermsRequest):
    video_terms = llm.generate_terms(
        video_subject=body.video_subject,
        video_script=body.video_script,
        amount=body.amount,
    )
    response = {"video_terms": video_terms}
    return utils.get_response(200, response)
