import json

from firebase_functions import https_fn
from firebase_admin import initialize_app

from shared_functions.main import SM_FUNCTION_post_parser_config, SM_FUNCTION_post_parser_imp
from config import openai_api_key

app = initialize_app()


@https_fn.on_request(min_instances=1)
def SM_FUNCTION_post_parser(request):
    """
    Wrapper on SM_FUNCTION_post_parser_imp
    """
    request_json = request.get_json()
    content = request_json["content"]
    parameters = request_json["parameters"]

    config: SM_FUNCTION_post_parser_config = {
        "wandb_project": "st-demo-sandbox",
        "max_summary_length": 500,
        "openai_api_key": openai_api_key,
        "openai_api_base": "https://openrouter.ai/api/v1",
        "openai_api_referer": "https://127.0.0.1:3000/",
    }

    # semantics = SM_FUNCTION_post_parser_imp(content, parameters, config)
    semantics = {
        "triplets": [
            "<_:1> <has-keyword> <happy>",
            "<_:1> <disagrees> <https://www.alink.com/>",
            "<_:1> <announce> <https://www.anotherlink.com/>",
        ]
    }

    return https_fn.Response(
        json.dumps({"semantics": semantics }),
        status=200,
        headers={"Content-Type": "application/json"}
    )
