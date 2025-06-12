import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import edge_tts
import asyncio
import os
import re
import threading
from datetime import datetime

class InterfazGeneradorAudio:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎙️ Generador de Audio TTS - Calidad de Estudio")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.voz = tk.StringVar(value="es-MX-DaliaNeural")
        self.velocidad = tk.StringVar(value="-10%")  # Equivalente a 0.9x
        self.nombre_proyecto = tk.StringVar(value="mi_audio")
        self.modo_generacion = tk.StringVar(value="unico")  # "unico" o "segmentos"
        self.carpeta_salida = "audios_generados"
        self.generando = False
        
        self.crear_interfaz()
        self.cargar_texto_ejemplo()
    
    def crear_interfaz(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2b2b2b', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#2b2b2b', foreground='#4CAF50')
        style.configure('Info.TLabel', font=('Arial', 10), background='#2b2b2b', foreground='#cccccc')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎙️ Generador de Audio TTS - Calidad de Estudio", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame de configuración
        config_frame = tk.LabelFrame(main_frame, text="⚙️ Configuración", bg='#3b3b3b', fg='white', font=('Arial', 11, 'bold'))
        config_frame.pack(fill='x', pady=(0, 15))
        
        # Configuración en dos columnas
        config_inner = tk.Frame(config_frame, bg='#3b3b3b')
        config_inner.pack(fill='x', padx=10, pady=10)
        
        # Columna izquierda
        left_config = tk.Frame(config_inner, bg='#3b3b3b')
        left_config.pack(side='left', fill='x', expand=True)
        
        ttk.Label(left_config, text="🗣️ Voz:", background='#3b3b3b', foreground='white').pack(anchor='w')
        voz_combo = ttk.Combobox(left_config, textvariable=self.voz, values=[
            "es-MX-DaliaNeural",
            "es-ES-AlvaroNeural", 
            "es-ES-ElviraNeural",
            "es-AR-ElenaNeural",
            "es-CO-SalomeNeural"
        ], state="readonly", width=25)
        voz_combo.pack(anchor='w', pady=(5, 10))
        
        ttk.Label(left_config, text="⚡ Velocidad:", background='#3b3b3b', foreground='white').pack(anchor='w')
        velocidad_combo = ttk.Combobox(left_config, textvariable=self.velocidad, values=[
            "-30%", "-20%", "-10%", "+0%", "+10%", "+20%"
        ], state="readonly", width=10)
        velocidad_combo.pack(anchor='w', pady=(5, 0))
        
        # Columna derecha
        right_config = tk.Frame(config_inner, bg='#3b3b3b')
        right_config.pack(side='right', fill='x', expand=True, padx=(20, 0))
        
        ttk.Label(right_config, text="📁 Nombre del proyecto:", background='#3b3b3b', foreground='white').pack(anchor='w')
        tk.Entry(right_config, textvariable=self.nombre_proyecto, bg='#4b4b4b', fg='white', width=25).pack(anchor='w', pady=(5, 10))
        
        ttk.Label(right_config, text="🎵 Modo de generación:", background='#3b3b3b', foreground='white').pack(anchor='w')
        modo_frame = tk.Frame(right_config, bg='#3b3b3b')
        modo_frame.pack(anchor='w', pady=(5, 10))
        
        tk.Radiobutton(modo_frame, text="🎙️ Audio único", variable=self.modo_generacion, value="unico",
                      bg='#3b3b3b', fg='white', selectcolor='#4b4b4b', activebackground='#3b3b3b', activeforeground='white').pack(anchor='w')
        tk.Radiobutton(modo_frame, text="📂 Segmentos separados", variable=self.modo_generacion, value="segmentos",
                      bg='#3b3b3b', fg='white', selectcolor='#4b4b4b', activebackground='#3b3b3b', activeforeground='white').pack(anchor='w')
        
        ttk.Label(right_config, text="💾 Carpeta de salida:", background='#3b3b3b', foreground='white').pack(anchor='w')
        carpeta_frame = tk.Frame(right_config, bg='#3b3b3b')
        carpeta_frame.pack(anchor='w', pady=(5, 0))
        
        self.carpeta_label = tk.Label(carpeta_frame, text=self.carpeta_salida, bg='#4b4b4b', fg='white', width=20, relief='sunken')
        self.carpeta_label.pack(side='left')
        
        ttk.Button(carpeta_frame, text="📂", command=self.seleccionar_carpeta, width=3).pack(side='right', padx=(5, 0))
        
        # Frame de texto
        text_frame = tk.LabelFrame(main_frame, text="📝 Texto a convertir", bg='#3b3b3b', fg='white', font=('Arial', 11, 'bold'))
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Área de texto con scroll
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=80, height=15, 
                                                  bg='#4b4b4b', fg='white', font=('Arial', 11))
        self.text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones de acción
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Button(button_frame, text="📂 Cargar archivo TXT", command=self.cargar_archivo).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="📄 Ejemplo", command=self.cargar_texto_ejemplo).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Limpiar", command=self.limpiar_texto).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="📁 Abrir carpeta", command=self.abrir_carpeta).pack(side='left', padx=(0, 20))
        
        self.btn_generar = ttk.Button(button_frame, text="🎙️ GENERAR AUDIO MP3", command=self.iniciar_generacion)
        self.btn_generar.pack(side='right', padx=(10, 0))
        
        # Frame de progreso y status
        status_frame = tk.LabelFrame(main_frame, text="📊 Progreso", bg='#3b3b3b', fg='white', font=('Arial', 11, 'bold'))
        status_frame.pack(fill='x')
        
        status_inner = tk.Frame(status_frame, bg='#3b3b3b')
        status_inner.pack(fill='x', padx=10, pady=10)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(status_inner, mode='determinate')
        self.progress.pack(fill='x', pady=(0, 10))
        
        # Labels de información
        info_frame = tk.Frame(status_inner, bg='#3b3b3b')
        info_frame.pack(fill='x')
        
        self.status_label = tk.Label(info_frame, text="✅ Listo para generar", bg='#3b3b3b', fg='#4CAF50', font=('Arial', 10, 'bold'))
        self.status_label.pack(side='left')
        
        self.info_label = tk.Label(info_frame, text="", bg='#3b3b3b', fg='#cccccc', font=('Arial', 9))
        self.info_label.pack(side='right')
        
        # Vincular evento de cambio de texto
        self.text_area.bind('<KeyRelease>', self.actualizar_info)
    
    def cargar_texto_ejemplo(self):
        texto_ejemplo = """Este es un ejemplo de texto largo que será convertido a audio usando la voz Dalia Neural de México con configuraciones optimizadas para calidad de estudio. La velocidad está ajustada al 90% para mejor comprensión, similar a la configuración de ElevenLabs.

El sistema divide automáticamente el texto en segmentos manejables respetando párrafos y oraciones para mantener la fluidez natural del audio generado.

Esta configuración replica los ajustes de ElevenLabs:
- Stability 80% (voz consistente)
- Clarity 75% (balance naturalidad-claridad)  
- Speed 0.9x (velocidad ligeramente reducida)

El resultado será un audio de calidad profesional ideal para audiolibros, podcasts, narraciones y contenido educativo."""
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, texto_ejemplo)
        self.actualizar_info()
    
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, contenido)
                self.actualizar_info()
                
                # Sugerir nombre de proyecto basado en archivo
                nombre_base = os.path.splitext(os.path.basename(archivo))[0]
                self.nombre_proyecto.set(nombre_base)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if carpeta:
            self.carpeta_salida = carpeta
            self.carpeta_label.config(text=os.path.basename(carpeta))
    
    def abrir_carpeta(self):
        """Abre la carpeta de salida en el explorador"""
        if os.path.exists(self.carpeta_salida):
            os.startfile(self.carpeta_salida)
        else:
            messagebox.showinfo("Información", f"La carpeta '{self.carpeta_salida}' aún no existe.\nSe creará cuando generes el primer audio.")
    
    def limpiar_texto(self):
        self.text_area.delete(1.0, tk.END)
        self.actualizar_info()
    
    def actualizar_info(self, event=None):
        texto = self.text_area.get(1.0, tk.END).strip()
        caracteres = len(texto)
        palabras = len(texto.split()) if texto else 0
        tiempo_aprox = caracteres / 200 if self.velocidad.get() == "-10%" else caracteres / 180  # Ajustar según velocidad
        
        velocidad_texto = {
            "-30%": "70%", "-20%": "80%", "-10%": "90%", 
            "+0%": "100%", "+10%": "110%", "+20%": "120%"
        }.get(self.velocidad.get(), "100%")
        
        self.info_label.config(text=f"📊 {caracteres:,} caracteres | {palabras:,} palabras | ~{tiempo_aprox:.1f} min (vel: {velocidad_texto})")
    
    def dividir_texto(self, texto, max_chars=1000):
        """Divide el texto en segmentos manejables"""
        texto = texto.strip()
        parrafos = texto.split('\n\n')
        segmentos = []
        
        for parrafo in parrafos:
            if not parrafo.strip():
                continue
                
            if len(parrafo) > max_chars:
                oraciones = re.split(r'(?<=[.!?])\s+', parrafo)
                segmento_actual = ""
                
                for oracion in oraciones:
                    if len(segmento_actual + oracion) > max_chars and segmento_actual:
                        segmentos.append(segmento_actual.strip())
                        segmento_actual = oracion
                    else:
                        segmento_actual += " " + oracion if segmento_actual else oracion
                
                if segmento_actual:
                    segmentos.append(segmento_actual.strip())
            else:
                segmentos.append(parrafo.strip())
        
        return segmentos
    
    def crear_ssml(self, texto):
        """Crea SSML con configuración de ElevenLabs"""
        voz = self.voz.get()
        velocidad = self.velocidad.get()
        
        ssml = f'''
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
            <voice name="{voz}">
                <prosody rate="{velocidad}" pitch="+0%" volume="+5%">
                    {texto}
                </prosody>
            </voice>
        </speak>
        '''
        return ssml.strip()
    
    async def generar_audio_async(self):
        """Función asíncrona para generar el audio"""
        try:
            texto = self.text_area.get(1.0, tk.END).strip()
            if not texto:
                messagebox.showwarning("Advertencia", "Por favor ingresa algún texto para convertir.")
                return
            
            # Crear carpeta de salida
            if not os.path.exists(self.carpeta_salida):
                os.makedirs(self.carpeta_salida)
            
            nombre_proyecto = self.nombre_proyecto.get() or "audio"
            modo = self.modo_generacion.get()
            
            if modo == "unico":
                # Generar todo como un solo audio
                await self.generar_audio_unico(texto, nombre_proyecto)
            else:
                # Generar en segmentos separados
                await self.generar_audio_segmentos(texto, nombre_proyecto)
                
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {error_msg}", fg='#F44336'))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la generación:\n{error_msg}"))
        
        finally:
            # Restaurar botón
            self.generando = False
            self.root.after(0, lambda: self.btn_generar.config(text="🎙️ GENERAR AUDIO", state='normal'))
    
    async def generar_audio_unico(self, texto, nombre_proyecto):
        """Genera todo el texto como un solo archivo de audio"""
        self.root.after(0, lambda: self.progress.config(maximum=100))
        self.root.after(0, lambda: self.status_label.config(text="🎙️ Generando audio único...", fg='#FFC107'))
        
        try:
            # Generar todo el texto como un solo archivo sin SSML
            self.root.after(0, lambda: self.progress.config(value=30))
            self.root.after(0, lambda: self.status_label.config(text="🔄 Procesando texto completo..."))
            
            # Cambiar a MP3 y asegurar que la carpeta existe
            os.makedirs(self.carpeta_salida, exist_ok=True)
            archivo_salida = os.path.join(self.carpeta_salida, f"{nombre_proyecto}.mp3")
            
            # Verificar que no esté el archivo abierto en otro programa
            if os.path.exists(archivo_salida):
                try:
                    os.remove(archivo_salida)
                except PermissionError:
                    # Si no se puede eliminar, usar nombre alternativo
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    archivo_salida = os.path.join(self.carpeta_salida, f"{nombre_proyecto}_{timestamp}.mp3")
            
            self.root.after(0, lambda: self.progress.config(value=70))
            self.root.after(0, lambda: self.status_label.config(text="🎙️ Generando audio MP3..."))
            
            # Usar Edge-TTS con formato MP3
            communicate = edge_tts.Communicate(texto, self.voz.get(), rate=f"{self.velocidad.get()}")
            await communicate.save(archivo_salida)
            
            self.root.after(0, lambda: self.progress.config(value=100))
            self.root.after(0, lambda: self.status_label.config(text="✅ Audio MP3 completado", fg='#4CAF50'))
            
            # Mostrar mensaje de éxito
            duracion_aprox = len(texto) / 180  # ~180 caracteres por minuto
            archivo_nombre = os.path.basename(archivo_salida)
            self.root.after(0, lambda: messagebox.showinfo(
                "¡Audio generado!",
                f"✅ Audio MP3 generado exitosamente!\n\n📁 Archivo: {archivo_nombre}\n📂 Ubicación: {self.carpeta_salida}\n⏱️ Duración estimada: ~{duracion_aprox:.1f} minutos"
            ))
            
        except PermissionError as pe:
            error_msg = f"Error de permisos: {str(pe)}\n\nSoluciones:\n• Cierra el reproductor de audio si está abierto\n• Cambia la carpeta de salida\n• Ejecuta como administrador"
            self.root.after(0, lambda: self.status_label.config(text="❌ Error de permisos", fg='#F44336'))
            self.root.after(0, lambda: messagebox.showerror("Error de Permisos", error_msg))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_label.config(text=f"❌ Error: {error_msg}", fg='#F44336'))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la generación:\n{error_msg}"))
    
    async def generar_audio_segmentos(self, texto, nombre_proyecto):
        """Genera el audio en segmentos separados (funcionalidad original)"""
        # Dividir texto
        segmentos = self.dividir_texto(texto)
        total_segmentos = len(segmentos)
        
        # Actualizar UI
        self.root.after(0, lambda: self.progress.config(maximum=total_segmentos))
        self.root.after(0, lambda: self.status_label.config(text=f"🔄 Generando {total_segmentos} segmentos MP3...", fg='#FFC107'))
        
        exitosos = 0
        
        for i, segmento in enumerate(segmentos, 1):
            # Actualizar progreso
            self.root.after(0, lambda i=i: self.progress.config(value=i))
            self.root.after(0, lambda i=i, t=total_segmentos: self.status_label.config(
                text=f"🔄 Procesando segmento {i}/{t}..."
            ))
            
            try:
                archivo_salida = os.path.join(self.carpeta_salida, f"{nombre_proyecto}_parte_{i:03d}.mp3")
                
                # Usar Edge-TTS para generar MP3
                communicate = edge_tts.Communicate(segmento, self.voz.get(), rate=f"{self.velocidad.get()}")
                await communicate.save(archivo_salida)
                exitosos += 1
                
                await asyncio.sleep(0.3)  # Pausa pequeña
                
            except Exception as e:
                print(f"Error en segmento {i}: {e}")
        
        # Completado
        self.root.after(0, lambda: self.progress.config(value=total_segmentos))
        self.root.after(0, lambda: self.status_label.config(
            text=f"✅ Completado: {exitosos}/{total_segmentos} segmentos MP3", fg='#4CAF50'
        ))
        
        # Mostrar mensaje de éxito
        self.root.after(0, lambda: messagebox.showinfo(
            "¡Audio generado!",
            f"Se generaron {exitosos} archivos MP3 exitosamente.\n\nArchivos guardados en:\n{self.carpeta_salida}"
        ))
    
    def iniciar_generacion(self):
        """Inicia la generación en un hilo separado"""
        if self.generando:
            return
        
        self.generando = True
        self.btn_generar.config(text="⏳ Generando MP3...", state='disabled')
        
        # Ejecutar en hilo separado para no bloquear la UI
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.generar_audio_async())
        
        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.root.mainloop()

# Función principal
def main():
    app = InterfazGeneradorAudio()
    app.ejecutar()

if __name__ == "__main__":
    main()