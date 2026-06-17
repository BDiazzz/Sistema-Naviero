function mostrarContenido(seleccionado, event) {
  const puertoContainer = event.target.closest('.puerto');
  puertoContainer.querySelectorAll('.opcion').forEach(btn => btn.classList.remove('activa'));
  event.target.classList.add('activa');
  puertoContainer.querySelectorAll('.contenido').forEach(contenido => {
    contenido.style.display = 'none';
  });
  document.getElementById(seleccionado).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function () {
  function calcularSubtotalYTotal() {
    let totalGeneral = 0;

    // Para cada puerto
    document.querySelectorAll('.puerto').forEach(puerto => {
      let subtotalProductos = 0;
      let subtotalServicios = 0;

      // Productos - CAMBIO IMPORTANTE AQUÍ
      const productosContainer = puerto.querySelector('[id^="productos-"]');
      if (productosContainer) {
        productosContainer.querySelectorAll('input[name^="productos["]').forEach(input => {
          const precio = parseFloat(input.dataset.precio) || 0;
          const cantidad = parseInt(input.value) || 0;
          if (cantidad > 0) {
            subtotalProductos += precio * cantidad;
  }
        });
      }

      // Servicios - CAMBIO IMPORTANTE AQUÍ
      const serviciosContainer = puerto.querySelector('[id^="servicios-"]');
      if (serviciosContainer) {
        serviciosContainer.querySelectorAll('select[name^="servicios["]').forEach(select => {
          if (select.value !== "0") {
            const precio = parseFloat(select.options[select.selectedIndex].dataset.precio) || 0;
            subtotalServicios += precio;
          }
        });
      }

      // Actualiza subtotales
      const epId = puerto.querySelector('[id^="productos-"]')?.id.split('-')[1] || 
                  puerto.querySelector('[id^="servicios-"]')?.id.split('-')[1];
      
      const subtotalProdElem = document.getElementById(`subtotal-productos-${epId}`);
      if (subtotalProdElem) {
        subtotalProdElem.textContent = subtotalProductos.toFixed(2);
      }

      const subtotalServElem = document.getElementById(`subtotal-servicios-${epId}`);
      if (subtotalServElem) {
        subtotalServElem.textContent = subtotalServicios.toFixed(2);
      }

      totalGeneral += subtotalProductos + subtotalServicios;
    });

    // Total general
    document.getElementById('total-general').textContent = totalGeneral.toFixed(2);
  }

  // Escuchar cambios en inputs de cantidad - CAMBIO IMPORTANTE AQUÍ
  document.querySelectorAll('input[name^="productos["]').forEach(input => {
    input.addEventListener('input', calcularSubtotalYTotal);
  });

  // Escuchar cambios en selects de servicios - CAMBIO IMPORTANTE AQUÍ
  document.querySelectorAll('select[name^="servicios["]').forEach(select => {
    select.addEventListener('change', calcularSubtotalYTotal);
  });

  // Inicializa cálculo al cargar
  calcularSubtotalYTotal();
});