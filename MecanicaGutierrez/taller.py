import streamlit as st
from dataclasses import dataclass
import pandas as pd
import os

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
        width=500
    )

# ==========================================================
# ESTILOS VISUALES
# ==========================================================

st.markdown("""
<style>

h1 {
    text-align: center;
    color: #0d6efd;
}

[data-testid="stMetric"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DEFINICIÓN DEL REGISTRO Y FUNCIONES
# ==========================================================

@dataclass
class RegistroTurno:
    id_turno: int      # Clave principal
    nombre_cliente: str  # ¡NUEVO!
    telefono: str        # ¡NUEVO!
    patente: str
    modelo_auto: str
    tipo_servicio: str
    costo: float
    estado: str

def guardar_csv():
    datos = []
    for turno in archivo_turnos:
        datos.append({
            "id_turno": turno.id_turno,
            "nombre_cliente": turno.nombre_cliente,  # ¡NUEVO!
            "telefono": turno.telefono,              # ¡NUEVO!
            "patente": turno.patente,
            "modelo_auto": turno.modelo_auto,
            "tipo_servicio": turno.tipo_servicio,
            "costo": turno.costo,
            "estado": turno.estado
        })

    pd.DataFrame(datos).to_csv(
        "turnos.csv",
        index=False
    )

# ==========================================================
# ARCHIVO DE REGISTROS
# ==========================================================

if os.path.exists("turnos.csv"):
    df_csv = pd.read_csv("turnos.csv")
    archivo_turnos = []
    for _, fila in df_csv.iterrows():
        # Validamos que las columnas existan en el CSV viejo para evitar errores de lectura
        nom = fila["nombre_cliente"] if "nombre_cliente" in fila else "No registrado"
        tel = fila["telefono"] if "telefono" in fila else "No registrado"
        
        archivo_turnos.append(
            RegistroTurno(
                int(fila["id_turno"]),
                str(nom),
                str(tel),
                fila["patente"],
                fila["modelo_auto"],
                fila["tipo_servicio"],
                float(fila["costo"]),
                fila["estado"]
            )
        )
else:
    archivo_turnos = []

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🔧 Mecánica Gutiérrez")
st.sidebar.image(
    "MecanicaGutierrez/herramientas.jpg",
    use_container_width=True
)

st.sidebar.info("""
Sistema de Gestión de Turnos

Proyecto:
Diseño de E-Commerce con IA

Alumno:
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

col1.metric("📋 Total", total)
col2.metric("🔧 En Taller", en_taller)
col3.metric("🟡 Pendientes", pendientes)
col4.metric("✅ Terminados", terminados)

# ==========================================================
# PESTAÑAS
# ==========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Turnos",
    "🔍 Buscar",
    "📅 Solicitar Turno",
    "📞 Contacto",
    "🛠️ Administrar"
])

# ==========================================================
# TAB 1 - LISTADO
# ==========================================================

with tab1:
    st.subheader("📋 Archivo de Turnos")
    df = pd.DataFrame([t.__dict__ for t in archivo_turnos])
    
    # Reordenamos las columnas del DataFrame para que visualmente quede lindo
    columnas_ordenadas = ["id_turno", "nombre_cliente", "telefono", "patente", "modelo_auto", "tipo_servicio", "costo", "estado"]
    df = df.reindex(columns=columnas_ordenadas)
    
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
        value=5001,
        step=1
    )

    if st.button("Buscar"):
        encontrado = False
        for turno in archivo_turnos:
            if turno.id_turno == id_input:
                st.success("✅ Registro encontrado")
                
                # Datos Personales agregados a la vista de búsqueda
                st.markdown("### 👤 Datos del Cliente")
                st.write(f"**Nombre y Apellido:** {turno.nombre_cliente}")
                st.write(f"**Teléfono:** {turno.telefono}")
                
                st.markdown("### 🚗 Datos del Vehículo y Servicio")
                st.write(f"**ID de Turno:** {turno.id_turno}")
                st.write(f"**Patente:** {turno.patente}")
                st.write(f"**Vehículo:** {turno.modelo_auto}")
                st.write(f"**Servicio:** {turno.tipo_servicio}")
                st.write(f"**Costo:** ${turno.costo:,.2f}")

                if turno.estado == "Terminado":
                    st.success("🟢 Estado: Terminado")
                elif turno.estado == "En Taller":
                    st.info("🔵 Estado: En Taller")
                else:
                    st.warning("🟡 Estado: Pendiente")

                encontrado = True
                break

        if not encontrado:
            st.error(f"No se encontró ningún registro con ID {id_input}")

