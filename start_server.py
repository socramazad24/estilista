#!/usr/bin/env python3
"""
Script para iniciar el servidor de desarrollo de Django
"""
import os
import sys
import subprocess

def main():
    os.chdir('/mnt/okcomputer/output/backend')
    
    print("=" * 60)
    print("INICIANDO SERVIDOR ESTILERA")
    print("=" * 60)
    print()
    print("Backend Django: http://localhost:8000")
    print("API Documentation: http://localhost:8000/api/")
    print("Admin Panel: http://localhost:8000/admin/")
    print()
    print("Credenciales de prueba:")
    print("  - Admin: admin / Admin123!")
    print("  - Estilista: maria.gomez / Estilista123!")
    print("  - Cajero: cajero1 / Cajero123!")
    print()
    print("=" * 60)
    print()
    
    # Start Django server
    subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()
