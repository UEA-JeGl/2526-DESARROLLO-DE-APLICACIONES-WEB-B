// ==========================================
// DATOS DEL PROYECTO (ARREGLO DE OBJETOS)
// ==========================================

let servicios = [

{
    nombre:"Desarrollo Web",
    descripcion:"Diseño y desarrollo de sitios web modernos.",
    color:"primary"
},

{
    nombre:"Soporte Técnico",
    descripcion:"Mantenimiento preventivo y correctivo de equipos.",
    color:"success"
},

{
    nombre:"Capacitación",
    descripcion:"Cursos y asesorías en herramientas digitales.",
    color:"warning"
}

];

// Solicitudes registradas
let solicitudes=[];

// ==========================================
// ELEMENTOS DEL HTML
// ==========================================

const contenedorServicios=document.getElementById("contenedorServicios");

const listaServicios=document.getElementById("listaServicios");

const contador=document.getElementById("contador");

const formulario=document.getElementById("formServicio");

const mensaje=document.getElementById("mensaje");

// ==========================================
// MOSTRAR SERVICIOS DINÁMICAMENTE
// ==========================================

function mostrarServicios(){

contenedorServicios.innerHTML="";

// CONDICIÓN

if(servicios.length===0){

contenedorServicios.innerHTML=`

<div class="alert alert-danger">

No existen servicios registrados.

</div>

`;

return;

}

// REPETICIÓN

servicios.forEach(servicio=>{

contenedorServicios.innerHTML+=`

<div class="col-md-4 mb-4">

<div class="card h-100 shadow">

<div class="card-body text-center">

<h4>${servicio.nombre}</h4>

<p>${servicio.descripcion}</p>

<button class="btn btn-${servicio.color}">
Más información
</button>

</div>

</div>

</div>

`;

});

}

// ==========================================
// MOSTRAR SOLICITUDES
// ==========================================

function mostrarSolicitudes(){

listaServicios.innerHTML="";

contador.innerHTML=solicitudes.length;

// CONDICIÓN

if(solicitudes.length===0){

listaServicios.innerHTML=`

<div class="alert alert-warning">

Todavía no existen solicitudes registradas.

</div>

`;

return;

}

// REPETICIÓN

solicitudes.forEach((dato,index)=>{

listaServicios.innerHTML+=`

<div class="servicio">

<h5>${dato.nombre}</h5>

<p>

<strong>Servicio:</strong>

${dato.categoria}

</p>

<p>

${dato.descripcion}

</p>

<small>

Registro #${index+1}

</small>

</div>

`;

});

}

// ==========================================
// VALIDACIONES
// ==========================================

formulario.addEventListener("submit",function(e){

e.preventDefault();

const nombre=document.getElementById("nombre");

const descripcion=document.getElementById("descripcion");

const categoria=document.getElementById("categoria");

// limpiar errores

nombre.classList.remove("is-invalid");

descripcion.classList.remove("is-invalid");

categoria.classList.remove("is-invalid");

document.getElementById("errorNombre").innerHTML="";

document.getElementById("errorDescripcion").innerHTML="";

document.getElementById("errorCategoria").innerHTML="";

mensaje.innerHTML="";

// VALIDACIÓN NOMBRE

if(nombre.value.trim()==""){

nombre.classList.add("is-invalid");

document.getElementById("errorNombre").innerHTML="Ingrese su nombre.";

return;

}

// VALIDACIÓN DESCRIPCIÓN

if(descripcion.value.trim().length<10){

descripcion.classList.add("is-invalid");

document.getElementById("errorDescripcion").innerHTML="La descripción debe tener mínimo 10 caracteres.";

return;

}

// VALIDACIÓN CATEGORÍA

if(categoria.value==""){

categoria.classList.add("is-invalid");

document.getElementById("errorCategoria").innerHTML="Seleccione un servicio.";

return;

}

// CREAR OBJETO

const nuevaSolicitud={

nombre:nombre.value,

descripcion:descripcion.value,

categoria:categoria.value

};

// GUARDAR EN EL ARREGLO

solicitudes.push(nuevaSolicitud);

// ACTUALIZAR LISTA

mostrarSolicitudes();

// MENSAJE

mensaje.innerHTML=`

<div class="alert alert-success">

Solicitud registrada correctamente.

</div>

`;

// LIMPIAR FORMULARIO

formulario.reset();

});

// ==========================================
// INICIAR
// ==========================================

mostrarServicios();

mostrarSolicitudes();
