(function () {
  var guardado = localStorage.getItem("rh_theme");
  document.documentElement.setAttribute("data-theme", guardado === "dark" ? "dark" : "light");
})();

function alternarTema() {
  var actual = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", actual);
  localStorage.setItem("rh_theme", actual);
}

function tokenDeLaUrl() {
  return new URLSearchParams(window.location.search).get("token") || "";
}

function escapar(valor) {
  return String(valor ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function api(ruta, opciones) {
  var respuesta = await fetch(ruta, opciones || {});
  var texto = await respuesta.text();
  var datos = null;
  if (texto) {
    try {
      datos = JSON.parse(texto);
    } catch (error) {
      datos = { detail: texto };
    }
  }
  if (!respuesta.ok) {
    var detalle = datos && datos.detail ? datos.detail : respuesta.statusText;
    throw new Error(typeof detalle === "string" ? detalle : JSON.stringify(detalle));
  }
  return datos;
}

function mostrarError(id, error) {
  var caja = document.getElementById(id);
  caja.hidden = false;
  caja.textContent = error.message || String(error);
}
