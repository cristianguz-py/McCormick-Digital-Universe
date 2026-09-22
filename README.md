# McCormick Digital Universe — V4

Aplicación web completa (no una simulación) construida con **Python + Django +
Django ORM + MySQL**, frontend con **HTML + CSS + JavaScript vanilla + Bootstrap
opcional**. Evoluciona la V3 (sitio estático) hacia una plataforma con sitio
público, autenticación real, dashboards privados por rol, sugerencias,
analítica, ingresos y contrataciones.

## 1. Qué es el proyecto

- **Público**: Home, Maco, C&MC, Melanie — contenido real, sin datos inventados.
- **Privado** (`/login`, `/dashboard/...`): autenticación real de Django,
  sesiones seguras, roles (`super_admin`, `artist`, `marketing`).
- **Apps Django**: `accounts` (usuarios/roles), `core` (público + actividad),
  `suggestions` (sugerencias + historial), `analytics` (eventos reales),
  `finance` (ingresos/contrataciones), `dashboard` (panel privado).

## 2. Arquitectura

```
mccormick/
├── manage.py
├── config/            settings, urls, wsgi, asgi
├── accounts/          User, roles, login/logout/perfil, seed
├── core/               páginas públicas, ActivityLog, errores 404/403/500
├── suggestions/        Suggestion, SuggestionComment, SuggestionHistory
├── analytics/          AnalyticsEvent, endpoint de tracking
├── finance/             Income, Contract
├── dashboard/           overview por rol, usuarios, actividad
├── templates/           base_public.html, base_dashboard.html + apps
├── static/               css/, js/, images/
├── media/                adjuntos de sugerencias
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Requisitos

- Python 3.11+
- MySQL 8+ y MySQL Workbench
- pip / virtualenv

## 4. Instalación paso a paso

### 4.1. Clonar y crear entorno virtual

```bash
cd mccormick
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> `mysqlclient` necesita las librerías de desarrollo de MySQL instaladas en el
> sistema (en Ubuntu/Debian: `sudo apt install default-libmysqlclient-dev
> build-essential pkg-config`; en macOS con Homebrew: `brew install mysql-client
> pkg-config` y exportar las variables que indique Homebrew).

### 4.2. Crear la base de datos en MySQL Workbench

1. Abre MySQL Workbench y conéctate a tu servidor local.
2. Ejecuta:
   ```sql
   CREATE DATABASE mccormick_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. (Opcional) crea un usuario dedicado:
   ```sql
   CREATE USER 'mccormick_user'@'localhost' IDENTIFIED BY 'una_clave_segura';
   GRANT ALL PRIVILEGES ON mccormick_db.* TO 'mccormick_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### 4.3. Configurar `.env`

```bash
cp .env.example .env
```

Edita `.env` con tus datos reales de MySQL y una `SECRET_KEY` propia
(puedes generarla con `python -c "import secrets; print(secrets.token_urlsafe(50))"`).

### 4.4. Migraciones

Django ORM gestiona el esquema — no crees tablas a mano en Workbench:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4.5. Seed (usuarios iniciales)

```bash
python manage.py seed
```

Crea `maco.admin`, `ian.admin`, `melanie.admin` y `cristian.admin` (super_admin)
con contraseñas de desarrollo (ver `accounts/management/commands/seed.py`) o las
que definas en `SEED_PASSWORD_*` dentro de `.env`. Cámbialas después desde
"Mi perfil" o el Django Admin.

### 4.6. (Opcional) Datos demo

```bash
python manage.py seed_demo
```

Crea registros de ejemplo **claramente marcados como `[DATOS DEMO]`** para
poder ver los dashboards con contenido. No lo ejecutes en producción, o
bórralos después desde el Django Admin.

### 4.7. Archivos estáticos e imágenes

Copia las imágenes reales de Maco dentro de `static/images/maco/` (los
nombres de archivo ya están referenciados en `templates/public/maco.html`:
`foto1.jpg`...`foto4.jpg`, `foto_de_maco.jpg`, `foto_de_maco_para_el_final.jpg`).

### 4.8. Ejecutar en local

```bash
python manage.py runserver
```

