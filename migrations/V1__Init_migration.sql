CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    status VARCHAR(100),
    address VARCHAR(255),
    city VARCHAR(255)
);

INSERT INTO orders (order_id, status, address, city) VALUES
('d9e9218f-39b2-4384-a123-001122334455', 'delivered', 'st. Avtozavodskaya 22', 'Moscow'),
('fae6b0c9-30ef-4872-bd7e-123456789012', 'canceled', 'st. Tverskaya 14', 'Moscow'),
('c1b7405d-1dc6-4c9c-9a1b-abcdefabcdef', 'in transit', 'st. Pushkina 5', 'St. Petersburg'),
('bde44b4e-9427-4cbe-8b34-cccdddeeefff', 'delivered', 'st. Mira 23', 'Kazan'),
('ae832d2f-f9e4-455e-a93a-aabbccddeeff', 'canceled', 'st. Nevsky 88', 'St. Petersburg'),
('f2d66b3e-a8b2-4b6e-8b52-deadbeef1234', 'returned', 'st. Novaya 1', 'Moscow'),
('aa0d3e2e-f402-45ad-b27d-987654321000', 'in transit', 'st. Lenina 99', 'Rostov'),
('99d881d4-5e15-4d9d-bf62-a1a2b3c4d5e6', 'delivered', 'st. Sovetskaya 4', 'Sochi'),
('6cdbf1de-b456-4018-9323-112233445566', 'in transit', 'st. Centralnaya 12', 'Omsk'),
('1a2b3c4d-5f6e-7a8b-9c0d-123412341234', 'delivered', 'st. Kirova 2', 'Yekaterinburg');
