document.addEventListener('DOMContentLoaded', function () {
    const farmaciaSelect = document.getElementById('sucursal_origen');
    const direccionOrigen = document.getElementById('direccion_origen');
    const motoristaSelect = document.getElementById('motorista');
    if (!farmaciaSelect) return;

    const motoristaInicial = motoristaSelect?.dataset.selected || '';

    async function cargarDireccion(id) {
        if (!direccionOrigen) return;
        if (!id) {
            direccionOrigen.value = '';
            return;
        }
        const res = await fetch(`/farmacia/api/${id}/direccion/`);
        if (!res.ok) return;
        const data = await res.json();
        direccionOrigen.value = data.direccion || data.direccion_calle || '';
    }

    async function cargarMotoristas(id, seleccionado) {
        if (!motoristaSelect) return;
        motoristaSelect.innerHTML = '<option value="">Seleccione motorista...</option>';
        if (!id) {
            motoristaSelect.disabled = true;
            return;
        }
        motoristaSelect.disabled = false;
        const res = await fetch(`/farmacia/api/${id}/motoristas/`);
        if (!res.ok) return;
        const data = await res.json();
        const lista = data.motoristas || [];
        if (lista.length === 0) {
            motoristaSelect.innerHTML = '<option value="">Sin motoristas en esta farmacia</option>';
            motoristaSelect.disabled = true;
            return;
        }
        lista.forEach(function (m) {
            const opt = document.createElement('option');
            opt.value = m.id;
            opt.textContent = m.nombre + (m.moto ? ' · Moto ' + m.moto : '');
            if (String(seleccionado) === String(m.id)) {
                opt.selected = true;
            }
            motoristaSelect.appendChild(opt);
        });
    }

    async function onFarmaciaChange() {
        const id = farmaciaSelect.value;
        await cargarDireccion(id);
        await cargarMotoristas(id, '');
    }

    farmaciaSelect.addEventListener('change', onFarmaciaChange);

    if (farmaciaSelect.value) {
        cargarDireccion(farmaciaSelect.value);
        cargarMotoristas(farmaciaSelect.value, motoristaInicial);
    } else if (motoristaSelect) {
        motoristaSelect.disabled = true;
    }
});
