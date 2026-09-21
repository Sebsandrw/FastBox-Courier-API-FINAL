const API_BASE = "https://sebaesco.alwaysdata.net/api/v1";

const listaPaquetes = document.getElementById("listaPaquetes");
const estadoCarga = document.getElementById("estadoCarga");
const buscador = document.getElementById("buscador");
const filtroEstado = document.getElementById("filtroEstado");
const btnRecargar = document.getElementById("btnRecargar");

const detallePaquete = document.getElementById("detallePaquete");
const contenidoDetalle = document.getElementById("contenidoDetalle");
const btnCerrarDetalle = document.getElementById("btnCerrarDetalle");

let paquetes = [];

async function cargarPaquetes() {
  mostrarMensaje("Cargando información...");
  listaPaquetes.innerHTML = "";
  detallePaquete.classList.add("oculto");

  try {
    const respuesta = await fetch(`${API_BASE}/paquetes/?format=json`);

    if (!respuesta.ok) {
      throw new Error("No se pudo consultar el servidor.");
    }

    paquetes = await respuesta.json();

    aplicarFiltros();

  } catch (error) {
    mostrarMensaje(
      "Error al consultar el servidor. Revise si la API está disponible."
    );
  }
}

function aplicarFiltros() {
  const texto = buscador.value.toLowerCase().trim();
  const estado = filtroEstado.value;

  let resultado = paquetes.filter((paquete) => {
    const datos = `
      ${paquete.guia_fastbox}
      ${paquete.tracking_original || ""}
      ${paquete.tienda_origen}
      ${paquete.descripcion}
      ${paquete.cliente_nombre}
    `.toLowerCase();

    const coincideTexto = datos.includes(texto);
    const coincideEstado = estado === "" || paquete.estado === estado;

    return coincideTexto && coincideEstado;
  });

  mostrarPaquetes(resultado);
}

function mostrarPaquetes(lista) {
  listaPaquetes.innerHTML = "";

  if (lista.length === 0) {
    mostrarMensaje("No existen registros con los criterios seleccionados.");
    return;
  }

  estadoCarga.classList.add("oculto");

  lista.forEach((paquete) => {
    const tarjeta = document.createElement("article");
    tarjeta.className = "tarjeta";

    tarjeta.innerHTML = `
      <h3>${paquete.guia_fastbox}</h3>

      <p><strong>Cliente:</strong> ${paquete.cliente_nombre}</p>
      <p><strong>Casillero:</strong> ${paquete.cliente_casillero}</p>
      <p><strong>Tienda:</strong> ${paquete.tienda_origen}</p>
      <p><strong>Descripción:</strong> ${paquete.descripcion}</p>
      <p><strong>Peso:</strong> ${paquete.peso_libras} lb</p>
      <p><strong>Costo:</strong> $${Number(paquete.costo_estimado).toFixed(2)}</p>

      <span class="estado">
        ${paquete.estado_texto}
      </span>

      <button
        class="btn-detalle"
        onclick="cargarDetalle(${paquete.id_paquete})"
      >
        Ver detalle
      </button>
    `;

    listaPaquetes.appendChild(tarjeta);
  });
}

async function cargarDetalle(idPaquete) {
  detallePaquete.classList.remove("oculto");
  contenidoDetalle.innerHTML = "<p>Cargando detalle...</p>";

  try {
    const respuesta = await fetch(
      `${API_BASE}/paquetes/${idPaquete}/?format=json`
    );

    if (!respuesta.ok) {
      throw new Error("No se pudo consultar el detalle.");
    }

    const paquete = await respuesta.json();

    contenidoDetalle.innerHTML = `
      <dl>
        <dt>ID</dt>
        <dd>${paquete.id_paquete}</dd>

        <dt>Guía FastBox</dt>
        <dd>${paquete.guia_fastbox}</dd>

        <dt>Tracking original</dt>
        <dd>${paquete.tracking_original || "No registrado"}</dd>

        <dt>Cliente</dt>
        <dd>${paquete.cliente_nombre}</dd>

        <dt>Casillero</dt>
        <dd>${paquete.cliente_casillero}</dd>

        <dt>Tienda</dt>
        <dd>${paquete.tienda_origen}</dd>

        <dt>Descripción</dt>
        <dd>${paquete.descripcion}</dd>

        <dt>Categoría</dt>
        <dd>${paquete.tarifa_categoria}</dd>

        <dt>Peso</dt>
        <dd>${paquete.peso_libras} lb</dd>

        <dt>Costo estimado</dt>
        <dd>$${Number(paquete.costo_estimado).toFixed(2)}</dd>

        <dt>Estado</dt>
        <dd>${paquete.estado_texto}</dd>

        <dt>Fecha de registro</dt>
        <dd>${formatearFecha(paquete.fecha_registro)}</dd>
      </dl>
    `;

    detallePaquete.scrollIntoView({
      behavior: "smooth",
    });

  } catch (error) {
    contenidoDetalle.innerHTML = `
      <p>
        Error al consultar el detalle del paquete.
      </p>
    `;
  }
}

function mostrarMensaje(texto) {
  estadoCarga.textContent = texto;
  estadoCarga.classList.remove("oculto");
}

function formatearFecha(fecha) {
  if (!fecha) {
    return "No registrada";
  }

  return new Date(fecha).toLocaleString("es-EC");
}

buscador.addEventListener("input", aplicarFiltros);
filtroEstado.addEventListener("change", aplicarFiltros);
btnRecargar.addEventListener("click", cargarPaquetes);

btnCerrarDetalle.addEventListener("click", () => {
  detallePaquete.classList.add("oculto");
});

cargarPaquetes();