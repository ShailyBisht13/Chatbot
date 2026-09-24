# ai_router.py — ALIAS TO MAIN ROUTER
from router import ai_router as _main_ai_router

def ai_router(user_input, lang="en", persona="travel_guide", image_path=None, persona_name=None):
    effective_persona = persona_name if persona_name is not None else persona
    return _main_ai_router(
        user_input=user_input,
        lang=lang,
        persona=effective_persona,
        image_path=image_path
    )
