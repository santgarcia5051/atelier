/* ===== NOTAS CON FOTO =====
   Fotos en fotos/notas/<clave>.webp. En cada perfume, "destacadas" lista
   tres claves de aquí: una de salida, una de corazón y una de fondo. */
const NOTAS = {
  jazmin:    { nombre: "Jazmín",        desc: "Floral blanco" },
  caramelo:  { nombre: "Caramelo",      desc: "Gourmand" },
  vainilla:  { nombre: "Vainilla",      desc: "Cálida" },
  cardamomo: { nombre: "Cardamomo",     desc: "Especiado" },
  lavanda:   { nombre: "Lavanda",       desc: "Aromática" },
  oud:       { nombre: "Oud",           desc: "Amaderado intenso" },
  bergamota: { nombre: "Bergamota",     desc: "Cítrica" },
  neroli:    { nombre: "Neroli",        desc: "Floral luminoso" },
  ambar:     { nombre: "Ámbar",         desc: "Resinoso" },
  toronja:   { nombre: "Toronja rosada", desc: "Cítrica jugosa" },
  vetiver:   { nombre: "Vetiver",       desc: "Terroso" },
  maderas:   { nombre: "Maderas secas", desc: "Amaderado" },
  mar:       { nombre: "Notas marinas", desc: "Acuática" },
  mimosa:    { nombre: "Mimosa",        desc: "Floral atalcado" },
  pachuli:   { nombre: "Pachulí",       desc: "Terroso" },
  azahar:    { nombre: "Flor de azahar", desc: "Floral luminoso", foto: "neroli" },
  cedro:     { nombre: "Cedro",         desc: "Amaderado", foto: "maderas" },
  guayaco:   { nombre: "Guayaco",       desc: "Amaderado", foto: "maderas" },
  /* Para una nota sin foto use: foto: false, color: "#hex" */
  almendra:  { nombre: "Almendra",      desc: "Gourmand" },
  tuberosa:  { nombre: "Tuberosa",      desc: "Floral blanco" },
  cacao:     { nombre: "Cacao",         desc: "Gourmand" },
  grosella:  { nombre: "Grosella negra", desc: "Afrutada" },
  iris:      { nombre: "Iris",          desc: "Atalcado" },
  frambuesa: { nombre: "Frambuesa",     desc: "Afrutada" },
  miel:      { nombre: "Miel",          desc: "Melosa" },
  rosa:      { nombre: "Rosa",          desc: "Floral" },
  rangun:    { nombre: "Enredadera de Rangún", desc: "Floral atalcado" },
  mango:     { nombre: "Mango",         desc: "Afrutado" },
  sandalo:   { nombre: "Sándalo",       desc: "Cremoso", foto: "maderas" },
  limon:     { nombre: "Limón siciliano", desc: "Cítrico" },
  laurel:    { nombre: "Laurel",        desc: "Aromático" },
  mandarina: { nombre: "Mandarina sanguina", desc: "Cítrica" },
  canela:    { nombre: "Canela",        desc: "Especiada" },
  cuero:     { nombre: "Cuero",         desc: "Intenso" },
  menta:     { nombre: "Menta",         desc: "Fresca" },
  haba:      { nombre: "Haba tonka",    desc: "Cálida" },
  pimienta:  { nombre: "Pimienta negra", desc: "Especiada" },
  granada:   { nombre: "Granada",       desc: "Afrutada" },
  peonia:    { nombre: "Peonía",        desc: "Floral" },
  pera:      { nombre: "Pera",          desc: "Afrutada" },
  champana:  { nombre: "Champán rosado", desc: "Espumoso" },
  durazno:   { nombre: "Flor de durazno", desc: "Afrutada" },
  lichi:     { nombre: "Lichi",         desc: "Afrutado" },
  pina:      { nombre: "Piña",          desc: "Tropical" },
  coco:      { nombre: "Coco",          desc: "Cremoso" },
  tabaco:    { nombre: "Tabaco",        desc: "Cálido" },
  violeta:   { nombre: "Hoja de violeta", desc: "Verde" },
  salvia:    { nombre: "Salvia",        desc: "Aromática" },
  manzana:   { nombre: "Manzana",       desc: "Afrutada" },
  fresa:     { nombre: "Fresa",         desc: "Afrutada",         foto: false, color: "#C8344A" },
  avellana:  { nombre: "Avellana",      desc: "Gourmand",         foto: false, color: "#9A6A3E" },
  gardenia:  { nombre: "Gardenia",      desc: "Floral blanco",    foto: false, color: "#EFE6D2" },
  azucena:   { nombre: "Azucena",       desc: "Floral blanco",    foto: false, color: "#F1EADB" },
  merengue:  { nombre: "Merengue",      desc: "Gourmand",         foto: false, color: "#F3E7D6" },
  loto:      { nombre: "Flor de loto",  desc: "Acuático floral",  foto: false, color: "#7C93C9" },
  fresia:    { nombre: "Fresia",        desc: "Floral fresco",    foto: false, color: "#C7A3D6" },
  castana:   { nombre: "Castaña",       desc: "Gourmand" }
};

const SECCIONES = ["Mujer", "Hombre"];

/* ===== ENVÍOS =====
   Tarifas que paga el cliente según la zona de su código postal.
   gratisDesde: número de perfumes a partir del cual el envío es gratis. */
const ENVIO = {
  gratisDesde: 2,
  zonas: {
    local:     { nombre: "Local",     cubre: "Ciudad de México y Estado de México", precio: 169, dias: "1 a 3 días hábiles" },
    nacional:  { nombre: "Nacional",  cubre: "Resto de la República",               precio: 229, dias: "3 a 6 días hábiles" },
    extendida: { nombre: "Extendida", cubre: "Baja California, Baja California Sur, Chiapas, Quintana Roo y Yucatán", precio: 349, dias: "5 a 8 días hábiles" }
  }
};
