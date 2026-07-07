-- Architecture Overhaul Migration (Final Frozen Blueprint)

-- 1. Drop Triggers & Trigger Functions
DROP TRIGGER IF EXISTS trigger_update_metrics_on_itinerary ON itineraries;
DROP TRIGGER IF EXISTS trigger_auto_training_data ON itineraries;
DROP FUNCTION IF EXISTS update_system_metrics();
DROP FUNCTION IF EXISTS auto_create_training_data();
DROP FUNCTION IF EXISTS trigger_training_cycle();

-- 2. ENUMs
CREATE TYPE event_type AS ENUM ('PromptSubmitted', 'GenerationStarted', 'GenerationCompleted', 'Feedback', 'Export', 'Share', 'Retry', 'Failure');
CREATE TYPE queue_status AS ENUM ('pending', 'processing', 'failed', 'completed', 'dead');
CREATE TYPE model_status AS ENUM ('evaluation', 'approved', 'archived');

-- 3. Core Domain Tables
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS prompts_metadata (
    id SERIAL PRIMARY KEY,
    version_name TEXT UNIQUE NOT NULL,
    checksum TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS training_queue (
    id SERIAL PRIMARY KEY,
    itinerary_id INT,
    status queue_status DEFAULT 'pending',
    retry_count INT DEFAULT 0,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    duration INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS config_evaluations (
    id SERIAL PRIMARY KEY,
    model_version_id INT REFERENCES model_versions(id),
    score FLOAT,
    passed BOOLEAN,
    structural_metrics JSONB,
    semantic_metrics JSONB,
    evaluated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. Update Existing Tables
ALTER TABLE itineraries 
    ADD COLUMN IF NOT EXISTS conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    ADD COLUMN IF NOT EXISTS prompt_id INT REFERENCES prompts_metadata(id),
    ADD COLUMN IF NOT EXISTS model_version_id INT REFERENCES model_versions(id),
    ADD COLUMN IF NOT EXISTS configuration_snapshot JSONB;

ALTER TABLE training_queue ADD CONSTRAINT fk_tq_itinerary FOREIGN KEY (itinerary_id) REFERENCES itineraries(id) ON DELETE CASCADE;

-- 5. Views
CREATE OR REPLACE VIEW dashboard_metrics AS
SELECT
    (SELECT COUNT(*) FROM conversations) AS total_conversations,
    (SELECT AVG(rating) FROM itineraries WHERE rating > 0) AS average_rating,
    (SELECT AVG(quality_score) FROM itineraries WHERE quality_score IS NOT NULL) AS average_quality,
    (SELECT AVG(generation_time_ms) FROM itineraries WHERE generation_time_ms IS NOT NULL) AS average_generation_time_ms,
    (SELECT COUNT(*) FROM itineraries WHERE configuration_snapshot IS NULL) AS generation_failures;
