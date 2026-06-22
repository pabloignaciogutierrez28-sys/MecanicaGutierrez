import streamlit as st
from dataclasses import dataclass
import pandas as pd

# ==========================================================
# DEFINICIÓN DEL REGISTRO
# ==========================================================
# id_turno es la CLAVE PRINCIPAL del registro.
# Cada turno posee un identificador único que permite
# localizarlo mediante búsqueda secuencial.

@dataclass
class RegistroTurno:
    id_turno: int
    patente: str
    modelo_auto: str
    tipo_servicio: str
    costo: float
    estado: str


# ==========================================================
# FUNCIONES
# ==========================================================

def buscar_por_id(id_buscado):
    for turno in archivo_turnos:
        if turno.id_turno == id_buscado:
            return turno
    return None


def buscar_por_patente(patente_buscada):
    for turno in archivo_turnos:
        if turno.patente.upper() == patente_buscada.upper():
            return turno
    return None


# ==========================================================
# ARCHIVO DE REGISTROS
# ==========================================================

if "archivo_turnos" not in st.session_state:
    st.session_state.archivo_turnos = [
        RegistroTurno(5001, "AA890BB", "Volkswagen Amarok", "Cambio Filtros y Aceite", 45000.0, "En Taller"),
        RegistroTurno(5002, "AF543CC", "Ford Focus", "Cambio de Pastillas Freno", 32000.0, "Pendiente"),
        RegistroTurno(5003, "LOK789", "Renault Clio", "Revisión Eléctrica", 15000.0, "Terminado")
    ]

archivo_turnos = st.session_state.archivo_turnos

# ==========================================================
# INTERFAZ WEB
# ==========================================================

st.title("🔧 Mecánica Gutiérrez - Gestión de Turnos")

st.info(
    "Clave principal del registro: ID de Turno. "
    "Cada turno posee un identificador único."
)

# ==========================================================
# MÉTRICAS
# ==========================================================

total = len(archivo_turnos)
en_taller = sum(1 for t in archivo_turnos if t.estado == "En Taller")
pendientes = sum(1 for t in archivo_turnos if t.estado == "Pendiente")
terminados = sum(1 for t in archivo_turnos if t.estado == "Terminado")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total", total)
col2.metric("En Taller", en_taller)
col3.metric("Pendientes", pendientes)
col4.metric("Terminados", terminados)

# ==========================================================
# LISTADO DE TURNOS
# ==========================================================

st.subheader("📋 Archivo de Turnos")

df = pd.DataFrame([t.__dict__ for t in archivo_turnos])
st.dataframe(df, use_container_width=True)

# ==========================================================
# AGREGAR TURNO
# ==========================================================

st.subheader("➕ Registrar Nuevo Turno")

with st.form("nuevo_turno"):

    nuevo_id = st.number_input("ID Turno", min_value=1, step=1)
    nueva_patente = st.text_input("Patente")
    nuevo_modelo = st.text_input("Modelo del vehículo")
    nuevo_servicio = st.text_input("Tipo de servicio")
    nuevo_costo = st.number_input("Costo", min_value=0.0)
    nuevo_estado = st.selectbox(
        "Estado",
        ["Pendiente", "En Taller", "Terminado"]
    )

    guardar = st.form_submit_button("Agregar Turno")

    if guardar:

        existe = buscar_por_id(nuevo_id)

        if existe:
            st.error("Ya existe un turno con ese ID.")
        else:
            archivo_turnos.append(
                RegistroTurno(
                    nuevo_id,
                    nueva_patente,
                    nuevo_modelo,
                    nuevo_servicio,
                    nuevo_costo,
                    nuevo_estado
                )
            )
            st.success("Turno agregado correctamente.")

# ==========================================================
# BÚSQUEDA POR ID
# ==========================================================

st.subheader("🔍 Buscar Turno por ID")

id_input = st.number_input(
    "Ingrese el ID del turno",
    value=5001,
    step=1,
    key="buscar_id"
)

if st.button("Buscar ID"):

    resultado = buscar_por_id(id_input)

    if resultado:

        st.success("¡Registro encontrado!")

        st.write(f"**ID:** {resultado.id_turno}")
        st.write(f"**Patente:** {resultado.patente}")
        st.write(f"**Vehículo:** {resultado.modelo_auto}")
        st.write(f"**Servicio:** {resultado.tipo_servicio}")
        st.write(f"**Costo:** ${resultado.costo:,.2f}")

        if resultado.estado == "Terminado":
            st.success(f"Estado: {resultado.estado}")
        elif resultado.estado == "En Taller":
            st.info(f"Estado: {resultado.estado}")
        else:
            st.warning(f"Estado: {resultado.estado}")

    else:
        st.error(f"No se encontró ningún registro con ID {id_input}")

# ==========================================================
# BÚSQUEDA POR PATENTE
# ==========================================================

st.subheader("🚗 Buscar por Patente")

patente_input = st.text_input("Ingrese la patente")

if st.button("Buscar Patente"):

    resultado = buscar_por_patente(patente_input)

    if resultado:
        st.success("Vehículo encontrado")

        st.write(f"**ID:** {resultado.id_turno}")
        st.write(f"**Vehículo:** {resultado.modelo_auto}")
        st.write(f"**Servicio:** {resultado.tipo_servicio}")
        st.write(f"**Estado:** {resultado.estado}")

    else:
        st.error("No se encontró la patente ingresada.")
