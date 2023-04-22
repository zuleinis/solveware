# Define las clases

import random

class InterfazUsuario:
    def __init__(self):
        # Inicializar la interfaz de usuario
        pass
    
    def mostrar_menu(self):
        # Mostrar el menú de opciones disponibles para el usuario
        pass
    
    def llenar_forma(self):
        # Obtener los datos ingresados por el operador del Departamento de Atención al Usuario y guardarlos en el sistema de gestión de reportes
        pass
    
    def consultar_reportes_vigentes(self):
        # Mostrar los reportes de fallas vigentes y permitir al operador asignar un técnico de soporte para atender la falla
        pass
    
    def imprimir_reportes(self, estado=None):
        # Mostrar los reportes de fallas en cualquiera de los tres estados (abierto, en ejecución o cerrado) y permitir su impresión
        pass
    
class ReporteFallas:
    def __init__(self, usuario, descripcion):
        self.numero_reporte = None
        self.estado = 'abierto'
        self.datos = {
            "usuario": usuario,
            "descripcion": descripcion,
            "tecnico": None
        }
    
    def asignar_numero_reporte(self):
        numero = random.randint(100000, 999999)
        self.numero_reporte = numero
    
    def cambiar_estado_reporte(self, nuevo_estado):
        self.estado = nuevo_estado
    
    def editar_datos(self, a_editar, valor):
        if a_editar in self.datos:
            self.datos[a_editar] = valor
        else:
            print("El campo a editar no existe.")

class Usuario:
    def __init__(self, nombre, ubicacion, num_telefono, email):
        self.nombre_completo = nombre
        self.ID = random.randint(100000, 999999)
        self.ubicacion = ubicacion
        self.num_telefono = num_telefono
        self.email = email

    def registrar_usuario(self):
        # Registrar un nuevo usuario en el sistema de gestión de usuarios
        pass
    
    def editar_nombre(self, nuevo_nombre):
        self.nombre_completo = nuevo_nombre
    
    def editar_email(self, nuevo_email):
        self.email = nuevo_email
    
    def editar_tel(self, nuevo_telefono):
        self.num_telefono = nuevo_telefono
    
    def editar_ubicacion(self, nueva_ubicacion):
        self.ubicacion = nueva_ubicacion

class GeneradorReportes:
    def __init__(self, lista_reportes):
        self.lista_reportes = lista_reportes
    
    def promedio_fallas(self, fecha_inicial, fecha_final):
        # Calcular y escribir el promedio de fallas reportadas dada una fecha inicial y una fecha final
        pass
    
    def equipos_con_mas_fallas(self, fecha_inicial, fecha_final):
        # Escribir los códigos y ubicaciones de aquellos equipos que presentaron el mayor número de fallas en un intervalo de fechas dado
        pass
    
    def reportes_por_mes(self, mes, anio):
        # Escribir todos los reportes de fallas que se recibieron en un mes y año dado
        pass
    
    def usuario_con_mas_fallas(self, fecha_inicial, fecha_final):
        # Escribir el nombre y ID del usuario que realizó el mayor número de reportes de fallas en un intervalo de fechas dado.
        # En caso de haber más de un usuario con el mismo número mayor de fallas, se deben escribir los datos de todos estos usuarios.
        pass
