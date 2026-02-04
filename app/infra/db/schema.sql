-- scenarios table
CREATE TABLE IF NOT EXISTS scenarios (
  id TEXT PRIMARY KEY,
  version TEXT NOT NULL,
  crime_type TEXT NOT NULL,
  description TEXT,
  steps JSONB NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT now()
);

-- sessions table
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  scenario_id TEXT NOT NULL,
  current_step TEXT,
  started_at TIMESTAMP DEFAULT now(),
  ended_at TIMESTAMP
);

-- events table
CREATE TABLE IF NOT EXISTS events (
  id UUID PRIMARY KEY,
  session_id TEXT NOT NULL,
  step_id TEXT,
  event_type TEXT NOT NULL,
  payload JSONB,
  created_at TIMESTAMP DEFAULT now()
);
