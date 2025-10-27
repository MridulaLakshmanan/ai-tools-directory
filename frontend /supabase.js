import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

export const supabase = createClient(
  'https://pjxrjytcurqrmbuhgyoi.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqeHJqeXRjdXJxcm1idWhneW9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExMjYxNTcsImV4cCI6MjA3NjcwMjE1N30.H5xP2ZlKFl_-h41I_ZjCcGmt0NLK64eOwO8Ipr2sfZQ'
);