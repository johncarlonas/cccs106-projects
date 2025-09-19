import flet as ft

import flet as ft
from db_connection import *

async def login_click(e):
    username = username_input.value.strip()
    password = password_input.value.strip()
    
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
                        content=ft.Text(f"Welcome, {username}!", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(success_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    failure_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.RED),
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
    
    invalid_input_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.BLUE),
                                ft.Text("Input Error")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text("Please enter username and password", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(invalid_input_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    database_error_dialog = ft.AlertDialog(
                        modal=True,
                        title= ft.Text("Database Error", text_align=ft.TextAlign.CENTER),
                        content=ft.Text("An error occured while connecting to the database", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda ev: e.page.close(database_error_dialog)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    
    if not username or not password:
        e.page.open(invalid_input_dialog)
        e.page.update()
        return
    
    try:
        connect = connect_db()
        if connect is None:
            e.page.open(database_error_dialog)
            e.page.update()
            return
        
        cursor = connect.cursor()
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        result = cursor.fetchone()

        cursor.close()
        connect.close()

        if result:
            e.page.open(success_dialog)
        else:
            e.page.open(failure_dialog)

        e.page.update()

    except Error:
        e.page.open(database_error_dialog)
        e.page.update()

def main(page: ft.Page): 
    global username_input, password_input
    
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
    
    username_input = ft.TextField(
                label="User name",
                hint_text="Enter your user name",
                helper_text="This is your unique identifier",
                width=300,
                autofocus=True,
                bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
            )
    
    username_field = ft.Row(
        [
            ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREY_800),
            username_input
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    password_input = ft.TextField(
                label="Password",
                hint_text="Enter your password",
                helper_text="This is your secret key",
                password=True,
                width=300,          
                can_reveal_password=True, 
                bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
            )
    
    password_field = ft.Row(
        [
            ft.Icon(ft.Icons.PASSWORD, color=ft.Colors.GREY_800),
            password_input
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
                            username_field,
                            password_field
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
