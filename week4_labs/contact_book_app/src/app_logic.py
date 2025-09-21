# app_logic.py
import flet as ft
from database import *


def create_contact_card(contact, page, db_conn, contacts_list_view):
    """Creates a contact card for better styling."""
    contact_id, name, phone, email = contact
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Icon(
                    name=ft.Icons.PERSON,
                    size=50,
                ),
                
                ft.Column([
                    ft.Text(
                        name, 
                        size=16, 
                        weight=ft.FontWeight.BOLD,
                    ),
                    
                    ft.Row([
                        ft.Icon(
                            name=ft.Icons.PHONE, 
                            size=15 
                        ),
                        ft.Text(
                            phone, 
                            size=15
                        ),
                    ], spacing=5),
                    
                    ft.Row([
                        ft.Icon(
                            name=ft.Icons.EMAIL, 
                            size=15, 
                        ),
                        ft.Text(
                            email, 
                            size=15,
                        ),
                    ], spacing=5),
                ], 
                spacing=8,
                expand=True
                ),
                
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    icon_size=20,
                    items=[
                        ft.PopupMenuItem(
                            text="Edit",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _, c=contact: open_edit_dialog(
                                page, c, db_conn, contacts_list_view
                            )
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            text="Delete",
                            icon=ft.Icons.DELETE,
                            on_click=lambda _, cid=contact_id: delete_contact(
                                page, cid, db_conn, contacts_list_view
                            )
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
            ),
            padding=ft.Padding(15, 10, 15, 10),
        ),
        elevation=2,
        margin=ft.Margin(0, 0, 0, 5),
    )


