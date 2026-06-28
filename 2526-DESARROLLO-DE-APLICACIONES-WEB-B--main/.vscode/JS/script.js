// ===============================
// PROYECTO SEMANA 5
// REGISTRO DINÁMICO DE SERVICIOS
// ===============================

const formulario = document.getElementById("formServicio");
const listaServicios = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

let totalRegistros = 0;

formulario.addEventListener("submit", function (evento) {

    evento.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;

    // Validación
    if (nombre === "" || descripcion === "" || categoria === "") {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Todos los campos son obligatorios.
            </div>
        `;

        return;
    }

    mensaje.innerHTML = `
        <div class="alert alert-success">
            La solicitud fue registrada correctamente.
        </div>
    `;

    // Crear tarjeta
    const tarjeta = document.createElement("div");
    tarjeta.classList.add("card", "shadow-sm", "mb-3");

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body");

    const titulo = document.createElement("h5");
    titulo.classList.add("card-title");
    titulo.textContent = nombre;

    const texto = document.createElement("p");
    texto.classList.add("card-text");
    texto.textContent = descripcion;

    const etiqueta = document.createElement("span");
    etiqueta.classList.add("badge", "bg-primary");
    etiqueta.textContent = categoria;

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

    botonEliminar.addEventListener("click", function () {

        tarjeta.remove();

        totalRegistros--;

        contador.textContent = totalRegistros;

        mensaje.innerHTML = `
            <div class="alert alert-warning">
                El registro fue eliminado.
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

    totalRegistros++;

    contador.textContent = totalRegistros;

    formulario.reset();

});