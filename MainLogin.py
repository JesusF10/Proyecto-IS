import flet as ft
import re
from flet import TextField, Checkbox, ElevatedButton, Text, Column, ControlEvent, Container, alignment
from database_utils import verificar_usuario, agregar_usuario
from admin_page import admin_panel
from main_app import show_main_app
        
def main(page: ft.Page):
    page.title = 'Librería Búho​'
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.AMBER,
        font_family="Roboto",
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_800,
        )
    )
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False
   
   
    def show_landing():
        page.clean()

        text_username = TextField(label='Usuario/Correo', width=200)
        text_password = TextField(label='Contraseña', width=200, password=True)
        message = Text("", color="red")

        def login(e: ControlEvent):
            if text_username.value and text_password.value:
                success, result, next_panel = verificar_usuario(text_username.value, text_password.value)
                if success:
                    page.clean()
                    if next_panel == "admin":
                        admin_panel(page, lambda: show_landing())
                    else:
                        show_main_app(page, result, go_back=lambda: show_landing())
                else:
                    message.value = result
                    page.update()
            else:
                message.value = "Por favor, complete todos los campos."
                page.update()

        content = Column(
            [
                Text("Librería Búho 🦉📚​​", size=30,weight="bold"),
                Text("¡Conecta todas las bibliotecas Unison!", size=15),
                text_username,
                text_password,
                ElevatedButton("Iniciar sesión", on_click=login),
                # ElevatedButton("Admin ⚙️", on_click=lambda e: admin_panel(page, lambda: show_landing())),
                ElevatedButton("¿No tienes cuenta? Regístrate", on_click=lambda e: show_signup()),
                message
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        page.add(Container(content=content, alignment=alignment.center, expand=True))

    def show_signup():
        page.clean()

        text_username = TextField(label='Usuario', width=200)
        text_email = TextField(label='Correo electronico', width=200)
        text_password = TextField(label='Contraseña', width=200, password=True)
        text_password_confirm = TextField(label='Confirmar contraseña', width=200, password=True)
        checkbox_agree = Checkbox(label='Acepto los términos', value=False)
        button_submit = ElevatedButton(text='Registrarse', width=200, disabled=True)
        message = Text("", color="red")

        def validate(e: ControlEvent):
            password_valid = text_password.value == text_password_confirm.value
            all_filled = all([
                  text_username.value,
                  text_email.value,
                  text_password.value, 
                  text_password_confirm.value, 
                  checkbox_agree.value
                  ])
            button_submit.disabled = not (all_filled and password_valid)
            message.value = "" if password_valid else "Las contraseñas no coinciden."    

            if not validate_email(text_email.value):
                message.value = "Correo inválido."
                button_submit.disabled = True
                page.update()
                return
            page.update()

        def submit(e: ControlEvent):
            if text_password.value != text_password_confirm.value:
                message.value = "Las contraseñas no coinciden."
                page.update()
                return
            
            success, msg = agregar_usuario(text_username.value,text_email.value, text_password.value)
            if success:
                page.clean()
                show_main_app(page, text_username.value, go_back=lambda: show_landing())
            else:
                message.value = msg
                page.update()

        def validate_email(email: str) -> bool:
            regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            return re.match(regex, email) is not None
        
        
        text_username.on_change = validate
        text_email.on_change = validate
        text_password.on_change = validate
        text_password_confirm.on_change = validate
        checkbox_agree.on_change = validate
        button_submit.on_click = submit

        content = Column([
            Text("Registrarse", size=24, weight="bold"),
            text_username,
            text_email,
            text_password,
            text_password_confirm,
            checkbox_agree,
            button_submit,
            ElevatedButton("Volver", on_click=lambda e: show_landing()),
            message
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        page.add(Container(content=content, alignment=alignment.center, expand=True))

    # Main app function
    # This function will be called after successful login
    
    show_landing()

if __name__ == "__main__":
    ft.app(target=main)
