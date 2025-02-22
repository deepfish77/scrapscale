import os


def lambda_handler(event, context):
    handler_name = os.getenv("HANDLER", "scrape")

    if handler_name == "app":
        return "this is where the handler be called"  # app_handler(event, context)
    elif handler_name == "scrape":
        return "This is where other handlers will be called"  # scrape_handler(event, context)
    else:
        raise ValueError(f"Unknown handler: {handler_name}")
