-- ==============================================================================
-- Traveler LLM - Complete Initial Database Schema (Domain-Driven Design)
-- Version: 5.0.0 (Unified Blueprint)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. ENUMS & TYPES
-- ------------------------------------------------------------------------------
CREATE TYPE event_type AS ENUM ('PromptSubmitted', 'GenerationStarted', 'GenerationCompleted', 'Feedback', 'Export', 'Share', 'Retry', 'Failure');
CREATE TYPE queue_status AS ENUM ('pending', 'processing', 'failed', 'completed', 'dead');
CREATE TYPE model_status AS ENUM ('evaluation', 'approved', 'archived');

-- ------------------------------------------------------------------------------
-- 2. CORE DOMAIN TABLES
-- ------------------------------------------------------------------------------

-- Users (Base Identity)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Conversations (Session Tracking)
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Events (Event Sourcing Log)
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    correlation_id TEXT NOT NULL,
    event_type event_type NOT NULL,
    occurred_at TIMESTAMP DEFAULT NOW(),
    actor TEXT DEFAULT 'system',
    payload JSONB NOT NULL,
    version TEXT DEFAULT '1.0'
);
CREATE INDEX IF NOT EXISTS idx_events_conversation_id ON events(conversation_id);
CREATE INDEX IF NOT EXISTS idx_events_correlation_id ON events(correlation_id);

