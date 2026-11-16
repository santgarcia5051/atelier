-- Base de datos única de Scantalia (Cloudflare D1: scantalia-pedidos).
-- 0001: clientes y contraseñas, códigos de verificación, sesiones, stock, envíos, reseñas,
-- quejas y precios de la competencia. Se aplica sobre la tabla `pedidos`, que ya existe.
-- Solo agrega tablas y una columna; no borra ni cambia datos existentes.

-- ── Clientes ─────────────────────────────────────────────────────────────
-- La contraseña NUNCA se guarda tal cual: pass_hash = "pbkdf2$<iteraciones>$<sal>$<hash>".
CREATE TABLE IF NOT EXISTS clientes (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  correo        TEXT NOT NULL UNIQUE COLLATE NOCASE,
  nombre        TEXT NOT NULL,
  telefono      TEXT,
  pass_hash     TEXT NOT NULL,
  verificado    INTEGER NOT NULL DEFAULT 0 CHECK (verificado IN (0, 1)),
  estado        TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'bloqueado')),
  creado_en     TEXT NOT NULL DEFAULT (datetime('now')),
  ultimo_acceso TEXT
);

CREATE TABLE IF NOT EXISTS direcciones (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id     INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
  calle          TEXT NOT NULL,
  colonia        TEXT NOT NULL,
  codigo_postal  TEXT NOT NULL CHECK (length(codigo_postal) = 5),
  ciudad         TEXT NOT NULL,
  referencias    TEXT,
  predeterminada INTEGER NOT NULL DEFAULT 0 CHECK (predeterminada IN (0, 1))
);
CREATE INDEX IF NOT EXISTS direcciones_cliente ON direcciones (cliente_id);

-- Códigos de 5 dígitos enviados por correo. Se guarda solo el hash del código.
CREATE TABLE IF NOT EXISTS codigos (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  correo      TEXT NOT NULL COLLATE NOCASE,
  motivo      TEXT NOT NULL CHECK (motivo IN ('registro', 'entrar', 'recuperar')),
  codigo_hash TEXT NOT NULL,
  intentos    INTEGER NOT NULL DEFAULT 5 CHECK (intentos >= 0),
  creado_en   TEXT NOT NULL DEFAULT (datetime('now')),
  expira_en   TEXT NOT NULL,
  usado_en    TEXT
);
CREATE INDEX IF NOT EXISTS codigos_correo ON codigos (correo, motivo, creado_en);

-- Sesiones abiertas. Se guarda solo el hash del token de la cookie.
CREATE TABLE IF NOT EXISTS sesiones (
  token_hash TEXT PRIMARY KEY,
  cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
  creado_en  TEXT NOT NULL DEFAULT (datetime('now')),
  expira_en  TEXT NOT NULL,
  ip         TEXT
);
CREATE INDEX IF NOT EXISTS sesiones_cliente ON sesiones (cliente_id);

-- ── Pedidos (la tabla ya existe): ahora pueden ligarse a una cuenta ──────
ALTER TABLE pedidos ADD COLUMN cliente_id INTEGER REFERENCES clientes(id);
CREATE INDEX IF NOT EXISTS pedidos_cliente ON pedidos (cliente_id);

-- ── Stock propio ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stock (
  perfume_id     TEXT NOT NULL,
  ml             INTEGER NOT NULL,
  piezas         INTEGER NOT NULL DEFAULT 0 CHECK (piezas >= 0),
  costo_unitario REAL,
  actualizado_en TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (perfume_id, ml)
);

CREATE TABLE IF NOT EXISTS movimientos_stock (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  perfume_id TEXT NOT NULL,
  ml         INTEGER NOT NULL,
  cantidad   INTEGER NOT NULL CHECK (cantidad <> 0),
  motivo     TEXT NOT NULL CHECK (motivo IN ('compra', 'venta', 'devolucion', 'ajuste')),
  folio      TEXT,
  nota       TEXT,
  creado_en  TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS movimientos_perfume ON movimientos_stock (perfume_id, ml);

-- ── Envíos ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS envios (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_folio   TEXT NOT NULL REFERENCES pedidos(folio),
  paqueteria     TEXT,
  servicio       TEXT,
  guia           TEXT,
  costo          REAL,
  estado         TEXT NOT NULL DEFAULT 'por_enviar'
                 CHECK (estado IN ('por_enviar', 'guia_creada', 'recolectado', 'en_camino', 'entregado', 'devuelto', 'incidencia')),
  skydropx_id    TEXT,
  creado_en      TEXT NOT NULL DEFAULT (datetime('now')),
  actualizado_en TEXT NOT NULL DEFAULT (datetime('now')),
  entregado_en   TEXT
);
CREATE INDEX IF NOT EXISTS envios_pedido ON envios (pedido_folio);
CREATE INDEX IF NOT EXISTS envios_estado ON envios (estado);

-- ── Reseñas ──────────────────────────────────────────────────────────────
-- Se publican solo cuando el equipo las aprueba (estado = 'publicada').
CREATE TABLE IF NOT EXISTS resenas (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  perfume_id   TEXT NOT NULL,
  cliente_id   INTEGER REFERENCES clientes(id) ON DELETE SET NULL,
  pedido_folio TEXT REFERENCES pedidos(folio),
  calificacion INTEGER NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
  titulo       TEXT,
  texto        TEXT,
  estado       TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'publicada', 'rechazada')),
  creado_en    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (cliente_id, perfume_id, pedido_folio)
);
CREATE INDEX IF NOT EXISTS resenas_perfume ON resenas (perfume_id, estado);

-- ── Quejas y aclaraciones ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS quejas (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id   INTEGER REFERENCES clientes(id) ON DELETE SET NULL,
  correo       TEXT NOT NULL,
  pedido_folio TEXT REFERENCES pedidos(folio),
  tipo         TEXT NOT NULL CHECK (tipo IN ('producto', 'envio', 'pago', 'devolucion', 'atencion', 'otro')),
  descripcion  TEXT NOT NULL,
  estado       TEXT NOT NULL DEFAULT 'abierta' CHECK (estado IN ('abierta', 'en_revision', 'resuelta', 'cerrada')),
  respuesta    TEXT,
  creado_en    TEXT NOT NULL DEFAULT (datetime('now')),
  resuelto_en  TEXT
);
CREATE INDEX IF NOT EXISTS quejas_estado ON quejas (estado);

-- ── Precios de la competencia (una foto por día, por perfume y tienda) ──
CREATE TABLE IF NOT EXISTS precios_competencia (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha        TEXT NOT NULL,              -- AAAA-MM-DD (hora de CDMX)
  perfume_id   TEXT NOT NULL,
  ml           INTEGER NOT NULL,
  tienda       TEXT NOT NULL,              -- liverpool, palacio, amazon, costco...
  precio       REAL NOT NULL CHECK (precio > 0),
  precio_antes REAL,
  disponible   INTEGER CHECK (disponible IN (0, 1)),
  url          TEXT,
  creado_en    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (fecha, perfume_id, ml, tienda)
);
CREATE INDEX IF NOT EXISTS precios_perfume ON precios_competencia (perfume_id, ml, fecha);
CREATE INDEX IF NOT EXISTS precios_fecha ON precios_competencia (fecha);
