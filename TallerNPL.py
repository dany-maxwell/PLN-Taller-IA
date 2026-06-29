import customtkinter as ctk
import spacy
from nltk.stem import SnowballStemmer

stemmer_es = SnowballStemmer("spanish")

try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    # Por si acaso no se descargó el modelo correctamente
    nlp = None

# Configuración del tema y color de la aplicación
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue") # Opciones: "blue", "green", "dark-blue"

class NLPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Procesamiento de Lenguaje Natural (PLN) - Dashboard")
        self.geometry("700x550")
        self.resizable(False, False)

        # --- TÍTULO ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="Procesador de Texto NLP", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(padx=20, pady=(20, 10))

        # --- ENTRADA DE TEXTO (TextField / Entry) ---
        self.input_label = ctk.CTkLabel(self, text="Ingresa el texto a analizar:", font=ctk.CTkFont(size=14))
        self.input_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.text_input = ctk.CTkEntry(
            self, 
            placeholder_text="Escribe o pega tu texto aquí...", 
            width=620, 
            height=40
        )
        self.text_input.pack(padx=40, pady=(0, 15))

        # --- SECCIÓN DE BOTONES (ACCIONES) ---
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=40, pady=10)

        # Botón Tokenizar
        self.btn_tokenize = ctk.CTkButton(
            self.buttons_frame, 
            text="Tokenizar", 
            command=self.accion_tokenizar,
            width=135
        )
        self.btn_tokenize.pack(side="left", expand=True, padx=5)

        # Botón Normalización
        self.btn_normalize = ctk.CTkButton(
            self.buttons_frame, 
            text="Normalización", 
            command=self.accion_normalizar,
            width=135
        )
        self.btn_normalize.pack(side="left", expand=True, padx=5)

        # Botón Lematización
        self.btn_lemmatize = ctk.CTkButton(
            self.buttons_frame, 
            text="Lematización", 
            command=self.accion_lematizar,
            width=135
        )
        self.btn_lemmatize.pack(side="left", expand=True, padx=5)

        # Botón Stemming
        self.btn_lemmatize = ctk.CTkButton(
            self.buttons_frame, 
            text="Stemming", 
            command=self.accion_stemming,
            width=135
        )
        self.btn_lemmatize.pack(side="left", expand=True, padx=5)

        # --- SALIDA DE TEXTO (TextArea) ---
        self.output_label = ctk.CTkLabel(self, text="Resultado del procesamiento:", font=ctk.CTkFont(size=14))
        self.output_label.pack(anchor="w", padx=40, pady=(15, 5))

        self.text_output = ctk.CTkTextbox(
            self, 
            width=620, 
            height=200, 
            activate_scrollbars=True
        )
        self.text_output.pack(padx=40, pady=(0, 20))
        
        # Bloquear el TextArea de salida para que sea solo de lectura inicialmente
        self.text_output.configure(state="disabled")

    # --- FUNCIONES / MÉTODOS DE CONTROL ---
    # Por ahora solo muestran un feedback en el TextArea para verificar el diseño
    
    def mostrar_en_salida(self, mensaje):
        """Función auxiliar para escribir en el TextArea simulando la salida"""
        self.text_output.configure(state="normal") # Habilitar escritura
        self.text_output.delete("1.0", "end")      # Limpiar texto anterior
        self.text_output.insert("0.0", mensaje)    # Insertar nuevo texto
        self.text_output.configure(state="disabled") # Bloquear de nuevo

    def accion_tokenizar(self):
        texto = self.obtener_texto()
        if texto:
            doc = nlp(texto)
            # Extraemos cada palabra/token por separado
            tokens = [token.text for token in doc]
            
            resultado = f"📌 RECUENTO DE TOKENS: {len(tokens)}\n"
            resultado += "----------------------------------------\n"
            resultado += " , ".join(f"[{t}]" for t in tokens)
            self.mostrar_en_salida(resultado)

    def accion_normalizar(self):
        texto = self.obtener_texto()
        if texto:
            # 1. Diccionario de abreviaturas / acrónimos
            abreviaturas = {
                "ia": "inteligencia artificial",
                "pln": "procesamiento de lenguaje natural",
                "nlp": "natural language processing",
                "q": "que",
                "tqm": "te quiero mucho",
                "porfa": "por favor",
                "sr": "señor",
                "sra": "señora"
            }
            
            # 2. Procesamos el texto original con SpaCy
            doc = nlp(texto)
            
            tokens_normalizados = []
            for token in doc:
                # Ignoramos puntuación y espacios
                if not token.is_punct and not token.is_space:
                    palabra_minuscula = token.text.lower()
                    
                    # 3. Verificamos si la palabra es una abreviatura conocida
                    if palabra_minuscula in abreviaturas:
                        # Si existe, agregamos su significado expandido
                        tokens_normalizados.append(abreviaturas[palabra_minuscula])
                    else:
                        # Si no, dejamos la palabra normal en minúsculas
                        tokens_normalizados.append(palabra_minuscula)
            
            # 4. Construimos el resultado final
            resultado = "🧹 TEXTO NORMALIZADO (Con expansión de abreviaturas):\n"
            resultado += "------------------------------------------------------\n"
            resultado += " ".join(tokens_normalizados)
            self.mostrar_en_salida(resultado)

    def accion_lematizar(self):
        texto = self.obtener_texto()
        if texto:
            doc = nlp(texto)
            # Obtenemos el lema (raíz) de cada palabra
            lineas = []
            for token in doc:
                token.text.lower()
                if not token.is_punct and not token.is_space:
                    lineas.append(f"• {token.text} ➡️ {token.lemma_} ({token.pos_})")
            
            resultado = "🌱 LEMATIZACIÓN (Palabras reducidas a su raíz léxica):\n"
            resultado += "------------------------------------------------------\n"
            resultado += "\n".join(lineas)
            self.mostrar_en_salida(resultado)

    def accion_stemming(self):
        texto = self.obtener_texto()
        if texto:
            # Primero usamos SpaCy para separar el texto en palabras limpias
            doc = nlp(texto)
            
            lineas = []
            for token in doc:
                # Procesamos solo palabras, ignorando puntuación y espacios
                if not token.is_punct and not token.is_space:
                    palabra_original = token.text
                    
                    # Aplicamos el Stemming de NLTK
                    raiz_stem = stemmer_es.stem(palabra_original)
                    
                    lineas.append(f"• {palabra_original} ➡️ {raiz_stem}")
            
            resultado = "✂️ STEMMING (Recorte algorítmico de sufijos):\n"
            resultado += "------------------------------------------------------\n"
            resultado += "\n".join(lineas)
            self.mostrar_en_salida(resultado)

# --- INSTANCIA Y EJECUCIÓN ---
if __name__ == "__main__":
    app = NLPApp()
    app.mainloop()