-- Prompts Metadata
CREATE TABLE IF NOT EXISTS prompts_metadata (
    id SERIAL PRIMARY KEY,
    version_name TEXT UNIQUE NOT NULL,
    checksum TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Datasets (Versioned Training Data)
CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    version_name TEXT UNIQUE NOT NULL,
    sample_count INT DEFAULT 0,
    average_quality FLOAT DEFAULT 0.0,
    language TEXT DEFAULT 'en',
    source TEXT DEFAULT 'feedback',
    parent_dataset_id INT REFERENCES datasets(id),
    created_by_pipeline_version TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Model Versions (Inference Configurations)
CREATE TABLE IF NOT EXISTS model_versions (
    id SERIAL PRIMARY KEY,
    version_name TEXT UNIQUE NOT NULL,
    provider TEXT NOT NULL DEFAULT 'Groq',
    provider_model TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    dataset_version TEXT NOT NULL,
    previous_version_id INT REFERENCES model_versions(id),
    status model_status DEFAULT 'evaluation',
    release_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- System Config (Singleton defining active configuration)
CREATE TABLE IF NOT EXISTS system_config (
    id INT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    config_version TEXT NOT NULL,
    active_model_id INT REFERENCES model_versions(id),
    active_prompt_id INT REFERENCES prompts_metadata(id),
    active_dataset_id INT REFERENCES datasets(id),
    retry_schedule JSONB DEFAULT '{"1": 60, "2": 300, "3": 900, "4": 3600}',
    learning_enabled BOOLEAN DEFAULT TRUE,
    evaluation_enabled BOOLEAN DEFAULT TRUE,
    exports_enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by TEXT DEFAULT 'system'
);

-- Trips (User Intent Parameters)
CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    destination TEXT NOT NULL,
    interests TEXT[] NOT NULL,
    duration INT NOT NULL CHECK (duration > 0),
    budget_level TEXT NOT NULL CHECK (budget_level IN ('Budget', 'Moderate', 'Luxury')),
    travel_style TEXT[] NOT NULL,
    include_food BOOLEAN DEFAULT TRUE,
    include_transport BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_trips_destination ON trips(destination);

-- Itineraries (LLM Generated Outputs)
CREATE TABLE IF NOT EXISTS itineraries (
    id SERIAL PRIMARY KEY,
    trip_id INT REFERENCES trips(id) ON DELETE CASCADE,
    conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    prompt_id INT REFERENCES prompts_metadata(id),
    model_version_id INT REFERENCES model_versions(id),
    itinerary_text TEXT NOT NULL,
    configuration_snapshot JSONB,
    word_count INT,
    character_count INT,
    rating INT CHECK (rating >= 0 AND rating <= 5),
    feedback_comments TEXT,
    quality_score FLOAT,
    generation_time_ms INT,
    created_at TIMESTAMP DEFAULT NOW(),
    rated_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_itineraries_trip_id ON itineraries(trip_id);
CREATE INDEX IF NOT EXISTS idx_itineraries_rating ON itineraries(rating DESC);

-- Training Data (High Quality Samples for Fine-Tuning)
CREATE TABLE IF NOT EXISTS training_data (
    id SERIAL PRIMARY KEY,
    trip_id INT REFERENCES trips(id) ON DELETE CASCADE,
    itinerary_id INT REFERENCES itineraries(id) ON DELETE CASCADE,
    dataset_id INT REFERENCES datasets(id),
    raw_input JSONB NOT NULL,
    raw_output JSONB NOT NULL,
    input_hash TEXT UNIQUE,
    quality_score FLOAT,
    is_high_quality BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_training_data_quality ON training_data(quality_score DESC);

-- Training Queue (Background Worker Instructions)
CREATE TABLE IF NOT EXISTS training_queue (
    id SERIAL PRIMARY KEY,
    itinerary_id INT REFERENCES itineraries(id) ON DELETE CASCADE,
    status queue_status DEFAULT 'pending',
    retry_count INT DEFAULT 0,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    duration INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_training_queue_status ON training_queue(status);

-- Config Evaluations (Automated LLM Grading)
CREATE TABLE IF NOT EXISTS config_evaluations (
    id SERIAL PRIMARY KEY,
    model_version_id INT REFERENCES model_versions(id),
    score FLOAT,
    passed BOOLEAN,
    structural_metrics JSONB,
    semantic_metrics JSONB,
    evaluated_at TIMESTAMP DEFAULT NOW()
);

-- Audit Logs (System Administrative Actions)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);


-- ------------------------------------------------------------------------------
-- 3. VIEWS
-- ------------------------------------------------------------------------------

-- Dashboard Metrics
CREATE OR REPLACE VIEW dashboard_metrics AS
SELECT
    (SELECT COUNT(*) FROM conversations) AS total_conversations,
    (SELECT AVG(rating) FROM itineraries WHERE rating > 0) AS average_rating,
    (SELECT AVG(quality_score) FROM itineraries WHERE quality_score IS NOT NULL) AS average_quality,
    (SELECT AVG(generation_time_ms) FROM itineraries WHERE generation_time_ms IS NOT NULL) AS average_generation_time_ms,
    (SELECT COUNT(*) FROM itineraries WHERE configuration_snapshot IS NULL) AS generation_failures;

-- Popular Destinations
CREATE OR REPLACE VIEW popular_destinations AS
SELECT 
    destination,
    COUNT(*) as trip_count,
    AVG(COALESCE(i.rating, 0)) as avg_rating
FROM trips t
LEFT JOIN itineraries i ON t.id = i.trip_id
GROUP BY destination
ORDER BY trip_count DESC, avg_rating DESC;


-- ------------------------------------------------------------------------------
-- 4. TRAINING ORIENTED HELPER FUNCTIONS (No Side Effects)
-- ------------------------------------------------------------------------------

-- Calculate normalized quality score without an ML model
CREATE OR REPLACE FUNCTION calculate_quality_score(
    p_rating INT, 
    p_edited BOOLEAN DEFAULT false, 
    p_exported BOOLEAN DEFAULT false
) RETURNS FLOAT AS $$
DECLARE
    score FLOAT := 0;
BEGIN
    -- Base score from rating (0-100)
    IF p_rating IS NOT NULL THEN
        score := (p_rating::FLOAT / 5.0) * 80;
    END IF;
    
    -- Bonus points for behavioral markers
    IF p_edited THEN score := score + 10; END IF;
    IF p_exported THEN score := score + 10; END IF;
    
    RETURN LEAST(score, 100.0);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Extract structured training sample for the learning pipeline
CREATE OR REPLACE FUNCTION extract_training_sample(p_itinerary_id INT)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT jsonb_build_object(
        'input', jsonb_build_object(
            'destination', t.destination,
            'interests', t.interests,
            'duration', t.duration,
            'budget_level', t.budget_level,
            'travel_style', t.travel_style
        ),
        'output', jsonb_build_object(
            'itinerary_text', i.itinerary_text,
            'rating', i.rating,
            'feedback', i.feedback_comments
        ),
        'metadata', jsonb_build_object(
            'quality_score', i.quality_score,
            'model_used', m.provider_model
        )
    ) INTO result
    FROM itineraries i
    JOIN trips t ON i.trip_id = t.id
    LEFT JOIN model_versions m ON i.model_version_id = m.id
    WHERE i.id = p_itinerary_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql STABLE;


-- ------------------------------------------------------------------------------
-- 5. INITIAL SEED DATA
-- ------------------------------------------------------------------------------

-- Seed Anonymous User
INSERT INTO users (id, email, username) 
VALUES (1, 'anonymous@travelplanner.ai', 'Anonymous User')
ON CONFLICT (id) DO NOTHING;

-- Seed Baseline Prompt
INSERT INTO prompts_metadata (id, version_name, is_active)
VALUES (1, 'v1', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Seed Baseline Dataset
INSERT INTO datasets (id, version_name, language)
VALUES (1, 'ds-v1', 'en')
ON CONFLICT (id) DO NOTHING;

-- Seed Baseline Model Configuration
INSERT INTO model_versions (id, version_name, provider, provider_model, prompt_version, dataset_version, status)
VALUES (1, 'travel-v1', 'Groq', 'llama-3.3-70b-versatile', 'v1', 'ds-v1', 'approved')
ON CONFLICT (id) DO NOTHING;

-- Seed System Config (linking everything together)
INSERT INTO system_config (id, config_version, active_model_id, active_prompt_id, active_dataset_id)
VALUES (1, '1.0', 1, 1, 1)
ON CONFLICT (id) DO UPDATE SET 
    active_model_id = 1,
    active_prompt_id = 1,
    active_dataset_id = 1;

COMMIT;
