import json

from firebase_functions import https_fn
from firebase_admin import initialize_app

from shared_functions.main import SM_FUNCTION_post_parser_config, SM_FUNCTION_post_parser_imp

app = initialize_app()

@https_fn.on_request(min_instances=1)
def SM_FUNCTION_post_parser(request):
    request_json = request.get_json()
    content =  request_json['content'];
    parameters =  request_json['parameters'];
    
    config:SM_FUNCTION_post_parser_config = {
        "wandb_project": "st-demo-sandbox",
        "max_summary_length": 500,
        "openai_api_base": "https://openrouter.ai/api/v1",
    }
    
    meta = SM_FUNCTION_post_parser_imp(content, parameters, config)
    
    return https_fn.Response(
        json.dumps({"meta": meta }),
        status=200,
        headers={"Content-Type": "application/json"}
    )
    