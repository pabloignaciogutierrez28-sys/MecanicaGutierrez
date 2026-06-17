import streamlit as st
from dataclasses import dataclass

# 1. Definición del Registro (Usamos dataclass que es más moderno)
@dataclass
class RegistroTurno:
    id_turno: int
    patente: str
    modelo_auto: str
    tipo_servicio: str
    costo: float
    estado: str

# 2. Datos de prueba
archivo_turnos = [
    RegistroTurno(5001, "AA890BB", "Volkswagen Amarok", "Cambio Filtros y Aceite", 45000.0, "En Taller"),
    RegistroTurno(5002, "AF543CC", "Ford Focus", "Cambio de Pastillas Freno", 32000.0, "Pendiente"),
    RegistroTurno(5003, "LOK789", "Renault Clio", "Revisión Eléctrica", 15000.0, "Terminado")
]

# 3. Interfaz Web con Streamlit
st.title("🔧 Mecánica Gutiérrez - Gestión de Turnos")

# Mostrar tabla en la web
st.subheader("Inventario de Turnos")
st.table([t.__dict__ for t in archivo_turnos])

# Búsqueda interactiva
st.subheader("Buscar Turno por ID")
id_input = st.number_input("Ingrese el ID del turno:", value=5001, step=1)

if st.button("Buscar"):
    encontrado = False
    for turno in archivo_turnos:
        if turno.id_turno == id_input:
            st.success(f"¡Registro encontrado!")
            st.write(f"**Vehículo:** {turno.modelo_auto}")
            st.write(f"**Servicio:** {turno.tipo_servicio}")
            st.write(f"**Estado:** {turno.estado}")
            encontrado = True
            break
    
    if not encontrado:
        st.error(f"No se encontró ningún registro con ID {id_input}")
