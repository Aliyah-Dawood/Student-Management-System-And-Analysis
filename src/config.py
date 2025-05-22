
from supabase import create_client

SUPABASE_URL = "https://gfjignmiiqcaxvqvsyif.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdmamlnbm1paXFjYXh2cXZzeWlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYwMDQ5NjMsImV4cCI6MjA2MTU4MDk2M30.LVfIOIriYPOuz8YVFXJ5uKtdIWubJ_ra-PJDt8qEjA8"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
