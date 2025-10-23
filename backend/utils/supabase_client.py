import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_TABLE = os.getenv('SUPABASE_TABLE','ai_tools')

_client = None

def get_client() -> Client:
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError('Supabase credentials missing in .env')
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client

def fetch_all_tools(columns='name,description,category,tags,url,rating,pricing,website'):
    client = get_client()
    res = client.table(SUPABASE_TABLE).select(columns).execute()
    return res.data or []
