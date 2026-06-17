# =====================================================================
# ALGORITMOS Y ESTRUCTURAS DE DATOS - ISI 2026
# TRABAJO PRÁCTICO: DISEÑO DE E-COMMERCE CON IA
# ALUMNO: PABLO IGNACIO GUTIERREZ
# PROYECTO: MECÁNICA GUTIÉRREZ
# =====================================================================

# Definición de la estructura tipo registro (Unidad 2)
class RegistroTurno:
    def __init__(self, id_turno, patente, modelo_auto, tipo_servicio, costo, estado):
        self.id_turno = id_turno  # <--- CLAVE PRINCIPAL
        self.patente = patente
        self.modelo_auto = modelo_auto
        self.tipo_servicio = tipo_servicio
        self.costo = costo
        self.estado = estado

    def mostrar_registro(self):
        print(f"Turno ID: {self.id_turno:<6} | Patente: {self.patente:<9} | Vehículo: {self.modelo_auto:<20} | Servicio: {self.tipo_servicio:<25} | Costo: ${self.costo:<10.2f} | Estado: {self.estado}")


# --- PROGRAMA PRINCIPAL (Simulación del Backend de Mecánica Gutiérrez) ---
if __name__ == "__main__":
    # Estructura contenedora que simula nuestro archivo de registros en memoria
    archivo_turnos = []

    # Alta y carga de registros (Datos de prueba simulando compras en la web)
    t1 = RegistroTurno(5001, "AA890BB", "Volkswagen Amarok", "Cambio Filtros y Aceite", 45000.00, "En Taller")
    t2 = RegistroTurno(5002, "AF543CC", "Ford Focus", "Cambio de Pastillas Freno", 32000.00, "Pendiente")
    t3 = RegistroTurno(5003, "LOK789", "Renault Clio", "Revisión Eléctrica", 15000.00, "Terminado")

    # Insertamos los registros en nuestra estructura de datos
    archivo_turnos.append(t1)
    archivo_turnos.append(t2)
    archivo_turnos.append(t3)

    # Listar el contenido del archivo
    print("=" * 115)
    print(" " * 35 + "SISTEMA DE GESTIÓN INTERNA - MECÁNICA GUTIÉRREZ")
    print("=" * 115)
    for turno in archivo_turnos:
        turno.mostrar_registro()
    print("=" * 115)

    # Algoritmo de Búsqueda Secuencial por campo CLAVE (id_turno)
    clave_buscada = 5002
    print(f"\n[BÚSQUEDA] Iniciando exploración en archivo para la clave (ID): {clave_buscada}...")
    
    encontrado = False
    for turno in archivo_turnos:
        if turno.id_turno == clave_buscada:
            print("¡Registro localizado con éxito!")
            turno.mostrar_registro()
            encontrado = True
            break # Rompemos el ciclo al encontrar la clave única
            
    if not encontrado:
        print(f"Error: No se encontró ningún registro bajo la clave {clave_buscada}.")
