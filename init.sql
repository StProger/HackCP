CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    business_id TEXT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    need_manager BOOLEAN DEFAULT FALSE,
    model_name TEXT DEFAULT 'sbert',
    created_at TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow')
);

CREATE TABLE support_managers (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    telegram_id BIGINT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    fio_manager TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE dialogs (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    feedback_user TEXT,
    rating INTEGER,
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow')
);
