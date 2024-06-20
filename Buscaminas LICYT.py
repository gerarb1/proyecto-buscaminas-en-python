#-------------------------------IMPORTACIONES------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import tkinter as tk                                                                                             #tkinter: Biblioteca para crear interfaces gráficas. 
from tkinter import messagebox                                                                                   #simpledialog y messagebox: Módulos de tkinter para diálogos sencillos y mensajes emergentes.
import random                                                                                                    #random: Biblioteca para generar números aleatorios.
import time                                                                                                      #time: Biblioteca para funciones relacionadas con el tiempo.

#-------------------------------CLASE BUSCAMINAS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Buscaminas:
    def __init__(self, maestro, filas, columnas, minas):                                                         # Inicializa el juego configurando la ventana, los elementos gráficos y el temporizador.
        self.maestro = maestro
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.botones = []
        self.posiciones_minas = set()
        self.posiciones_banderas = set()
        self.posiciones_reveladas = set()
        self.juego_terminado = False
        self.tiempo_inicio = time.time()

        self.maestro.configure(bg='dark orange')                                                                  #fondo naranja oscuro para la ventana principal.
        self.maestro.resizable(True, True)

        self.marco = tk.Frame(self.maestro, bg='black')                                                           #color negro para los bordes de las casillas.
        self.marco.grid(row=0, column=0, padx=10, pady=10)
        
        self.etiqueta_tiempo = tk.Label(self.maestro, text="Tiempo: 0", bg='black', fg='white', font=('Helvetica', 32))  #crea el boton del tiempo, tamaño y color del boton.
        self.etiqueta_tiempo.grid(row=1, column=0, columnspan=self.columnas)
        self.actualizar_tiempo()

        self.crear_widgets()
        self.colocar_minas()
        self.centrar_ventana(self.maestro)

#---------------------------CREAR WIDGETS--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
    def crear_widgets(self):                                                                                       #configura el entorno gráfico del juego de Buscaminas, inicializa las variables necesarias y establece la interfaz gráfica de usuario (ventana, marco y temporizador).
        for fila in range(self.filas):
            fila_botones = []
            for columna in range(self.columnas):
                boton = tk.Button(
                    self.marco,
                    width=2,                                                                                       #Modifica el tamaño de lo ancho de las casillas.
                    height=1,                                                                                      #Modifica el tamaño de lo alto de las casillas.
                    command=lambda f=fila, c=columna: self.click(f, c),
                    highlightthickness=1,
                    highlightbackground="black",
                    bg="gray",                                                                                     #Fondo gris para los botones
                    fg="white",                                                                                    #Texto blanco para los botones
                )
                boton.bind('<Button-3>', lambda e, f=fila, c=columna: self.banderilla(f, c))                       #Permite hacer click izquierdo y derecho para revelar casillas y poner banderas
                boton.grid(row=fila, column=columna, padx=1, pady=1)
                fila_botones.append(boton)
            self.botones.append(fila_botones)

#-------------------------COLOCAR MINAS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def colocar_minas(self):                                                                                       # Coloca las minas en posiciones aleatorias dentro de la cuadrícula.
        while len(self.posiciones_minas) < self.minas:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            self.posiciones_minas.add((f, c))

    def click(self, f, c):                                                                                         # Maneja los clics del usuario en los botones. Revela una casilla o muestra una mina y termina el juego.
        if self.juego_terminado:
            return

        if (f, c) in self.posiciones_banderas:
            return

        if (f, c) in self.posiciones_minas:
            self.botones[f][c].config(text='💣', bg='red')                                                        #Se usara el emoji 💣 para las minas y se marcara de color rojo cuando este explote.
            self.juego_terminado = True
            self.mostrar_todas_minas()
            messagebox.showinfo("Game Over", "Has perdido!")                                                      #Muestra un mensaje emergente que el jugador perdio el juego
        else:
            self.revelar(f, c)
            if self.verificar_victoria():
                self.juego_terminado = True
                messagebox.showinfo("Congratulations", "Has ganado!")                                             #Muestra un mensaje emergente que el jugador gano el juego

#-------------------------REVELAR CELDAS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def revelar(self, f, c):                                                                                      # Revela una casilla y, si no tiene minas adyacentes, revela recursivamente las casillas adyacentes.
        if (f, c) in self.posiciones_reveladas:
            return

        self.posiciones_reveladas.add((f, c))
        minas_adyacentes = self.contar_minas_adyacentes(f, c)
        self.botones[f][c].config(text=str(minas_adyacentes) if minas_adyacentes > 0 else '', bg='black')

        if minas_adyacentes == 0:
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= f + df < self.filas and 0 <= c + dc < self.columnas:
                        self.revelar(f + df, c + dc)

