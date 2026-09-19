-- ==========================================================
-- TECNOSOLUCIONES
-- SEMANA 13 - ESQUEMA DE BASE DE DATOS MYSQL
-- ==========================================================

CREATE DATABASE IF NOT EXISTS tecnosoluciones;

USE tecnosoluciones;


-- ==========================================================
-- TABLA: PROVEEDORES
-- ==========================================================

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    PRIMARY KEY (id_proveedor)
);


-- ==========================================================
-- TABLA: CLIENTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(20),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    PRIMARY KEY (id_cliente)
);


-- ==========================================================
-- TABLA: PRODUCTOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    id_proveedor INT,
    PRIMARY KEY (id_producto),
    CONSTRAINT fk_productos_proveedores
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
);


-- ==========================================================
-- TABLA: FACTURAS
-- ==========================================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT NOT NULL AUTO_INCREMENT,
    id_cliente INT,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_factura),
    CONSTRAINT fk_facturas_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);


-- ==========================================================
-- CONSULTA DE VERIFICACIÓN
-- ==========================================================

SHOW TABLES;