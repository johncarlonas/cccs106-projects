import flet as ft


def main(page: ft.Page): 
    page.bgcolor = ft.Colors.AMBER_ACCENT 
    page.window.title_bar_hidden = True 
    page.window.frameless = True 
    page.window.title = "User Login" 
    page.window.center() 
    page.window.height = 350 
    page.window.width = 400
    
    title = ft.Text(
        "User Login",
        size=20,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLACK,
        weight=ft.FontWeight.BOLD,
    )
    
    username_input = ft.Row(
        [
            ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_800),
            ft.TextField(
                label="User name",
                hint_text="Enter your user name",
                helper_text="This is your unique identifier",
                width=300,
                autofocus=True,
                bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    password_input = ft.Row(
        [
            ft.Icon(ft.Icons.PASSWORD, color=ft.Colors.GREY_800),
            ft.TextField(
                label="Password",
                hint_text="Enter your password",
                helper_text="This is your secret key",
                password=True,
                width=300,          
                can_reveal_password=True, 
                bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    login_button = ft.ElevatedButton(
                    "Login",
                    icon=ft.Icons.LOGIN,
                    icon_color=ft.Colors.BLUE_800,
                )
    
    page.add(
        ft.Column(
            [
                ft.Container(height=20),
                title,
                ft.Container( 
                    ft.Column(
                        [
                            username_input,
                            password_input
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ), 
                
                ft.Container(
                    ft.Row(
                        [
                            login_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    width=300
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            spacing=15,
        )
    )


ft.app(main)