#-------------------------CONTAR MINAS ADYACENTES------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def contar_minas_adyacentes(self, f, c):                                                                      # Cuenta las minas adyacentes a una casilla.
        cuenta = 0
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                if 0 <= f + df < self.filas and 0 <= c + dc < self.columnas:
                    if (f + df, c + dc) in self.posiciones_minas:
                        cuenta += 1
        return cuenta
    
#-------------------------MARCAR CON BANDERA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def banderilla(self, f, c):                                                                                   # Marca una casilla con una bandera 🚩 para indicar una mina potencial.
        if self.juego_terminado:
            return

        if self.botones[f][c]['text'] == '':
            self.botones[f][c].config(text='🚩', bg='grey')
            self.posiciones_banderas.add((f, c))
        elif self.botones[f][c]['text'] == '🚩':
            self.botones[f][c].config(text='')
            self.posiciones_banderas.remove((f, c))

#-------------------------MOSTRAR MINAS------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def mostrar_todas_minas(self):                                                                                # Muestra todas las minas en la cuadrícula.
        for f, c in self.posiciones_minas:
            self.botones[f][c].config(text='💣')

#-------------------------VERIFICAR VICTOIA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def verificar_victoria(self):                                                                                 # Verifica si todas las minas han sido correctamente marcadas.
        return all((f, c) in self.posiciones_banderas for f, c in self.posiciones_minas)
    
#-------------------------TIEMPO------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def actualizar_tiempo(self):                                                                                  # Actualiza el temporizador cada segundo.
        if not self.juego_terminado:
            tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
            self.etiqueta_tiempo.config(text=f"Tiempo: {tiempo_transcurrido}")
            self.maestro.after(1000, self.actualizar_tiempo)

#-------------------------CENTRAR VENTANA DEL TABLERO EN LA PANTALLA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def centrar_ventana(self, ventana):                                                                           # Centra la ventana en la pantalla.
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))

#-------------------------INICIO DE JUEGO ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def iniciar_juego(dificultad):                                                                                    # Inicia una nueva partida del buscaminas con la dificultad seleccionada.
    if dificultad == 'facil':
        filas, columnas, minas = 8, 8, 8                                                                          #Inicia la partida con 8x8 casillas y 8 minas.
    elif dificultad == 'medio':
        filas, columnas, minas = 12, 12, 16                                                                       #Inicia la partida con 12x12 casillas y 16 minas.
    elif dificultad == 'dificil':
        filas, columnas, minas = 20, 20, 40                                                                       #Inicia la partida con 20x20 casillas y 40 minas.
    else:
        return

    ventana_juego = tk.Toplevel()
    ventana_juego.title('Buscaminas')
    Buscaminas(ventana_juego, filas, columnas, minas)

#---------------------FUNCION PRINCIPAL----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():                                                                                                       # Configura la ventana principal del juego y los botones para seleccionar la dificultad.
    raiz = tk.Tk()
    raiz.title('Buscaminas')
    raiz.configure(bg='dark orange')
    raiz.resizable(True, True)

    tk.Button(raiz, text="Fácil", command=lambda: iniciar_juego('facil')).pack(fill=tk.BOTH)                      #Boton de modo facil 
    tk.Button(raiz, text="Medio", command=lambda: iniciar_juego('medio')).pack(fill=tk.BOTH)                      #Boton de modo medio
    tk.Button(raiz, text="Difícil", command=lambda: iniciar_juego('dificil')).pack(fill=tk.BOTH)                  #Boton de modo dificil

    centrar_ventana(raiz)
    raiz.mainloop()

#-------------------------CENTRAR VENTANA DEL MENU EN LA PANTALLA------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def centrar_ventana(ventana):                                                                                     # Centra una ventana en la pantalla.
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 7) - (alto // 7)
    ventana.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))

#-------------------------LLAMADA FINAL A LA FUNCION PRINCIPAL main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":                                                                                        #Condición especial en Python que verifica si el script actual se está ejecutando directamente como programa principal.
    main()                                                                                                        #Esto significa que la función main() se ejecutará solo si el script se está ejecutando directamente como programa principal.