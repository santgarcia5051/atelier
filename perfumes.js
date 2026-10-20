/* =========================================================
   CATÁLOGO Y ENVÍOS DE LA TIENDA
   Este es el único archivo que necesita tocar para:
   - cambiar precios, textos o notas de un perfume
   - agregar o quitar perfumes
   - cambiar tarifas de envío o el envío gratis
   Consejos: conserve las comillas "" y las comas al final de
   cada línea. Los precios van sin signo $ ni comas (2999, no $2,999).
   ========================================================= */

/* ===== CATÁLOGO =====
   Para cambiar o añadir perfumes, edite esta lista.
   seccion: "Mujer" o "Hombre".
   pres: presentaciones disponibles, cada una con sus mililitros y precio en pesos mexicanos.
   img: deje null para usar la ilustración, o ponga el nombre del archivo de la foto. */
const PERFUMES = [
  { id: "scandal-le-parfum", marca: "Jean Paul Gaultier", nombre: "Scandal Le Parfum", conc: "EDP Intense",
    seccion: "Mujer", familia: "Oriental floral",
    lema: "Audaz, dulce y magnética.",
    venta: "Scandal Le Parfum es la versión más intensa y seductora de la línea Scandal. El jazmín abre con elegancia y da paso a un caramelo salado irresistible que se funde en un fondo cálido de vainilla. Es una fragancia que se nota al llegar y se recuerda al salir: ideal para la noche, las citas y los eventos donde usted quiere dejar huella.",
    salida: ["Jazmín"], corazon: ["Caramelo", "Sal"], fondo: ["Vainilla"],
    acordes: [["Caramelo", 92], ["Avainillado", 80], ["Floral blanco", 60], ["Salado", 45]],
    duracion: "8–10 h", proyeccion: 4, temporada: "Otoño · Invierno", ocasion: "Noche · Citas",
    pres: [{ ml: 80, precio: 2999 }], forma: "alto", liquido: "#8E1F2F", img: "fotos/scandal-le-parfum.webp" },
  { id: "le-male-le-parfum", marca: "Jean Paul Gaultier", nombre: "Le Male Le Parfum", conc: "EDP Intense",
    seccion: "Hombre", familia: "Aromático ambarado",
    lema: "Elegancia intensa con carácter.",
    venta: "Le Male Le Parfum lleva el clásico de Jean Paul Gaultier a su expresión más elegante. El cardamomo abre con un toque especiado y fresco; la lavanda y el iris forman un corazón refinado, y una estela ambarada y amaderada con vainilla lo vuelve cálido y envolvente. Una fragancia de gran presencia para proyectar seguridad en la oficina, en una cena o en una noche especial.",
    salida: ["Cardamomo"], corazon: ["Lavanda", "Iris"], fondo: ["Vainilla", "Notas amaderadas"],
    acordes: [["Aromático", 85], ["Avainillado", 78], ["Atalcado", 60], ["Amaderado", 55]],
    duracion: "10–12 h", proyeccion: 4, temporada: "Otoño · Invierno", ocasion: "Noche · Eventos formales",
    pres: [{ ml: 125, precio: 2999 }], forma: "cuadrado", liquido: "#22324F", img: "fotos/le-male-le-parfum.webp" },
  { id: "bad-boy-cobalt-absolute", marca: "Carolina Herrera", nombre: "Bad Boy Cobalt Absolute", conc: "EDP",
    seccion: "Hombre", familia: "Amaderado ambarado",
    lema: "Oscuro, intenso y magnético.",
    venta: "Bad Boy Cobalt Absolute es la interpretación más profunda y sensual de la línea Bad Boy de Carolina Herrera. Abre fresca y herbal con lavanda, salvia y elemí; en el corazón, el oud y la trufa aportan un carácter terroso y opulento, y un fondo de roble, vainilla y vetiver deja una estela cálida que acompaña toda la noche. Una fragancia para quien no pasa desapercibido.",
    salida: ["Lavanda", "Salvia", "Elemí"], corazon: ["Oud", "Trufa", "Geranio"], fondo: ["Roble", "Vainilla", "Vetiver"],
    acordes: [["Amaderado", 88], ["Aromático", 72], ["Avainillado", 62], ["Terroso", 55]],
    duracion: "10–12 h", proyeccion: 4, temporada: "Otoño · Invierno", ocasion: "Noche · Citas",
    pres: [{ ml: 100, precio: 3099 }], forma: "facetado", liquido: "#1D3A8A", img: "fotos/bad-boy-cobalt-absolute.webp" },
  { id: "neroli-portofino", marca: "Tom Ford", nombre: "Neroli Portofino", conc: "EDP",
    seccion: "Hombre", familia: "Cítrico aromático",
    lema: "La Riviera italiana en un frasco.",
    venta: "Neroli Portofino captura la luz del verano en la costa italiana. Bergamota, mandarina y limón de Amalfi abren con una frescura chispeante, matizada por lavanda, romero y mirto; el corazón de flor de naranjo y neroli aporta una elegancia luminosa, y un fondo suave de ámbar y angélica lo mantiene limpio y sofisticado. La fragancia de lujo ideal para el día, el calor y para quien busca distinguirse con discreción.",
    salida: ["Bergamota", "Mandarina", "Limón de Amalfi", "Lavanda", "Romero"], corazon: ["Neroli", "Flor de naranjo", "Jazmín"], fondo: ["Ámbar", "Ambreta", "Angélica"],
    acordes: [["Cítrico", 95], ["Floral blanco", 70], ["Aromático", 60], ["Fresco", 55]],
    duracion: "5–7 h", proyeccion: 3, temporada: "Primavera · Verano", ocasion: "Día · Vacaciones",
    pres: [{ ml: 100, precio: 7899 }], forma: "cuadrado", liquido: "#1AA3A3", img: "fotos/neroli-portofino.webp" },
  { id: "perseus", marca: "Parfums de Marly", nombre: "Perseus", conc: "EDP",
    seccion: "Hombre", familia: "Cítrico aromático",
    lema: "Frescura luminosa con carácter.",
    venta: "Perseus es la propuesta más vibrante de Parfums de Marly. Toronja rosada, bergamota y grosella negra abren con una energía fresca y jugosa; el vetiver, la mandarina verde y el geranio le dan un corazón verde y elegante, y un fondo de maderas secas, madera de cachemira y ámbar gris lo vuelve sofisticado y duradero. Una fragancia de nicho que transmite seguridad y buen gusto desde la primera aplicación.",
    salida: ["Toronja rosada", "Bergamota", "Grosella negra"], corazon: ["Vetiver", "Mandarina verde", "Geranio"], fondo: ["Maderas secas", "Madera de cachemira", "Ámbar gris"],
    acordes: [["Cítrico", 90], ["Afrutado", 62], ["Amaderado", 60], ["Aromático", 55]],
    duracion: "7–9 h", proyeccion: 4, temporada: "Primavera · Verano", ocasion: "Día · Oficina",
    pres: [{ ml: 125, precio: 6699 }], forma: "cuadrado", liquido: "#F39A1E", img: "fotos/perseus.webp" },
  { id: "acqua-di-gio-profondo-parfum", marca: "Giorgio Armani", nombre: "Acqua di Giò Profondo", conc: "Parfum",
    seccion: "Hombre", familia: "Acuático aromático",
    lema: "La profundidad del mar en su versión más intensa.",
    venta: "Acqua di Giò Profondo Parfum lleva el clásico marino de Giorgio Armani a su concentración más rica. Notas marinas y mandarina verde abren con una frescura oceánica; un corazón de mimosa aporta una calidez suave y ligeramente atalcada, y un fondo de pachulí y ládano le da profundidad ambarada y gran duración. Fresco para el día y elegante para la noche: un perfume que funciona en cualquier ocasión.",
    salida: ["Notas marinas", "Mandarina verde"], corazon: ["Mimosa"], fondo: ["Pachulí", "Ládano"],
    acordes: [["Acuático", 90], ["Ambarado", 62], ["Aromático", 58], ["Terroso", 45]],
    duracion: "8–10 h", proyeccion: 4, temporada: "Todo el año", ocasion: "Día · Noche",
    pres: [{ ml: 100, precio: 3299 }], forma: "alto", liquido: "#1E3A6B", img: "fotos/acqua-di-gio-profondo-parfum.webp" }
];
const SECCIONES = ["Mujer", "Hombre"];

/* ===== ENVÍOS =====
   Tarifas que paga el cliente según la zona de su código postal.
   gratisDesde: número de perfumes a partir del cual el envío es gratis. */
const ENVIO = {
  gratisDesde: 2,
  zonas: {
    local:     { nombre: "Local",     cubre: "Ciudad de México y Estado de México", precio: 129, dias: "1 a 3 días hábiles" },
    nacional:  { nombre: "Nacional",  cubre: "Resto de la República",               precio: 179, dias: "3 a 6 días hábiles" },
    extendida: { nombre: "Extendida", cubre: "Baja California, Baja California Sur, Chiapas, Quintana Roo y Yucatán", precio: 299, dias: "5 a 8 días hábiles" }
  }
};