def add_contact_and_close(page, inputs, contacts_list_view, db_conn, modal):
    """Validates inputs, adds a new contact to the database, and displays success dialog."""
    name_input, phone_input, email_input = inputs

    if not name_input.value.strip() or not phone_input.value.strip():
        for field in inputs:
            field.value = ""
        page.update()
        input_error(page)
        return
    
    add_contact(page, inputs, contacts_list_view, db_conn)
    
    page.close(modal)
    
    success_modal = ft.AlertDialog(
                        modal=True,
                        title= ft.Column(
                            [
                                ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                ft.Text("Contact Added")
                                
                            ],             
                            alignment=ft.MainAxisAlignment.CENTER,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                        ),
                        content=ft.Text(f"Contact has been added successfully!", text_align=ft.TextAlign.CENTER),
                        actions=[
                            ft.TextButton("OK", on_click=lambda e: page.close(success_modal)),
                        ],
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
    page.open(success_modal)


def display_contacts(page, contacts_list_view, db_conn):
    """Fetches all contacts from the database and displays them as modern cards in the ListView."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn)
    
    for contact in contacts:
        contact_card = create_contact_card(contact, page, db_conn, contacts_list_view)
        contacts_list_view.controls.append(contact_card)
    
    page.update()


def add_contact(page, inputs, contacts_list_view, db_conn):
    """Adds a new contact to the database, clears input fields, and refreshes the contact list."""
    name_input, phone_input, email_input = inputs
    add_contact_db(db_conn, name_input.value, phone_input.value, email_input.value)
    
    for field in inputs:
        field.value = ""
    
    display_contacts(page, contacts_list_view, db_conn)
    page.update()


def delete_contact(page, contact_id, db_conn, contacts_list_view):
    """Initiates the contact deletion process by showing a confirmation modal dialog."""
    delete_contact_modal(page, contact_id, db_conn, contacts_list_view)


def delete_contact_modal(page, contact_id, db_conn, contacts_list_view):
    """Creates and displays a confirmation dialog for deleting a contact with success feedback."""
    
    def confirm_delete(e):
        """Handles the actual deletion after user confirms the action."""
        page.close(confirmation_dialog)
        
        delete_contact_db(db_conn, contact_id)
        display_contacts(page, contacts_list_view, db_conn)
        
        success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Column(
                [
                    ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                    ft.Text("Contact Deleted!")
                ],             
                alignment=ft.MainAxisAlignment.CENTER,  
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            ),
            content=ft.Text("Contact has been deleted successfully!", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=lambda ev: page.close(success_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(success_dialog)
        page.update()
    
    def cancel_delete(e):
        """Cancels the deletion process and closes the confirmation dialog."""
        page.close(confirmation_dialog)
    
    
    confirmation_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Column(
            [
                ft.Icon(name=ft.Icons.DELETE, color=ft.Colors.RED),
                ft.Text("Confirm Delete")
            ],             
            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
        ),
        content=ft.Text("Are you sure you want to delete this contact?", text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton("Cancel", on_click=cancel_delete),
            ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.open(confirmation_dialog)


def input_error(page):
    """Displays an input error modal dialog when required fields are missing."""
    invalid_input_modal = ft.AlertDialog(
                            modal=True,
                            title= ft.Column(
                                [
                                    ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.BLUE),
                                    ft.Text("Input Error")
                                    
                                ],             
                                alignment=ft.MainAxisAlignment.CENTER,  
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                            ),
                            content=ft.Text("Please input Name and Phone Number", text_align=ft.TextAlign.CENTER),
                            actions=[
                                ft.TextButton("OK", on_click=lambda e: page.close(invalid_input_modal)),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
    page.open(invalid_input_modal)


def open_edit_dialog(page, contact, db_conn, contacts_list_view):
    """Creates and displays an edit dialog for modifying contact details with validation."""
    contact_id, name, phone, email = contact
    
    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)

    def save_and_close(e):
        """Validates input fields, updates the contact, and shows success dialog."""
        if not edit_name.value.strip() or not edit_phone.value.strip():
            edit_name.value = ""
            edit_phone.value = ""
            edit_email.value = ""
            page.update()
            input_error(page)
            return
        
        update_contact_db(
            db_conn, contact_id, edit_name.value, edit_phone.value, edit_email.value
        )
        
        page.close(edit_dialog)
        
        edit_success_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Column(
                [
                    ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                    ft.Text("Contact Updated!")
                ],             
                alignment=ft.MainAxisAlignment.CENTER,  
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            ),
            content=ft.Text("Contact has been updated successfully!", text_align=ft.TextAlign.CENTER),
            actions=[
                ft.TextButton("OK", on_click=lambda ev: page.close(edit_success_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(edit_success_dialog)
        
        display_contacts(page, contacts_list_view, db_conn)
        page.update()

    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.Column([
                edit_name,
                edit_phone,
                edit_email     
            ]),
            width=400,   
            height=200,   
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(edit_dialog, 'open', False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )
    
    page.open(edit_dialog)


def filter_contacts(query, page, contacts_list_view, db_conn):
    """Filters contacts based on search query and displays matching results."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn)
    
    for contact in contacts:
        contact_id, name, phone, email = contact
        if query.lower() in name.lower() or query.lower() in phone.lower() or query.lower() in email.lower():
            contact_card = create_contact_card(contact, page, db_conn, contacts_list_view)
            contacts_list_view.controls.append(contact_card)
    page.update()


def toggle_theme(page, theme_icon):
    """Toggles between light and dark theme mode."""
    page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    theme_icon.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE
    page.update()


def toggle_search(page, search_mode, header_row, theme_icon, search_icon, search_field, contacts_list_view, db_conn):
    """Toggles search mode on/off and updates the header layout."""
    search_mode = not search_mode
    
    if search_mode:
        header_row.controls.clear()
        header_row.controls.extend([
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: exit_search_mode(page, header_row, theme_icon, search_icon, search_field, contacts_list_view, db_conn)
            ),
            search_field,
        ])
        page.update()  
        search_field.focus()  
    else:
        exit_search_mode(page, header_row, theme_icon, search_icon, search_field, contacts_list_view, db_conn)
    
    page.update()
    return search_mode


def exit_search_mode(page, header_row, theme_icon, search_icon, search_field, contacts_list_view, db_conn):
    """Exits search mode and restores the normal header layout."""
    header_row.controls.clear()
    header_row.controls.extend([
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
    search_field.value = ""
    display_contacts(page, contacts_list_view, db_conn)
    page.update()