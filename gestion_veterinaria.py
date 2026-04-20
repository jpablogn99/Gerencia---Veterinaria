from abc import ABC, abstractmethod

# ======= CLASE ABSTRACTA PERSONA =======
class Persona(ABC):
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    @abstractmethod
    def mostrar_rol(self):
        pass

# ======= CLASE VETERINARIO - HERENCIA =======
class Veterinario(Persona):
    def __init__(self, nombre, documento, especialidad):
        super().__init__(nombre, documento)
        self.especialidad = especialidad
    
    def mostrar_rol(self):
        return f"Veterinario {self.nombre} - Especialidad: {self.especialidad}"
    
    def atender_mascota(self, mascota):
        return f"El veterinario {self.nombre} está atendiendo a {mascota.nombre}"

# ======= CLASE RECEPCIONISTA - HERENCIA =======
class Recepcionista(Persona):
    def __init__(self, nombre, documento):
        super().__init__(nombre, documento)

    def mostrar_rol(self):
        return f"Recepcionista {self.nombre}"
    
    def registrar_cliente(self, cliente):
        return f"Recepcionista {self.nombre} registró al cliente {cliente.nombre}"

# ======= CLASE CLIENTE - HERENCIA con AGREGACIÓN =======
class Cliente(Persona):
    def __init__(self, nombre, documento, telefono):
        super().__init__(nombre, documento)
        self.telefono = telefono
        self.mascotas = []  # AGREGACIÓN: lista de mascotas

    def mostrar_rol(self):
        return f"Cliente {self.nombre} - Dueño de {len(self.mascotas)} mascota(s)"
    
    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)
        print(f"Mascota '{mascota.nombre}' agregada a {self.nombre}")
    
    def mostrar_mascotas(self):
        if not self.mascotas:
            print(f"{self.nombre} no tiene ninguna mascota registrada")
        else:
            print(f"Mascotas de {self.nombre}:")
            for mascota in self.mascotas:
                print(f"  {mascota.mostrar_info()}")

# ======= CLASE MASCOTAS =======
class Mascota:
    def __init__(self, nombre, especie, edad, peso):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.peso = peso 

    def mostrar_info(self):
        return f"{self.nombre} ({self.especie}|{self.edad} años|{self.peso} kg)"

# ======= CLASE TRATAMIENTO (COMPOSICIÓN) =======
class Tratamiento:
    def __init__(self, nombre, costo, duracion_dias):
        self.nombre = nombre
        self.costo = costo
        self.duracion_dias = duracion_dias

    def mostrar_tratamientos(self):
        return f"{self.nombre} | ${self.costo:,} | {self.duracion_dias} días"

# ======= CLASE CONSULTA (ASOCIACIÓN Y COMPOSICIÓN) =======
class Consulta:
    def __init__(self, veterinario, mascota, motivo):
        self.veterinario = veterinario     # ASOCIACIÓN
        self.mascota = mascota             # ASOCIACIÓN
        self.motivo = motivo
        self.diagnostico = ""
        self.tratamientos = []              # COMPOSICIÓN

    def crear_tratamiento(self, nombre, costo, duracion_dias):
        tratamiento = Tratamiento(nombre, costo, duracion_dias)
        self.tratamientos.append(tratamiento)
        print(f"  Tratamiento '{tratamiento.nombre}' agregado")

    def calcular_costo_consulta(self):
        costo_consulta = 50000
        costo_tratamiento = sum(tratamiento.costo for tratamiento in self.tratamientos)
        return costo_consulta + costo_tratamiento
    
    def mostrar_resumen(self):
        print("\n" + "-" * 40)
        print("RESUMEN CONSULTA")
        print("-" * 40)
        print(f"Mascota: {self.mascota.nombre}")
        print(f"Veterinario: {self.veterinario.nombre}")
        print(f"Motivo: {self.motivo}")
        print(f"Diagnóstico: {self.diagnostico}")
        print("Tratamientos:")
        for tratamiento in self.tratamientos:
            print(f"{tratamiento.mostrar_tratamientos()}")
        print(f"Costo total: ${self.calcular_costo_consulta():,}")

