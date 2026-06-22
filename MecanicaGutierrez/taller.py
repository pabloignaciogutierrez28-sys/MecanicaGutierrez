import streamlit as st
from dataclasses import dataclass
import pandas as pd

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Mecánica Gutiérrez",
    page_icon="🔧",
    layout="wide"
)

# ==========================================================
# BANNER
# ==========================================================

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image(
        "MecanicaGutierrez/banner.jpg",
        width=700
    )

# ==========================================================
# ESTILOS VISUALES
# ==========================================================

st.markdown("""
<style>

/* Título principal */
h1 {
    text-align: center;
}

/* Tarjetas de métricas */
[data-testid="stMetric"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
}

/* Colores de texto métricas */
[data-testid="stMetricLabel"] {
    color: white;
}

[data-testid="stMetricValue"] {
    color: #38bdf8;
    font-size: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

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

st.sidebar.markdown("""
### Sistema de Gestión de Turnos

**Materia:**  
Algoritmos y Estructuras de Datos

**Proyecto:**  
Diseño de E-Commerce con IA

**Alumno:**  
Pablo Ignacio Gutiérrez
""")

# ==========================================================
# ENCABEZADO
# ==========================================================

st.title("🔧 Mecánica Gutiérrez - Gestión de Turnos")

st.info(
    "📌 Clave principal del registro: ID de Turno. "
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

with col1:
    st.metric("📋 Total", total)

with col2:
    st.metric("🔧 En Taller", en_taller)

with col3:
    st.metric("🟡 Pendientes", pendientes)

with col4:
    st.metric("✅ Terminados", terminados)

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
# TAB 2 - BÚSQUEDA SECUENCIAL
# ==========================================================

with tab2:

    st.subheader("🔍 Buscar Turno por ID")

    id_input = st.number_input(
        "Ingrese el ID del turno:",
        min_value=1,
        value=5001,
        step=1
    )

    if st.button("Buscar"):

        encontrado = False

        # Búsqueda Secuencial por la clave principal
        for turno in archivo_turnos:

            if turno.id_turno == id_input:

                st.success("✅ Registro encontrado")

                st.markdown(f"""
### 🚗 Información del Vehículo

**ID de Turno:** {turno.id_turno}

**Patente:** {turno.patente}

**Modelo:** {turno.modelo_auto}

**Servicio:** {turno.tipo_servicio}

**Costo:** ${turno.costo:,.2f}
""")

                if turno.estado == "Terminado":
                    st.success("🟢 Estado: Terminado")

                elif turno.estado == "En Taller":
                    st.info("🔵 Estado: En Taller")

                else:
                    st.warning("🟡 Estado: Pendiente")

                encontrado = True
                break

        if not encontrado:

            st.error(
                f"❌ No se encontró ningún registro con ID {id_input}"
            )

# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.divider()

st.caption(
    "Mecánica Gutiérrez © 2026 | Sistema de Gestión de Turnos"
)
