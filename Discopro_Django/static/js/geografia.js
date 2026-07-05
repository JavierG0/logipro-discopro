/**
 * Selects en cascada Región → Provincia → Comuna
 */
document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('id_region');
    const provinciaSelect = document.getElementById('id_provincia');
    const comunaSelect = document.getElementById('id_comuna');

    if (!regionSelect || !provinciaSelect || !comunaSelect) return;

    const apiProvincias = regionSelect.dataset.apiProvincias || '/farmacia/api/provincias/';
    const apiComunas = regionSelect.dataset.apiComunas || '/farmacia/api/comunas/';

    function resetSelect(select, placeholder) {
        select.innerHTML = '';
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = placeholder;
        select.appendChild(opt);
    }

    async function cargarProvincias(region, selected) {
        resetSelect(provinciaSelect, 'Seleccione provincia...');
        resetSelect(comunaSelect, 'Seleccione comuna...');
        if (!region) return;
        const res = await fetch(`${apiProvincias}?region=${encodeURIComponent(region)}`);
        const data = await res.json();
        data.provincias.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p;
            opt.textContent = p;
            if (p === selected) opt.selected = true;
            provinciaSelect.appendChild(opt);
        });
    }

    async function cargarComunas(region, provincia, selected) {
        resetSelect(comunaSelect, 'Seleccione comuna...');
        if (!region || !provincia) return;
        const res = await fetch(`${apiComunas}?region=${encodeURIComponent(region)}&provincia=${encodeURIComponent(provincia)}`);
        const data = await res.json();
        data.comunas.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            if (c === selected) opt.selected = true;
            comunaSelect.appendChild(opt);
        });
    }

    regionSelect.addEventListener('change', () => {
        cargarProvincias(regionSelect.value);
    });

    provinciaSelect.addEventListener('change', () => {
        cargarComunas(regionSelect.value, provinciaSelect.value);
    });

    if (regionSelect.value) {
        cargarProvincias(regionSelect.value, provinciaSelect.value).then(() => {
            if (provinciaSelect.value) {
                cargarComunas(regionSelect.value, provinciaSelect.value, comunaSelect.value);
            }
        });
    }
});
