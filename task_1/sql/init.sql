-- 1. SETUP SCHEMA SUMBER
CREATE SCHEMA IF NOT EXISTS source;
CREATE TABLE source.retail_transactions (
    id VARCHAR(50) PRIMARY KEY,        -- receipt id [cite: 7]
    customer_id VARCHAR(50),           -- [cite: 7]
    last_status VARCHAR(50),           -- Last Status of the package [cite: 7]
    pos_origin VARCHAR(100),           -- [cite: 7]
    pos_destination VARCHAR(100),      -- [cite: 7]
    created_at TIMESTAMP,              -- Fill when receipt is created [cite: 7]
    updated_at TIMESTAMP,              -- Created or updated [cite: 7]
    deleted_at TIMESTAMP               -- Filled when status DONE then deleted [cite: 7]
);

-- 2. SETUP SCHEMA WAREHOUSE
CREATE SCHEMA IF NOT EXISTS warehouse;
CREATE TABLE warehouse.retail_transactions (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    last_status VARCHAR(50),
    pos_origin VARCHAR(100),
    pos_destination VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    dw_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Kolom audit internal
);

-- 3. GENERATE DUMMY DATA [cite: 7]
INSERT INTO source.retail_transactions (id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at)
VALUES 
('LP001', 'CUST_A', 'IN_TRANSIT', 'JAKARTA', 'SURABAYA', NOW() - INTERVAL '2 hours', NOW() - INTERVAL '2 hours', NULL),
('LP002', 'CUST_B', 'DONE', 'BANDUNG', 'MEDAN', NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour', NOW()), -- Contoh Soft Delete 
('LP003', 'CUST_C', 'PICKUP', 'SEMARANG', 'BALI', NOW(), NOW(), NULL);