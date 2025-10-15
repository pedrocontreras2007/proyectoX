import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class CreadorRecorridosBuses:
    def __init__(self, root):
        self.root = root
        self.root.title("🚍 Creador de Recorridos de Buses")
        self.root.geometry("700x600")
        
        # Datos
        self.rutas = {}
        self.buses = {}
        self.archivo_datos = "datos_buses.json"
        
        # Cargar datos existentes
        self.cargar_datos()
        
        self.crear_interfaz()
    
    def cargar_datos(self):
        """Cargar datos desde archivo JSON"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.rutas = datos.get('rutas', {})
                    self.buses = datos.get('buses', {})
            except:
                self.rutas = {}
                self.buses = {}
    
    def guardar_datos(self):
        """Guardar datos en archivo JSON"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump({
                    'rutas': self.rutas,
                    'buses': self.buses
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
    
    def crear_interfaz(self):
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Crear Rutas
        self.crear_pestana_rutas(notebook)
        
        # Pestaña 2: Gestionar Buses
        self.crear_pestana_buses(notebook)
        
        # Pestaña 3: Ver Recorridos
        self.crear_pestana_recorridos(notebook)
        
        # Pestaña 4: Simulación
        self.crear_pestana_simulacion(notebook)
    
    def crear_pestana_rutas(self, notebook):
        """Pestaña para crear y gestionar rutas"""
        frame_rutas = ttk.Frame(notebook)
        notebook.add(frame_rutas, text="📍 Crear Rutas")
        
        # Título
        ttk.Label(frame_rutas, text="CREAR NUEVA RUTA", font=("Arial", 14, "bold"))\
            .pack(pady=10)
        
        # Formulario para nueva ruta
        form_frame = ttk.LabelFrame(frame_rutas, text=" Información de la Ruta ", padding="10")
        form_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(form_frame, text="Nombre de la Ruta:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nombre_ruta = ttk.Entry(form_frame, width=30)
        self.entry_nombre_ruta.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Agregar Parada:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_parada = ttk.Entry(form_frame, width=30)
        self.entry_parada.grid(row=1, column=1, pady=5, padx=5)
        
        # Botones para paradas
        btn_frame_paradas = ttk.Frame(form_frame)
        btn_frame_paradas.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame_paradas, text="➕ Agregar Parada", 
                  command=self.agregar_parada_lista).pack(side='left', padx=5)
        ttk.Button(btn_frame_paradas, text="🗑️ Limpiar Paradas", 
                  command=self.limpiar_paradas).pack(side='left', padx=5)
        
        # Lista de paradas
        ttk.Label(form_frame, text="Paradas de la Ruta:").grid(row=3, column=0, sticky='w', pady=5)
        self.lista_paradas = tk.Listbox(form_frame, width=40, height=8)
        self.lista_paradas.grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')
        
        # Botones de gestión de paradas
        btn_frame_lista = ttk.Frame(form_frame)
        btn_frame_lista.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame_lista, text="⬆️ Subir", 
                  command=self.subir_parada).pack(side='left', padx=2)
        ttk.Button(btn_frame_lista, text="⬇️ Bajar", 
                  command=self.bajar_parada).pack(side='left', padx=2)
        ttk.Button(btn_frame_lista, text="✏️ Editar", 
                  command=self.editar_parada).pack(side='left', padx=2)
        ttk.Button(btn_frame_lista, text="❌ Eliminar", 
                  command=self.eliminar_parada).pack(side='left', padx=2)
        
        # Botón crear ruta
        ttk.Button(form_frame, text="🚍 Crear Ruta", 
                  command=self.crear_ruta, style='Accent.TButton')\
            .grid(row=6, column=0, columnspan=2, pady=10)
        
        # Lista de rutas existentes
        list_frame = ttk.LabelFrame(frame_rutas, text=" Rutas Existentes ", padding="10")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree_rutas = ttk.Treeview(list_frame, columns=('Nombre', 'Paradas'), show='headings', height=8)
        self.tree_rutas.heading('Nombre', text='Nombre Ruta')
        self.tree_rutas.heading('Paradas', text='N° de Paradas')
        self.tree_rutas.column('Nombre', width=200)
        self.tree_rutas.column('Paradas', width=100)
        self.tree_rutas.pack(fill='both', expand=True)
        
        # Botones para rutas existentes
        btn_frame_rutas = ttk.Frame(list_frame)
        btn_frame_rutas.pack(pady=5)
        
        ttk.Button(btn_frame_rutas, text="🔄 Actualizar Lista", 
                  command=self.actualizar_lista_rutas).pack(side='left', padx=5)
        ttk.Button(btn_frame_rutas, text="👀 Ver Detalles", 
                  command=self.ver_detalles_ruta).pack(side='left', padx=5)
        ttk.Button(btn_frame_rutas, text="🗑️ Eliminar Ruta", 
                  command=self.eliminar_ruta).pack(side='left', padx=5)
        
        # Cargar lista inicial
        self.actualizar_lista_rutas()
    
    def crear_pestana_buses(self, notebook):
        """Pestaña para gestionar buses"""
        frame_buses = ttk.Frame(notebook)
        notebook.add(frame_buses, text="🚌 Gestionar Buses")
        
        ttk.Label(frame_buses, text="GESTIONAR FLOTA DE BUSES", font=("Arial", 14, "bold"))\
            .pack(pady=10)
        
        # Formulario para nuevo bus
        form_frame = ttk.LabelFrame(frame_buses, text=" Agregar Nuevo Bus ", padding="10")
        form_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(form_frame, text="Número de Bus:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_numero_bus = ttk.Entry(form_frame, width=20)
        self.entry_numero_bus.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Ruta Asignada:").grid(row=1, column=0, sticky='w', pady=5)
        self.combo_ruta_bus = ttk.Combobox(form_frame, width=20)
        self.combo_ruta_bus.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Capacidad:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_capacidad = ttk.Entry(form_frame, width=20)
        self.entry_capacidad.insert(0, "40")
        self.entry_capacidad.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Button(form_frame, text="➕ Agregar Bus", 
                  command=self.agregar_bus).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Lista de buses
        list_frame = ttk.LabelFrame(frame_buses, text=" Buses en Flota ", padding="10")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tree_buses = ttk.Treeview(list_frame, 
                                     columns=('Bus', 'Ruta', 'Capacidad', 'Estado'), 
                                     show='headings', 
                                     height=10)
        
        self.tree_buses.heading('Bus', text='N° de Bus')
        self.tree_buses.heading('Ruta', text='Ruta Asignada')
        self.tree_buses.heading('Capacidad', text='Capacidad')
        self.tree_buses.heading('Estado', text='Estado')
        
        self.tree_buses.column('Bus', width=100)
        self.tree_buses.column('Ruta', width=150)
        self.tree_buses.column('Capacidad', width=80)
        self.tree_buses.column('Estado', width=100)
        
        self.tree_buses.pack(fill='both', expand=True)
        
        # Actualizar combobox de rutas
        self.actualizar_combo_rutas()
        self.actualizar_lista_buses()
    
    def crear_pestana_recorridos(self, notebook):
        """Pestaña para ver recorridos"""
        frame_recorridos = ttk.Frame(notebook)
        notebook.add(frame_recorridos, text="🗺️ Ver Recorridos")
        
        ttk.Label(frame_recorridos, text="VISUALIZAR RECORRIDOS", font=("Arial", 14, "bold"))\
            .pack(pady=10)
        
        # Selección de ruta
        selec_frame = ttk.Frame(frame_recorridos)
        selec_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(selec_frame, text="Seleccionar Ruta:").pack(side='left', padx=5)
        self.combo_rutas_ver = ttk.Combobox(selec_frame, width=30)
        self.combo_rutas_ver.pack(side='left', padx=5)
        self.combo_rutas_ver.bind('<<ComboboxSelected>>', self.mostrar_recorrido)
        
        # Área de visualización
        vis_frame = ttk.LabelFrame(frame_recorridos, text=" Recorrido ", padding="15")
        vis_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.text_recorrido = tk.Text(vis_frame, width=60, height=15, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(vis_frame, orient='vertical', command=self.text_recorrido.yview)
        self.text_recorrido.configure(yscrollcommand=scrollbar.set)
        
        self.text_recorrido.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Actualizar combobox
        self.actualizar_combo_rutas_ver()
    
    def crear_pestana_simulacion(self, notebook):
        """Pestaña para simulación en tiempo real"""
        frame_sim = ttk.Frame(notebook)
        notebook.add(frame_sim, text="🎮 Simulación")
        
        ttk.Label(frame_sim, text="SIMULACIÓN EN TIEMPO REAL", font=("Arial", 14, "bold"))\
            .pack(pady=10)
        
        # Controles de simulación
        controls_frame = ttk.LabelFrame(frame_sim, text=" Controles ", padding="10")
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="▶️ Iniciar Simulación", 
                  command=self.iniciar_simulacion).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="⏸️ Pausar", 
                  command=self.pausar_simulacion).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="🔄 Reiniciar", 
                  command=self.reiniciar_simulacion).pack(side='left', padx=5)
        
        # Área de simulación
        sim_frame = ttk.LabelFrame(frame_sim, text=" Estado Actual ", padding="10")
        sim_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.text_simulacion = tk.Text(sim_frame, width=60, height=15, font=("Courier", 9))
        self.text_simulacion.pack(fill='both', expand=True)
        
        # Estado inicial
        self.text_simulacion.insert('1.0', "Simulación lista...\n")
        self.text_simulacion.insert('end', "Presiona 'Iniciar Simulación' para comenzar\n")
    
    # Métodos para gestión de rutas
    def agregar_parada_lista(self):
        parada = self.entry_parada.get().strip()
        if parada:
            self.lista_paradas.insert(tk.END, parada)
            self.entry_parada.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Escribe el nombre de la parada")
    
    def limpiar_paradas(self):
        self.lista_paradas.delete(0, tk.END)
    
    def subir_parada(self):
        try:
            indice = self.lista_paradas.curselection()[0]
            if indice > 0:
                item = self.lista_paradas.get(indice)
                self.lista_paradas.delete(indice)
                self.lista_paradas.insert(indice-1, item)
                self.lista_paradas.select_set(indice-1)
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una parada")
    
    def bajar_parada(self):
        try:
            indice = self.lista_paradas.curselection()[0]
            if indice < self.lista_paradas.size()-1:
                item = self.lista_paradas.get(indice)
                self.lista_paradas.delete(indice)
                self.lista_paradas.insert(indice+1, item)
                self.lista_paradas.select_set(indice+1)
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una parada")
    
    def editar_parada(self):
        try:
            indice = self.lista_paradas.curselection()[0]
            item_actual = self.lista_paradas.get(indice)
            nuevo_nombre = tk.simpledialog.askstring("Editar Parada", "Nuevo nombre:", initialvalue=item_actual)
            if nuevo_nombre:
                self.lista_paradas.delete(indice)
                self.lista_paradas.insert(indice, nuevo_nombre)
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una parada para editar")
    
    def eliminar_parada(self):
        try:
            indice = self.lista_paradas.curselection()[0]
            self.lista_paradas.delete(indice)
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una parada para eliminar")
    
    def crear_ruta(self):
        nombre_ruta = self.entry_nombre_ruta.get().strip()
        paradas = list(self.lista_paradas.get(0, tk.END))
        
        if not nombre_ruta:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para la ruta")
            return
        
        if len(paradas) < 2:
            messagebox.showwarning("Advertencia", "Agrega al menos 2 paradas")
            return
        
        if nombre_ruta in self.rutas:
            messagebox.showwarning("Advertencia", "Ya existe una ruta con ese nombre")
            return
        
        self.rutas[nombre_ruta] = paradas
        self.guardar_datos()
        self.actualizar_lista_rutas()
        self.actualizar_combo_rutas()
        self.actualizar_combo_rutas_ver()
        
        messagebox.showinfo("Éxito", f"Ruta '{nombre_ruta}' creada correctamente")
        self.entry_nombre_ruta.delete(0, tk.END)
        self.limpiar_paradas()
    
    def actualizar_lista_rutas(self):
        for item in self.tree_rutas.get_children():
            self.tree_rutas.delete(item)
        
        for nombre, paradas in self.rutas.items():
            self.tree_rutas.insert('', tk.END, values=(nombre, len(paradas)))
    
    def ver_detalles_ruta(self):
        try:
            item = self.tree_rutas.selection()[0]
            nombre_ruta = self.tree_rutas.item(item)['values'][0]
            paradas = self.rutas[nombre_ruta]
            
            detalles = f"Ruta: {nombre_ruta}\n\nParadas:\n"
            for i, parada in enumerate(paradas, 1):
                detalles += f"{i}. {parada}\n"
            
            messagebox.showinfo(f"Detalles - {nombre_ruta}", detalles)
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una ruta")
    
    def eliminar_ruta(self):
        try:
            item = self.tree_rutas.selection()[0]
            nombre_ruta = self.tree_rutas.item(item)['values'][0]
            
            confirmar = messagebox.askyesno(
                "Confirmar Eliminación", 
                f"¿Estás seguro de eliminar la ruta '{nombre_ruta}'?"
            )
            
            if confirmar:
                del self.rutas[nombre_ruta]
                self.guardar_datos()
                self.actualizar_lista_rutas()
                self.actualizar_combo_rutas()
                self.actualizar_combo_rutas_ver()
                messagebox.showinfo("Éxito", "Ruta eliminada correctamente")
                
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una ruta")
    
    # Métodos para gestión de buses
    def actualizar_combo_rutas(self):
        self.combo_ruta_bus['values'] = list(self.rutas.keys())
    
    def actualizar_combo_rutas_ver(self):
        self.combo_rutas_ver['values'] = list(self.rutas.keys())
    
    def agregar_bus(self):
        numero_bus = self.entry_numero_bus.get().strip()
        ruta = self.combo_ruta_bus.get()
        capacidad = self.entry_capacidad.get().strip()
        
        if not numero_bus:
            messagebox.showwarning("Advertencia", "Ingresa el número del bus")
            return
        
        if not ruta:
            messagebox.showwarning("Advertencia", "Selecciona una ruta")
            return
        
        if not capacidad.isdigit() or int(capacidad) <= 0:
            messagebox.showwarning("Advertencia", "Ingresa una capacidad válida")
            return
        
        if numero_bus in self.buses:
            messagebox.showwarning("Advertencia", "Ya existe un bus con ese número")
            return
        
        self.buses[numero_bus] = {
            'ruta': ruta,
            'capacidad': int(capacidad),
            'estado': 'Disponible'
        }
        
        self.guardar_datos()
        self.actualizar_lista_buses()
        
        messagebox.showinfo("Éxito", f"Bus {numero_bus} agregado correctamente")
        self.entry_numero_bus.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)
        self.entry_capacidad.insert(0, "40")
    
    def actualizar_lista_buses(self):
        for item in self.tree_buses.get_children():
            self.tree_buses.delete(item)
        
        for numero, info in self.buses.items():
            self.tree_buses.insert('', tk.END, values=(
                numero, 
                info['ruta'], 
                info['capacidad'],
                info['estado']
            ))
    
    # Métodos para visualización
    def mostrar_recorrido(self, event=None):
        ruta_seleccionada = self.combo_rutas_ver.get()
        
        if ruta_seleccionada in self.rutas:
            paradas = self.rutas[ruta_seleccionada]
            
            self.text_recorrido.delete('1.0', tk.END)
            self.text_recorrido.insert('1.0', f"🚍 RECORRIDO: {ruta_seleccionada}\n\n")
            
            for i, parada in enumerate(paradas, 1):
                self.text_recorrido.insert('end', f"📍 Parada {i}: {parada}\n")
            
            # Mostrar buses en esta ruta
            buses_en_ruta = [bus for bus, info in self.buses.items() if info['ruta'] == ruta_seleccionada]
            if buses_en_ruta:
                self.text_recorrido.insert('end', f"\n🚌 Buses en esta ruta: {', '.join(buses_en_ruta)}")
            else:
                self.text_recorrido.insert('end', "\n⚠️ No hay buses asignados a esta ruta")
    
    # Métodos para simulación
    def iniciar_simulacion(self):
        self.text_simulacion.delete('1.0', tk.END)
        self.text_simulacion.insert('1.0', "=== SIMULACIÓN INICIADA ===\n\n")
        
        if not self.buses:
            self.text_simulacion.insert('end', "No hay buses en la flota\n")
            return
        
        for bus, info in self.buses.items():
            ruta = info['ruta']
            paradas = self.rutas.get(ruta, [])
            
            self.text_simulacion.insert('end', f"🚍 Bus {bus} (Ruta: {ruta}):\n")
            
            if paradas:
                # Simular posición aleatoria
                import random
                posicion = random.randint(0, len(paradas)-1)
                siguiente = (posicion + 1) % len(paradas)
                
                self.text_simulacion.insert('end', f"   🟢 En: {paradas[posicion]}\n")
                self.text_simulacion.insert('end', f"   ➡️ Siguiente: {paradas[siguiente]}\n")
                self.text_simulacion.insert('end', f"   👥 Pasajeros: {random.randint(5, info['capacidad'])}/{info['capacidad']}\n\n")
            else:
                self.text_simulacion.insert('end', f"   ⚠️ Ruta sin paradas definidas\n\n")
    
    def pausar_simulacion(self):
        self.text_simulacion.insert('end', "\n⏸️ Simulación pausada\n")
    
    def reiniciar_simulacion(self):
        self.text_simulacion.delete('1.0', tk.END)
        self.text_simulacion.insert('1.0', "Simulación reiniciada...\n")
        self.text_simulacion.insert('end', "Presiona 'Iniciar Simulación' para comenzar\n")

def main():
    root = tk.Tk()
    app = CreadorRecorridosBuses(root)
    root.mainloop()

if __name__ == "__main__":
    main()