- Sitio público: http://127.0.0.1:8000/
- Login privado: http://127.0.0.1:8000/login/
- Django Admin: http://127.0.0.1:8000/admin/ (usa `cristian.admin`, que tiene
  `is_staff`/`is_superuser`, o crea un superusuario aparte con
  `python manage.py createsuperuser`)

## 5. Acceso al Django Admin

Cristian (`cristian.admin`) puede entrar directamente a `/admin/`. Desde ahí
se administran usuarios, sugerencias, ingresos, contrataciones y actividad
con la interfaz nativa de Django, sin necesidad de una UI adicional.

## 6. Cambiar contraseñas

- Cada usuario: "Mi perfil" → "Cambiar mi contraseña" dentro del dashboard.
- Administrativamente: desde `/admin/` → Usuarios → editar → "this form".

## 7. Analítica

`analytics.services.log_event` registra eventos reales desde el backend
(page_view, login, logout, sugerencia creada/actualizada). El frontend
(`static/js/analytics.js`) envía además `social_click`, `contact_click`,
`gallery_open` y `cta_click` al endpoint `POST /analytics/track/` protegido
con CSRF. Nunca se inventan cifras: si no hay eventos, el dashboard muestra
"Sin datos".

## 8. Administración

El sidebar del dashboard (`templates/base_dashboard.html`) muestra distintas
opciones según el rol del usuario autenticado. Las rutas privadas están
protegidas con `@login_required` y `@role_required(...)` en el backend — no
sólo ocultas visualmente.

## 9. Archivos estáticos y media en producción

```bash
python manage.py collectstatic
```

Sirve `staticfiles/` con tu servidor web (Nginx, Whitenoise, etc.) y asegúrate
de que `media/` sea persistente (no se borre en cada deploy) para conservar
los adjuntos de sugerencias.

## 10. Preparación para producción

En tu `.env` de producción:

```
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com
SECURE_SSL_REDIRECT=True
SECRET_KEY=<una clave distinta a la de desarrollo>
```

Con `DEBUG=False`, `settings.py` activa automáticamente `SESSION_COOKIE_SECURE`,
`CSRF_COOKIE_SECURE` y HSTS. Sirve la aplicación detrás de HTTPS (Nginx +
Let's Encrypt, o el proxy de tu proveedor de hosting) y con un proceso WSGI
(gunicorn/uwsgi) apuntando a `config.wsgi:application`.

Ejemplo mínimo con gunicorn:

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Pon Nginx (u otro proxy) delante para TLS y archivos estáticos/media.

## 11. Backups de MySQL

Respaldar:

```bash
mysqldump -u root -p mccormick_db > backup_mccormick_$(date +%Y%m%d).sql
```

Restaurar:

```bash
mysql -u root -p mccormick_db < backup_mccormick_20260101.sql
```

No se requiere infraestructura adicional: para uso real, automatiza este
`mysqldump` con un cron diario y guarda los `.sql` en un lugar seguro
(almacenamiento externo, no el mismo servidor únicamente).

## 12. Troubleshooting básico

| Problema | Causa probable | Solución |
|---|---|---|
| `django.db.utils.OperationalError` al migrar | MySQL no corre o credenciales incorrectas | Verifica que MySQL esté activo y revisa `.env` |
| `ModuleNotFoundError: No module named 'MySQLdb'` | Falta `mysqlclient` o sus dependencias de sistema | Instala las librerías de desarrollo de MySQL y reinstala `mysqlclient` |
| Login siempre "incorrecto" | Usuario no existe o `seed` no se ejecutó | `python manage.py seed` |
| Imágenes rotas en `/maco/` | Fotos no copiadas a `static/images/maco/` | Copia los archivos reales con esos nombres |
| Dashboard vacío en analítica | Aún no hay eventos reales | Es el comportamiento esperado — nunca se inventan datos |

## 13. Reglas del proyecto (resumen)

- No se inventan biografías, cifras, clientes ni estadísticas.
- No hay login falso ni contraseñas en JavaScript ni `localStorage` como
  sistema de autenticación.
- Arquitectura segura por encima de animaciones vistosas.
- Frontend tradicional: HTML + CSS + JS vanilla, sin React/Next/TypeScript.

---
Diseñado y desarrollado por **Cristian Guzmán**.
