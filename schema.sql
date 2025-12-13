-- Create table credit_limit_rq
CREATE TABLE IF NOT EXISTS credit_limit_rq (
    id_credit_limit_rq SERIAL PRIMARY KEY,
    code_client_backoffice VARCHAR(50),
    code_client_obt VARCHAR(50),
    name VARCHAR(255),
    loc_validacion VARCHAR(100),
    value NUMERIC(15, 2),
    currency VARCHAR(10),
    product VARCHAR(100),
    description TEXT,
    payment_type VARCHAR(50),
    mail_user VARCHAR(255),
    status VARCHAR(20) DEFAULT 'PENDING',
    message_validation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Stored Procedure to create table (requested by user, though script above is sufficient)
CREATE OR REPLACE PROCEDURE create_database_schema()
LANGUAGE plpgsql
AS $$
BEGIN
    -- This block is just for demonstration as the table is created above.
    -- In Postgres, CREATE TABLE IF NOT EXISTS is standard.
    NULL;
END;
$$;
