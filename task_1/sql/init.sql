CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS warehouse;

-- Tabel Sumber
CREATE TABLE source.retail_transactions (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    last_status VARCHAR(50),
    pos_origin VARCHAR(100),
    pos_destination VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_retail_updated_at ON source.retail_transactions (updated_at);

-- Tabel Warehouse
CREATE TABLE warehouse.retail_transactions (
    id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    last_status VARCHAR(50),
    pos_origin VARCHAR(100),
    pos_destination VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    dw_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Dummy
INSERT INTO source.retail_transactions (id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at)
VALUES 
('LP001', 'CUST_A', 'IN_TRANSIT', 'JAKARTA', 'SURABAYA', NOW() - INTERVAL '48 hours', NOW() - INTERVAL '48 hours', NULL),
('LP002', 'CUST_B', 'DONE', 'BANDUNG', 'MEDAN', NOW() - INTERVAL '3 hours', NOW(), NOW()), 
('LP003', 'CUST_C', 'PICKUP', 'SEMARANG', 'BALI', NOW(), NOW(), NULL);