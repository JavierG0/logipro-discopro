"""Datos geográficos de Chile para selects en cascada (Región → Provincia → Comuna)."""

GEOGRAFIA_CHILE = {
    'Arica': {
        'Arica': ['Arica'],
    },
    'Parinacota': {
        'Parinacota': ['Putre', 'General Lagos'],
    },
    'Tarapacá': {
        'Iquique': ['Iquique', 'Alto Hospicio'],
        'Tamarugal': ['Pozo Almonte', 'Pica', 'Huara', 'Camiña', 'Colchane'],
    },
    'Antofagasta': {
        'Antofagasta': ['Antofagasta', 'Mejillones', 'Sierra Gorda', 'Taltal'],
        'El Loa': ['Calama', 'Ollagüe', 'San Pedro de Atacama'],
        'Tocopilla': ['Tocopilla', 'María Elena'],
    },
    'Atacama': {
        'Copiapó': ['Copiapó', 'Caldera', 'Tierra Amarilla'],
        'Huasco': ['Vallenar', 'Alto del Carmen', 'Freirina', 'Huasco'],
        'Chañaral': ['Chañaral', 'Diego de Almagro'],
    },
    'Coquimbo': {
        'Elqui': ['La Serena', 'Coquimbo', 'Andacollo', 'La Higuera', 'Paiguano', 'Vicuña'],
        'Choapa': ['Illapel', 'Canela', 'Los Vilos', 'Salamanca'],
        'Limarí': ['Ovalle', 'Combarbalá', 'Monte Patria', 'Punitaqui', 'Río Hurtado'],
    },
    'Valparaíso': {
        'Valparaíso': ['Valparaíso', 'Viña del Mar', 'Quilpué', 'Villa Alemana', 'Concón', 'Quintero', 'Puchuncaví', 'Casablanca', 'Cartagena', 'San Antonio', 'Santo Domingo'],
        'San Felipe de Aconcagua': ['San Felipe', 'Catemu', 'Panquehue', 'Llaillay', 'Putaendo', 'Santa María'],
        'Quillota': ['Quillota', 'La Calera', 'Hijuelas', 'La Cruz', 'Nogales', 'Limache', 'Olmué'],
        'Petorca': ['La Ligua', 'Cabildo', 'Papudo', 'Zapallar', 'Petorca'],
        'Los Andes': ['Los Andes', 'San Esteban', 'Calle Larga', 'Rinconada'],
        'Isla de Pascua': ['Isla de Pascua'],
        'Marga Marga': ['Quilpué', 'Villa Alemana', 'Limache', 'Olmué'],
    },
    'Metropolitana de Santiago': {
        'Santiago': ['Santiago', 'Cerrillos', 'Cerro Navia', 'Conchalí', 'El Bosque', 'Estación Central', 'Huechuraba', 'Independencia', 'La Cisterna', 'La Florida', 'La Granja', 'La Pintana', 'La Reina', 'Las Condes', 'Lo Barnechea', 'Lo Espejo', 'Lo Prado', 'Macul', 'Maipú', 'Ñuñoa', 'Pedro Aguirre Cerda', 'Peñalolén', 'Providencia', 'Pudahuel', 'Quilicura', 'Quinta Normal', 'Recoleta', 'Renca', 'San Joaquín', 'San Miguel', 'San Ramón', 'Vitacura', 'Puente Alto', 'Pirque', 'San José de Maipo'],
        'Cordillera': ['Puente Alto', 'Pirque', 'San José de Maipo'],
        'Chacabuco': ['Colina', 'Lampa', 'Tiltil'],
        'Maipo': ['San Bernardo', 'Buin', 'Calera de Tango', 'Paine'],
        'Melipilla': ['Melipilla', 'Alhué', 'Curacaví', 'María Pinto', 'San Pedro'],
        'Talagante': ['Talagante', 'El Monte', 'Isla de Maipo', 'Padre Hurtado', 'Peñaflor'],
    },
    "O'Higgins": {
        'Cachapoal': ['Rancagua', 'Codegua', 'Coinco', 'Coltauco', 'Doñihue', 'Graneros', 'Las Cabras', 'Machalí', 'Malloa', 'Mostazal', 'Olivar', 'Peumo', 'Pichidegua', 'Quinta de Tilcoco', 'Rengo', 'Requínoa', 'San Vicente'],
        'Colchagua': ['San Fernando', 'Chimbarongo', 'Lolol', 'Nancagua', 'Palmilla', 'Peralillo', 'Placilla', 'Pumanque', 'Santa Cruz'],
        'Cardenal Caro': ['Pichilemu', 'La Estrella', 'Litueche', 'Marchihue', 'Navidad', 'Paredones'],
    },
}


def regiones():
    return sorted(GEOGRAFIA_CHILE.keys())


def provincias(region):
    if not region or region not in GEOGRAFIA_CHILE:
        return []
    return sorted(GEOGRAFIA_CHILE[region].keys())


def comunas(region, provincia):
    if not region or not provincia:
        return []
    return GEOGRAFIA_CHILE.get(region, {}).get(provincia, [])
