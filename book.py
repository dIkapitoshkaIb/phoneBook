import sqlite3
import csv
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

# Создание подключения к базе данных
conn = sqlite3.connect('телефонный_справочник.db')
cursor = conn.cursor()

# Создание таблицы контактов
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   first_name TEXT,
                   last_name TEXT,
                   phone_number TEXT)''')

# Функция для добавления контакта
def add_contact(first_name, last_name, phone_number):
    # Проверка на повторение контакта
    cursor.execute("SELECT * FROM contacts WHERE first_name = ? AND last_name = ?",
                   (first_name, last_name))
    result = cursor.fetchall()
    if len(result) > 0:
        messagebox.showinfo("Ошибка", "Контакт уже существует!")
    else:
        cursor.execute("INSERT INTO contacts (first_name, last_name, phone_number) VALUES (?, ?, ?)",
                       (first_name, last_name, phone_number))
        conn.commit()
        messagebox.showinfo("Успех", "Контакт успешно добавлен!")
        refresh_contacts_list()

# Функция для удаления контакта
def delete_contact():
    selected_contact = listbox_contacts.get(listbox_contacts.curselection())
    contact_id = selected_contact.split(' ')[0]
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    messagebox.showinfo("Успех", "Контакт успешно удален!")
    refresh_contacts_list()

# Функция для сохранения контактов в файл bookphone.csv
def save_contacts_to_csv():
    cursor.execute("SELECT * FROM contacts")
    result = cursor.fetchall()
    with open('bookphone.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Имя', 'Фамилия', 'Номер телефона'])
        writer.writerows(result)
    messagebox.showinfo("Успех", "Контакты успешно сохранены в файле bookphone.csv")

# Функция для обновления списка контактов
def refresh_contacts_list():
    cursor.execute("SELECT * FROM contacts")
    result = cursor.fetchall()
    listbox_contacts.delete(0, END)
    for contact in result:
        listbox_contacts.insert(END, f"{contact[0]} {contact[1]} {contact[2]} {contact[3]}")

# Функция для создания графического интерфейса пользователя
def create_gui():
    global listbox_contacts  # Объявление переменной как глобальной
    root = Tk()
    root.title("Телефонный справочник")
    
    label_first_name = Label(root, text="Имя:")
    label_first_name.pack()
    entry_first_name = Entry(root)
    entry_first_name.pack()
    
    label_last_name = Label(root, text="Фамилия:")
    label_last_name.pack()
    entry_last_name = Entry(root)
    entry_last_name.pack()
    
    label_phone_number = Label(root, text="Номер телефона:")
    label_phone_number.pack()
    entry_phone_number = Entry(root)
    entry_phone_number.pack()
    
    button_add_contact = Button(root, text="Добавить контакт", command=lambda: add_contact(entry_first_name.get(), entry_last_name.get(), entry_phone_number.get()))
    button_add_contact.pack()
    
    button_save_to_csv = Button(root, text="Сохранить в CSV", command=save_contacts_to_csv)
    button_save_to_csv.pack()
    
    scrollbar_contacts = Scrollbar(root)
    scrollbar_contacts.pack(side="right", fill="y")
    
    listbox_contacts = Listbox(root, yscrollcommand=scrollbar_contacts.set)
    listbox_contacts.pack(fill="both", expand=True)
    
    scrollbar_contacts.config(command=listbox_contacts.yview)
    
    refresh_contacts_list()
    
    button_delete_contact = Button(root, text="Удалить контакт", command=delete_contact)
    button_delete_contact.pack()
    
    root.mainloop()

def on_closing(conn, root):
    conn.close()  # Закрытие соединения с базой данных
    root.destroy()  # Закрытие окна Tkinter
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Установка действия при закрытии окна


# Запуск графического интерфейса пользователя
create_gui()
