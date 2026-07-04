// ===============================
// PROYECTO INTEGRADOR - SEMANA 6
// VALIDACIONES DINÁMICAS
// ===============================

const formulario = document.getElementById("formServicio");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const listaServicios = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

let totalRegistros = 0;

// ===============================
// VALIDAR NOMBRE
// ===============================

function validarNombre() {

    const valor = nombre.value.trim();

    if (valor === "") {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        document.getElementById("errorNombre").textContent =
            "El nombre es obligatorio.";

        return false;
    }

    if (valor.length < 3) {

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        document.getElementById("errorNombre").textContent =
            "Debe ingresar mínimo 3 caracteres.";

        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    document.getElementById("errorNombre").textContent = "";

    return true;
}

// ===============================
// VALIDAR DESCRIPCIÓN
// ===============================

function validarDescripcion() {

    const valor = descripcion.value.trim();

    if (valor === "") {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        document.getElementById("errorDescripcion").textContent =
            "La descripción es obligatoria.";

        return false;
    }

    if (valor.length < 10) {

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        document.getElementById("errorDescripcion").textContent =
            "Debe contener mínimo 10 caracteres.";

        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    document.getElementById("errorDescripcion").textContent = "";

    return true;
}

// ===============================
// VALIDAR CATEGORÍA
// ===============================

function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        document.getElementById("errorCategoria").textContent =
            "Seleccione un tipo de servicio.";

        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    document.getElementById("errorCategoria").textContent = "";

    return true;
}

// ===============================
// EVENTOS
// ===============================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);

// ===============================
// ENVIAR FORMULARIO
// ===============================

formulario.addEventListener("submit", function (evento) {

    evento.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los errores antes de registrar la solicitud.
            </div>
        `;

        return;
    }

    mensaje.innerHTML = `
        <div class="alert alert-success">
            La solicitud fue registrada correctamente.
        </div>
    `;
        // ===============================
    // CREAR TARJETA DEL SERVICIO
    // ===============================

    const tarjeta = document.createElement("div");
    tarjeta.classList.add("card", "shadow-sm", "mb-3");

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body");

    const titulo = document.createElement("h5");
    titulo.classList.add("card-title");
    titulo.textContent = nombre.value;

    const texto = document.createElement("p");
    texto.classList.add("card-text");
    texto.textContent = descripcion.value;

    const etiqueta = document.createElement("span");
    etiqueta.classList.add("badge", "bg-primary");
    etiqueta.textContent = categoria.value;

    const salto1 = document.createElement("br");
    const salto2 = document.createElement("br");

    const botonEliminar = document.createElement("button");

    botonEliminar.textContent = "Eliminar";

    botonEliminar.classList.add(
        "btn",
        "btn-outline-danger",
        "btn-sm",
        "float-end"
    );

    // ===============================
    // ELIMINAR REGISTRO
    // ===============================

    botonEliminar.addEventListener("click", function () {

        tarjeta.remove();

        totalRegistros--;

        contador.textContent = totalRegistros;

        mensaje.innerHTML = `
            <div class="alert alert-warning">
                El registro fue eliminado correctamente.
            </div>
        `;

    });

    cuerpo.appendChild(titulo);
    cuerpo.appendChild(texto);
    cuerpo.appendChild(etiqueta);
    cuerpo.appendChild(salto1);
    cuerpo.appendChild(salto2);
    cuerpo.appendChild(botonEliminar);

    tarjeta.appendChild(cuerpo);

    listaServicios.appendChild(tarjeta);

    // ===============================
    // ACTUALIZAR CONTADOR
    // ===============================

    totalRegistros++;

    contador.textContent = totalRegistros;

    // ===============================
    // LIMPIAR FORMULARIO
    // ===============================

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    document.getElementById("errorNombre").textContent = "";
    document.getElementById("errorDescripcion").textContent = "";
    document.getElementById("errorCategoria").textContent = "";

});