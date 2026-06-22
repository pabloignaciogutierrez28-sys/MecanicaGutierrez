import streamlit as st
from dataclasses import dataclass
import pandas as pd

# ==========================================================
# ESTILOS VISUALES
# ==========================================================

st.set_page_config(
    page_title="Mecánica Gutiérrez",
    page_icon="🔧",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    color: #0d6efd;
    text-align: center;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #dddddd;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# DEFINICIÓN DEL REGISTRO
# ==========================================================

@dataclass
class RegistroTurno:
    id_turno: int      # Clave principal
    patente: str
    modelo_auto: str
    tipo_servicio: str
    costo: float
    estado: str


# ==========================================================
# ARCHIVO DE REGISTROS
# ==========================================================

archivo_turnos = [
    RegistroTurno(
        5001,
        "AA890BB",
        "Volkswagen Amarok",
        "Cambio Filtros y Aceite",
        45000.0,
        "En Taller"
    ),
    RegistroTurno(
        5002,
        "AF543CC",
        "Ford Focus",
        "Cambio de Pastillas Freno",
        32000.0,
        "Pendiente"
    ),
    RegistroTurno(
        5003,
        "LOK789",
        "Renault Clio",
        "Revisión Eléctrica",
        15000.0,
        "Terminado"
    )
]

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🔧 Mecánica Gutiérrez")

st.sidebar.info("""
Sistema de Gestión de Turnos

Materia:
Algoritmos y Estructuras de Datos

Proyecto:
Diseño de E-Commerce con IA
""")

# ==========================================================
# ENCABEZADO
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
# PESTAÑAS
# ==========================================================

tab1, tab2 = st.tabs([
    "📋 Turnos",
    "🔍 Buscar"
])

# ==========================================================
# TAB 1 - LISTADO
# ==========================================================

with tab1:

    st.subheader("📋 Archivo de Turnos")

    df = pd.DataFrame([t.__dict__ for t in archivo_turnos])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# TAB 2 - BÚSQUEDA
# ==========================================================

with tab2:

    st.subheader("🔍 Buscar Turno por ID")

    id_input = st.number_input(
        "Ingrese el ID del turno:",
        value=5001,
        step=1
    )

    if st.button("Buscar"):

        encontrado = False

        for turno in archivo_turnos:

            if turno.id_turno == id_input:

                st.success("¡Registro encontrado!")

                st.write(f"**ID:** {turno.id_turno}")
                st.write(f"**Patente:** {turno.patente}")
                st.write(f"**Vehículo:** {turno.modelo_auto}")
                st.write(f"**Servicio:** {turno.tipo_servicio}")
                st.write(f"**Costo:** ${turno.costo:,.2f}")

                if turno.estado == "Terminado":
                    st.success("🟢 Terminado")

                elif turno.estado == "En Taller":
                    st.info("🔵 En Taller")

                else:
                    st.warning("🟡 Pendiente")

                encontrado = True
                break

        if not encontrado:
            st.error(
                f"No se encontró ningún registro con ID {id_input}"
            )