# ======= CLASE METODOS PAGO (POLIMORFISMO) =======
class Metodo_pago(ABC):
    @abstractmethod
    def procesar_pago(self, monto): 
        pass
    
class Pago_efectivo(Metodo_pago):
    def procesar_pago(self, monto):
        print(f"Pago en efectivo por ${monto:,}-APROBADO")
        return True
    
class Pago_tarjeta(Metodo_pago):
    def procesar_pago(self, monto):
        print(f"Pago con tarjeta por ${monto:,}-APROBADO")
        return True
    
class Pago_transferencia(Metodo_pago):
    def procesar_pago(self, monto):
        print(f"Transferencia por ${monto:,}-APROBADO")
        return True

# ======= CLASE FACTURA =======
class Factura:
    def __init__(self, consulta, impuesto_IVA=0.19):
        self.consulta = consulta
        self.impuesto_IVA = impuesto_IVA
        self.subtotal = consulta.calcular_costo_consulta()
        self.impuesto = impuesto_IVA * self.subtotal
        self.total = self.impuesto + self.subtotal

    def pagar(self, metodo_pago: Metodo_pago):
        print("\n" + "=" * 40)
        print("FACTURA")
        print("=" * 40)
        print(f"Subtotal: ${self.subtotal:,}")
        print(f"IVA ({int(self.impuesto_IVA*100)}%): ${self.impuesto:,}")
        print(f"TOTAL: ${self.total:,}")
        print("=" * 40)
        return metodo_pago.procesar_pago(self.total)