# ==========================================================
# TAB 3 - SOLICITAR TURNO
# ==========================================================

with tab3:
    st.subheader("📅 Solicitar Nuevo Turno")
    nombre_cliente = st.text_input("Nombre y Apellido")
    telefono = st.text_input("Teléfono")
    patente = st.text_input("Patente")
    modelo = st.text_input("Modelo del Vehículo")
    servicio = st.selectbox(
        "Tipo de Servicio",
        [
            "Cambio de Aceite",
            "Cambio de Pastillas de Freno",
            "Revisión Eléctrica",
            "Alineación y Balanceo",
            "Diagnóstico General"
        ]
    )
    fecha = st.date_input("Fecha Deseada")

    if st.button("Reservar Turno"):
        if (
            nombre_cliente.strip() == ""
            or telefono.strip() == ""
            or patente.strip() == ""
            or modelo.strip() == ""
        ):
            st.error("⚠️ Complete todos los campos.")
        else:
            nuevo_id = max(
                (turno.id_turno for turno in archivo_turnos), 
                default=0
            ) + 1

            # Pasamos las nuevas variables al Registro
            nuevo_turno = RegistroTurno(
                nuevo_id,
                nombre_cliente.strip(),
                telefono.strip(),
                patente.upper(),
                modelo,
                servicio,
                0.0,
                "Pendiente"
            )

            archivo_turnos.append(nuevo_turno)
            guardar_csv()

            st.success(
                f"✅ Turno reservado correctamente.\n\n"
                f"ID asignado: {nuevo_id}\n\n"
                f"Cliente: {nombre_cliente.strip()}\n\n"
                f"Fecha solicitada: {fecha}"
            )
            st.balloons()

# ==========================================================
# TAB 4 - CONTACTO
# ==========================================================

with tab4:
    st.subheader("📞 Información de Contacto")
    st.markdown("""
### 🔧 Mecánica Gutiérrez

📍 Dirección: Florencia, Santa Fe, Argentina

📞 Teléfono: (3482) 44-49-58

📧 Email: pabloignaciogutierrez28@gmail.com

🕒 Horarios de Atención

- Lunes a Viernes: 08:00 - 12:00 hs  Por la tarde 15:00 - 20:00 hs
- Sábados: 08:00 - 12:00 hs

### 🚗 Servicios

- Mecánica General
- Electricidad Automotriz
- Cambio de Aceite
- Frenos y Suspensión
- Diagnóstico Computarizado
- Alineación y Balanceo
""")
    st.success("¡Gracias por confiar en Mecánica Gutiérrez!")

# ==========================================================
# TAB 5 - ADMINISTRAR TURNOS
# ==========================================================

with tab5:
    st.subheader("🛠️ Administrar Turnos")
    id_admin = st.number_input(
        "Ingrese el ID del turno",
        min_value=1,
        step=1,
        key="admin_id"
    )

    turno_encontrado = None
    for turno in archivo_turnos:
        if turno.id_turno == id_admin:
            turno_encontrado = turno
            break

 if turno_encontrado:

    st.success("✅ Turno encontrado")

    st.write(f"**Cliente:** {turno_encontrado.nombre_cliente}")
    st.write(f"**Patente:** {turno_encontrado.patente}")
    st.write(f"**Vehículo:** {turno_encontrado.modelo_auto}")
    st.write(f"**Servicio:** {turno_encontrado.tipo_servicio}")

    estados = ["Pendiente", "En Taller", "Terminado"]

    nuevo_estado = st.selectbox(
        "Estado del trabajo",
        estados,
        index=estados.index(turno_encontrado.estado)
    )

    nuevo_costo = st.number_input(
        "Costo Final",
        min_value=0.0,
        value=float(turno_encontrado.costo),
        step=1000.0
    )

    if st.button("Guardar Cambios", key="guardar_turno"):

        turno_encontrado.estado = nuevo_estado
        turno_encontrado.costo = nuevo_costo

        guardar_csv()

        st.success("✅ Turno actualizado correctamente")
        st.rerun()

    st.divider()

    if st.button(
        "🗑️ Eliminar Turno",
        key="eliminar_turno"
    ):

        st.session_state.archivo_turnos = [
            t for t in st.session_state.archivo_turnos
            if t.id_turno != turno_encontrado.id_turno
        ]

        guardar_csv()

        st.success(
            "✅ Turno eliminado correctamente"
        )

        st.rerun()

elif id_admin > 0:

    st.warning(
        "No se encontró ningún turno con ese ID."
    )
