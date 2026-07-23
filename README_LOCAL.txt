INSTRUCCIONES RAPIDAS

1) Activar entorno virtual (opcional si ya lo tienes)
2) Ejecutar:
   python manage.py migrate
   python manage.py runserver

3) Registrar psicologos desde RH:
   /portal/rh/doctores/nuevo/

IMPORTANTE:
- El login usa correo como username.
- Para doctores creados en RH, el sistema guarda username=email automaticamente.
- Para crear el administrador inicial de forma segura:
   $env:ADMIN_USERNAME="admin"
   $env:ADMIN_EMAIL="admin@cap.com"
   $env:ADMIN_PASSWORD="tu-contraseña-segura"
   python manage.py crear_admin

   En Render configura esas tres variables y ejecuta el mismo comando desde
   el Shell del servicio. No pongas la contraseña en el repositorio.
