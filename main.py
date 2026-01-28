import json
import os
from datetime import datetime

# File untuk menyimpan data tugas
DATA_FILE = "tugas.json"

def load_data():
    """Memuat data tugas dari file JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Menyimpan data tugas ke file JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_task(nama_tugas, deadline, nama_guru):
    """Menambahkan tugas baru"""
    data = load_data()
    task = {
        "id": len(data) + 1,
        "nama_tugas": nama_tugas,
        "deadline": deadline,
        "nama_guru": nama_guru,
        "status": "Belum Selesai",
        "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(task)
    save_data(data)
    print(f"\n✓ Tugas '{nama_tugas}' berhasil ditambahkan!")

def view_tasks():
    """Menampilkan semua tugas"""
    data = load_data()
    if not data:
        print("\n⚠ Tidak ada tugas. Silakan tambahkan tugas terlebih dahulu.")
        return
    
    print("\n" + "="*100)
    print("DAFTAR TUGAS")
    print("="*100)
    print(f"{'ID':<5} {'Nama Tugas':<30} {'Deadline':<15} {'Nama Guru':<20} {'Status':<15}")
    print("-"*100)
    
    for task in data:
        print(f"{task['id']:<5} {task['nama_tugas']:<30} {task['deadline']:<15} {task['nama_guru']:<20} {task['status']:<15}")
    
    print("="*100)

def mark_complete(task_id):
    """Menandai tugas sebagai selesai"""
    data = load_data()
    for task in data:
        if task["id"] == task_id:
            task["status"] = "Selesai"
            save_data(data)
            print(f"\n✓ Tugas '{task['nama_tugas']}' telah ditandai sebagai selesai!")
            return
    print("\n✗ Tugas tidak ditemukan!")

def delete_task(task_id):
    """Menghapus tugas"""
    data = load_data()
    for i, task in enumerate(data):
        if task["id"] == task_id:
            deleted_task = data.pop(i)
            # Perbarui ID
            for j, t in enumerate(data):
                t["id"] = j + 1
            save_data(data)
            print(f"\n✓ Tugas '{deleted_task['nama_tugas']}' berhasil dihapus!")
            return
    print("\n✗ Tugas tidak ditemukan!")

def edit_task(task_id, nama_tugas=None, deadline=None, nama_guru=None):
    """Mengedit tugas"""
    data = load_data()
    for task in data:
        if task["id"] == task_id:
            if nama_tugas:
                task["nama_tugas"] = nama_tugas
            if deadline:
                task["deadline"] = deadline
            if nama_guru:
                task["nama_guru"] = nama_guru
            save_data(data)
            print(f"\n✓ Tugas dengan ID {task_id} berhasil diperbarui!")
            return
    print("\n✗ Tugas tidak ditemukan!")

def search_by_guru(nama_guru):
    """Mencari tugas berdasarkan nama guru"""
    data = load_data()
    results = [task for task in data if nama_guru.lower() in task["nama_guru"].lower()]
    
    if not results:
        print(f"\n⚠ Tidak ada tugas dari guru '{nama_guru}'")
        return
    
    print(f"\n" + "="*100)
    print(f"TUGAS DARI GURU: {nama_guru}")
    print("="*100)
    print(f"{'ID':<5} {'Nama Tugas':<30} {'Deadline':<15} {'Nama Guru':<20} {'Status':<15}")
    print("-"*100)
    
    for task in results:
        print(f"{task['id']:<5} {task['nama_tugas']:<30} {task['deadline']:<15} {task['nama_guru']:<20} {task['status']:<15}")
    
    print("="*100)

def main_menu():
    """Menampilkan menu utama"""
    print("\n" + "="*80)
    print("╔═══════════════════════════════════════════════════════════════════════════╗")
    print("║               APLIKASI TO-DO LIST - MANAJEMEN TUGAS SEKOLAH              ║")
    print("╚═══════════════════════════════════════════════════════════════════════════╝")
    print("="*80)
    print("1. Tambah Tugas Baru")
    print("2. Lihat Semua Tugas")
    print("3. Tandai Tugas Selesai")
    print("4. Hapus Tugas")
    print("5. Edit Tugas")
    print("6. Cari Tugas berdasarkan Guru")
    print("7. Keluar")
    print("="*80)

def main():
    """Fungsi utama aplikasi"""
    while True:
        main_menu()
        pilihan = input("Pilih menu (1-7): ").strip()
        
        if pilihan == "1":
            print("\n--- TAMBAH TUGAS BARU ---")
            nama_tugas = input("Nama tugas: ").strip()
            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            nama_guru = input("Nama guru: ").strip()
            
            if nama_tugas and deadline and nama_guru:
                add_task(nama_tugas, deadline, nama_guru)
            else:
                print("\n✗ Semua field harus diisi!")
        
        elif pilihan == "2":
            view_tasks()
        
        elif pilihan == "3":
            view_tasks()
            task_id = input("\nMasukkan ID tugas yang selesai: ").strip()
            try:
                mark_complete(int(task_id))
            except ValueError:
                print("\n✗ ID harus berupa angka!")
        
        elif pilihan == "4":
            view_tasks()
            task_id = input("\nMasukkan ID tugas yang akan dihapus: ").strip()
            try:
                delete_task(int(task_id))
            except ValueError:
                print("\n✗ ID harus berupa angka!")
        
        elif pilihan == "5":
            view_tasks()
            task_id = input("\nMasukkan ID tugas yang akan diedit: ").strip()
            try:
                task_id = int(task_id)
                print("\n(Kosongkan jika tidak ingin mengubah)")
                nama_tugas = input("Nama tugas baru: ").strip() or None
                deadline = input("Deadline baru (YYYY-MM-DD): ").strip() or None
                nama_guru = input("Nama guru baru: ").strip() or None
                edit_task(task_id, nama_tugas, deadline, nama_guru)
            except ValueError:
                print("\n✗ ID harus berupa angka!")
        
        elif pilihan == "6":
            nama_guru = input("Masukkan nama guru: ").strip()
            if nama_guru:
                search_by_guru(nama_guru)
            else:
                print("\n✗ Nama guru tidak boleh kosong!")
        
        elif pilihan == "7":
            print("\n✓ Terima kasih telah menggunakan aplikasi To-Do List!")
            print("Sampai jumpa lagi!\n")
            break
        
        else:
            print("\n✗ Pilihan tidak valid! Silakan pilih menu 1-7.")
        
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()
