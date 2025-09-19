import flet as ft

import flet as ft
from db_connection import *

async def login_click(e):
    success_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                ft.Text("Login Successful")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text("Welcome, testuser!", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(success_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    failure_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                ft.Text("Login Failed")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text("Invalid username or password", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(failure_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    input_error_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                ft.Text("Input Error")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(input_error_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    database_error_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                ft.Text("Database Error")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text("An error occured while connecting to the database", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(database_error_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    e.page.open(success_dialog)
    e.page.update()


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
                    width=100,
                    on_click=login_click
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
                        spacing=20,
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
                    margin=ft.margin.only(top=0, right=20, bottom=40, left=0)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
        )
    )
    

ft.app(target=main)
