import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
import webbrowser

SERVER_URL = "http://127.0.0.1:5000"  # Cambiar por IP si se usa otro dispositivo

class FormApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.nombre_input = TextInput(hint_text="Nombre", multiline=False)
        self.coord_input = TextInput(hint_text="Coordinación", multiline=False, input_filter='int')
        self.equi_input = TextInput(hint_text="Equilibrio", multiline=False, input_filter='int')
        self.aten_input = TextInput(hint_text="Atención", multiline=False, input_filter='int')

        layout.add_widget(self.nombre_input)
        layout.add_widget(self.coord_input)
        layout.add_widget(self.equi_input)
        layout.add_widget(self.aten_input)

        submit_btn = Button(text="Guardar y ver resultados")
        submit_btn.bind(on_press=self.guardar)
        layout.add_widget(submit_btn)

        self.mensaje = Label(text="")
        layout.add_widget(self.mensaje)

        return layout

    def guardar(self, instance):
        nombre = self.nombre_input.text.strip()
        try:
            coord = int(self.coord_input.text.strip())
        except:
            coord = 0
        try:
            equi = int(self.equi_input.text.strip())
        except:
            equi = 0
        try:
            aten = int(self.aten_input.text.strip())
        except:
            aten = 0

        if not nombre:
            self.mensaje.text = "⚠️ Debes ingresar un nombre"
            return

        data = {"nombre": nombre, "puntajes": {"coordinacion": coord, "equilibrio": equi, "atencion": aten}}

        try:
            r = requests.post(f"{SERVER_URL}/api/guardar_datos", json=data)
            if r.status_code == 200:
                self.mensaje.text = "✅ Guardado correctamente. Abriendo web..."
                # Abrir la web de resultados
                webbrowser.open(f"{SERVER_URL}/resultados_web")
                # Limpiar inputs
                self.nombre_input.text = ""
                self.coord_input.text = ""
                self.equi_input.text = ""
                self.aten_input.text = ""
            else:
                self.mensaje.text = f"Error: {r.json().get('error')}"
        except Exception as e:
            self.mensaje.text = f"Error de conexión: {e}"

if __name__ == "__main__":
    FormApp().run()