# ==================== MAIN ====================
def main():
    print("\n" + "=" * 50)
    print("HOSPITAL VETERINARIO")
    print("=" * 50)
    
    # PASO 1: Crear cliente
    print("\n--- REGISTRO DE CLIENTE ---")
    nombre_cliente = input("Nombre del cliente: ").title()
    documento = input("Documento: ")
    telefono = input("Teléfono: ")
    
    cliente = Cliente(nombre_cliente, documento, telefono)
    print(f"Cliente creado: {cliente.nombre}")
    print(f"Rol: {cliente.mostrar_rol()}")
    
    # PASO 2: Agregar mascotas (AGREGACIÓN)
    print("\n--- REGISTRO DE MASCOTAS ---")
    cantidad = int(input("¿Cuántas mascotas quieres registrar? "))
    
    for i in range(cantidad):
        print(f"\nMascota {i+1}")
        nombre_mascota = input("  Nombre: ").title()
        especie = input("  Especie: ").title()
        edad = int(input("  Edad (años): "))
        peso = float(input("  Peso (kg): "))
        
        mascota = Mascota(nombre_mascota, especie, edad, peso)
        cliente.agregar_mascota(mascota)
    
    print("\n--- MIS MASCOTAS ---")
    cliente.mostrar_mascotas()
    print(f"Mascotas: {len(cliente.mascotas)}")
    
    # PASO 3: Crear veterinario
    print("\n--- REGISTRO DE VETERINARIO ---")
    nombre_vet = input("Nombre del veterinario: ").title()
    doc_vet = input("Documento: ")
    especialidad = input("Especialidad: ").title()
    
    veterinario = Veterinario(nombre_vet, doc_vet, especialidad)
    print(f"Veterinario creado: {veterinario.nombre}")
    print(f"Rol: {veterinario.mostrar_rol()}")
    
    # PASO 4: Seleccionar mascota para atender
    print("\n--- SELECCIONAR MASCOTA ---")
    print("Mascotas disponibles:")
    for i in range(len(cliente.mascotas)):
        print(f"{i+1}. {cliente.mascotas[i].mostrar_info()}")
    
    opcion = int(input("Elige una mascota (número): "))
    mascota_atender = cliente.mascotas[opcion - 1]
    
    print(veterinario.atender_mascota(mascota_atender))
    
    # PASO 5: Crear consulta (ASOCIACIÓN)
    print("\n--- REGISTRO DE CONSULTA ---")
    motivo = input("Motivo de la consulta: ").title()
    diagnostico = input("Diagnóstico: ").title()
    
    consulta = Consulta(veterinario, mascota_atender, motivo)
    consulta.diagnostico = diagnostico
    print(f"Consulta creada para {mascota_atender.nombre}")
    
    # PASO 6: Agregar tratamientos (COMPOSICIÓN)
    print("\n--- REGISTRO DE TRATAMIENTOS ---")
    cantidad_trat = int(input("¿Cuántos tratamientos? "))
    
    for i in range(cantidad_trat):
        print(f"\nTratamiento {i+1}")
        nombre_trat = input("  Nombre: ").title()
        costo_trat = float(input("  Costo: $"))
        duracion = int(input("  Duración (días): "))
        
        consulta.crear_tratamiento(nombre_trat, costo_trat, duracion)
    
    # PASO 7: Mostrar resumen
    print("\n--- RESUMEN DE CONSULTA ---")
    consulta.mostrar_resumen()
    
    # PASO 8: Generar factura
    factura = Factura(consulta)
    
    print("\n" + "=" * 40)
    print("FACTURA")
    print("=" * 40)
    print(f"Subtotal: ${factura.subtotal:,.0f}")
    print(f"IVA ({int(factura.impuesto_IVA*100)}%): ${factura.impuesto:,.0f}")
    print(f"TOTAL A PAGAR: ${factura.total:,.0f}")
    print("=" * 40)
   
    
    # PASO 9: Pago con bucle while
       
    print("\n--- MÉTODO DE PAGO ---")
    
    pago_exitoso = False
    
    while pago_exitoso == False:
        print("\nOpciones de pago:")
        print("1 - Efectivo")
        print("2 - Tarjeta")
        print("3 - Transferencia")
        print("0 - Salir sin pagar")
        
        opcion_pago = input("Elige una opción (1, 2, 3 o 0): ")
        
        if opcion_pago == "1":
            print(f"\nValor a pagar: ${factura.total:,.0f}")
            respuesta = input("¿Desea finalizar el pago en efectivo? (Si/No): ").capitalize()
            if respuesta == "Si":
                factura.pagar(Pago_efectivo())
                pago_exitoso = True
                print("\n¡FACTURA PAGADA CON ÉXITO!")
            elif respuesta == "No":
                print("\nPago cancelado. Puedes elegir otro método.\n")
            else:
                print("Opción inválida. Responda Si o No\n")
                
        elif opcion_pago == "2":
            print(f"\nValor a pagar: ${factura.total:,.0f}")
            respuesta = input("¿Desea finalizar el pago con tarjeta? (Si/No): ").capitalize()
            if respuesta == "Si":
                factura.pagar(Pago_tarjeta())
                pago_exitoso = True
                print("\n¡FACTURA PAGADA CON ÉXITO!")
            elif respuesta == "No":
                print("\nPago cancelado. Puedes elegir otro método.\n")
            else:
                print("Opción inválida. Responda Si o No\n")
                
        elif opcion_pago == "3":
            print(f"\nValor a pagar: ${factura.total:,.0f}")
            respuesta = input("¿Desea finalizar la transferencia? (Si/No): ").capitalize()
            if respuesta == "Si":
                factura.pagar(Pago_transferencia())
                pago_exitoso = True
                print("\n¡FACTURA PAGADA CON ÉXITO!")
            elif respuesta == "No":
                print("\nPago cancelado. Puedes elegir otro método.\n")
            else:
                print("Opción inválida. Responda Si o No\n")
                
        elif opcion_pago == "0":
            print("\nCliente decidió no pagar. Saliendo del sistema...")
            break
            
        else:
            print(" Opción inválida. Elige 1, 2, 3 o 0.")

if __name__ == "__main__":
    main()

