from uuid import uuid4

def generate_asset_id() -> str:
    return str(uuid4())