import json
import logging
from backend.db import supabase_public as supabase_public



def fetch_dynamic_promos():
    try:
        response = supabase_public.from_("promos").select("*").execute()
        data = response.model_dump_json()
        return json.loads(data).get("data", [])
    except Exception as e:
        logging.error(f"Error fetching dynamic promos: {e}")
        return []