""" RESULTADO DE LA EJECUCIÓN (SEGÚN DATOS INGRESADOS) -- IGNORE --
==================================================
HOSPITAL VETERINARIO
==================================================

--- REGISTRO DE CLIENTE ---
Nombre del cliente: Juan Pablo Gaitán Navia
Documento: 1054571547
Teléfono: 3007907176
Cliente creado: Juan Pablo Gaitán Navia
Rol: Cliente Juan Pablo Gaitán Navia - Dueño de 0 mascota(s)

--- REGISTRO DE MASCOTAS ---
¿Cuántas mascotas quieres registrar? 2

Mascota 1
  Nombre: Maia
  Especie: Gato
  Edad (años): 7
  Peso (kg): 4
Mascota 'Maia' agregada a Juan Pablo Gaitán Navia

Mascota 2
  Nombre: Goyo
  Especie: Gato
  Edad (años): 3
  Peso (kg): 2
Mascota 'Goyo' agregada a Juan Pablo Gaitán Navia

--- MIS MASCOTAS ---
Mascotas de Juan Pablo Gaitán Navia:
  Maia (Gato|7 años|4.0 kg)
  Goyo (Gato|3 años|2.0 kg)
Mascotas: 2

--- REGISTRO DE VETERINARIO ---
Nombre del veterinario: Julian Parra Jaramillo
Documento: 1054320654
Especialidad: Veterinario Cirujano - Odontologo y Gastroenterologia
Veterinario creado: Julian Parra Jaramillo
Rol: Veterinario Julian Parra Jaramillo - Especialidad: Veterinario Cirujano - Odontologo Y Gastroenterologia

--- SELECCIONAR MASCOTA ---
Mascotas disponibles:
1. Maia (Gato|7 años|4.0 kg)
2. Goyo (Gato|3 años|2.0 kg)
Elige una mascota (número): 2
El veterinario Julian Parra Jaramillo está atendiendo a Goyo

--- REGISTRO DE CONSULTA ---
Motivo de la consulta: Inflamación Aréa Abdominal
Diagnóstico: Ascitis
Consulta creada para Goyo

--- REGISTRO DE TRATAMIENTOS ---
¿Cuántos tratamientos? 3

Tratamiento 1
  Nombre: Oxigeno Terapia
  Costo: $300000
  Duración (días): 3
  Tratamiento 'Oxigeno Terapia' agregado

Tratamiento 2
  Nombre: Diuréticos
  Costo: $130500
  Duración (días): 3
  Tratamiento 'Diuréticos' agregado

Tratamiento 3
  Nombre: Cirugía
  Costo: $700000
  Duración (días): 1
  Tratamiento 'Cirugía' agregado

--- RESUMEN DE CONSULTA ---

----------------------------------------
RESUMEN CONSULTA
----------------------------------------
Mascota: Goyo
Veterinario: Julian Parra Jaramillo
Motivo: Inflamación Aréa Abdominal
Diagnóstico: Ascitis
Tratamientos:
Oxigeno Terapia | $300,000.0 | 3 días
Diuréticos | $130,500.0 | 3 días
Cirugía | $700,000.0 | 1 días
Costo total: $1,180,500.0

========================================
FACTURA
========================================
Subtotal: $1,180,500
IVA (19%): $224,295
TOTAL A PAGAR: $1,404,795
========================================

--- MÉTODO DE PAGO ---

Opciones de pago:
1 - Efectivo
2 - Tarjeta
3 - Transferencia
0 - Salir sin pagar
Elige una opción (1, 2, 3 o 0): 2

Valor a pagar: $1,404,795
¿Desea finalizar el pago con tarjeta? (Si/No): no

Pago cancelado. Puedes elegir otro método.


Opciones de pago:
1 - Efectivo
2 - Tarjeta
3 - Transferencia
0 - Salir sin pagar
Elige una opción (1, 2, 3 o 0): 1

Valor a pagar: $1,404,795
¿Desea finalizar el pago en efectivo? (Si/No): si

========================================
FACTURA
========================================
Subtotal: $1,180,500.0
IVA (19%): $224,295.0
TOTAL: $1,404,795.0
========================================
Pago en efectivo por $1,404,795.0-APROBADO
"""