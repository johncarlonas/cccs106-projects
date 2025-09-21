# main.py
import flet as ft
from database import *
from app_logic import *


def main(page: ft.Page):
    page.title = "Contacts"
    page.window.width = 400  
    page.window.height = 700  
    page.window.center()
    page.theme_mode = ft.ThemeMode.LIGHT 
    
    db_conn = init_db()

    search_state = [False]
    
    name_input = ft.TextField(label="Name", width=350)  
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)
    
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)
    
    search_field = ft.TextField(
        hint_text="Search contacts...",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        on_change=lambda e: filter_contacts(e.control.value, page, contacts_list_view, db_conn)
    )
    
    theme_icon = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Toggle Theme",
        on_click=lambda e: toggle_theme(page, theme_icon)
    )
    
    def handle_toggle_search(e):
        """Wrapper function to handle search toggle with state management."""
        search_state[0] = toggle_search(page, search_state[0], header_row, theme_icon, search_icon, search_field, contacts_list_view, db_conn)
    
    search_icon = ft.IconButton(
        icon=ft.Icons.SEARCH,
        tooltip="Search",
        on_click=handle_toggle_search
    )
    
    header_row = ft.Row([
        theme_icon,
        ft.Text(
            "Contacts",
            size=25,
            weight=ft.FontWeight.BOLD,
            expand=True,
            text_align=ft.TextAlign.CENTER
        ),
        search_icon,
    ])
    
    add_contact_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add Contact", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                name_input,
                phone_input,
                email_input,     
            ]),
            width=400,   
            height=200,  
        ),
        actions=[
            ft.TextButton(
                "Cancel", 
                on_click=lambda e: page.close(add_contact_modal)
            ),
            ft.TextButton(
                "Add Contact", 
                on_click=lambda e: add_contact_and_close(page, inputs, contacts_list_view, db_conn, add_contact_modal)
            )
        ],
    )
    
    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=10),
                        header_row,
                        ft.Divider(),  
                    ]),
                    padding=ft.Padding(10, 0, 10, 0),
                ),
                
                ft.Container(
                    content=contacts_list_view,
                    expand=True,
                    padding=ft.Padding(10, 0, 10, 0),
                ),
            ], 
            expand=True
        )
    )
    
    page.overlay.append(
        ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.Icons.PERSON_ADD_ALT_1, 
                tooltip="Add Contact",
                on_click=lambda e: page.open(add_contact_modal)
            ),
            right=20,
            bottom=20,
        )
    )
    
    display_contacts(page, contacts_list_view, db_conn)


if __name__ == "__main__":
    ft.app(target=main)