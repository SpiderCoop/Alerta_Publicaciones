# Alerta de publicaciones regulatorias

Este repositorio automatiza la revisión de publicaciones regulatorias y envía avisos por correo cuando encuentra contenido nuevo. La primera fuente activa es la página de [consultas públicas de Banco de México (Banxico)](https://www.banxico.org.mx/ConsultaRegulacionWeb/).

El objetivo es incorporar gradualmente otras fuentes públicas. El código ya contiene una implementación inicial para el Diario Oficial de la Federación (DOF), pero actualmente **no se ejecuta en el flujo principal**: `src/main.py` solo invoca el envío de consultas de Banxico.

## Qué hace hoy

En cada ejecución, el proceso:

1. Abre con Selenium la página de consultas de Banxico y obtiene las consultas vigentes, su fecha límite y los enlaces a sus documentos.
2. Consulta el registro local de envíos (`logs/log_deliveries.db`) para identificar consultas ya notificadas.
3. Descarga los documentos PDF de cada consulta nueva y los adjunta a un correo.
4. Registra el envío para evitar notificar de nuevo la misma consulta y elimina los archivos descargados después de enviar el correo.

La automatización se ejecuta en GitHub Actions de lunes a viernes, varias veces al día, según el horario configurado en `.github/workflows/deploy.yml`. También se puede iniciar manualmente desde la pestaña **Actions** de GitHub. El registro de envíos se guarda en el repositorio mediante un commit automático del flujo de despliegue; esto permite conservarlo entre ejecuciones.

## Estructura del proyecto

```text
src/
  main.py                         Punto de entrada: selecciona las fuentes que se ejecutan
  config.py                       Lee credenciales, destinatarios y rutas
  publicaciones/
    consulta_publica_banxico/      Extracción, integración y correo de Banxico
    dof/                           Implementación inicial del DOF (no activada)
  services/
    email_manager.py               Configura el servicio de correo
    download_service.py            Descarga documentos
    log_service.py                 Registra publicaciones enviadas en SQLite
    clean_text.py                  Normaliza texto para nombres e identificadores
tests/                              Pruebas automatizadas
.github/workflows/
  ci.yml                           Lint y pruebas en cambios al repositorio
  deploy.yml                       Ejecución programada y manual
```

## Requisitos

- Python 3.12 o posterior.
- [uv](https://docs.astral.sh/uv/) para administrar el entorno y las dependencias.
- Una cuenta de correo con permisos para enviar mensajes desde la automatización.

Las dependencias están definidas en `pyproject.toml` y fijadas en `uv.lock`. Selenium usa la configuración de navegador proporcionada por la dependencia `driver-configuration`.

## Preparar el entorno local

Desde la raíz del repositorio:

```powershell
uv sync --locked --only-group dev
```

Crea un archivo `.env` en la raíz para ejecutar localmente:

```dotenv
CUENTA=correo_emisor@example.com
PASSWORD=
RECIPIENTS_TO=destinatario1@example.com,destinatario2@example.com
RECIPIENTS_CC=
RECIPIENTS_BCC=
```

Completa `PASSWORD` con la credencial de la cuenta remitente antes de ejecutar. No agregues `.env` ni credenciales al control de versiones. `.env` está excluido por `.gitignore`.

Ejecuta el proceso y las pruebas con:

```powershell
uv run src/main.py
uv run pytest tests/ -v
```

Para verificar estilo y formato de Python:

```powershell
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
```

## Configuración en GitHub Actions

El flujo de despliegue lee estas variables de **GitHub Secrets** (Settings → Secrets and variables → Actions):

| Secret | Uso |
| --- | --- |
| `CUENTA_CORREO` | Cuenta remitente |
| `PASSWORD_CUENTA` | Credencial de la cuenta remitente |
| `RECIPIENTS_TO` | Destinatarios principales (director adjunta de juridico), separados por comas |
| `RECIPIENTS_CC` | Destinatarios en copia (director adjunto tecnico), separados por comas |
| `RECIPIENTS_BCC` | Destinatarios en copia oculta (responsable), separados por comas |

El workflow los asigna a las variables `CUENTA`, `PASSWORD`, `RECIPIENTS_TO`, `RECIPIENTS_CC` y `RECIPIENTS_BCC` que utiliza `src/config.py`. Si cambias la configuración, actualiza tanto el workflow como este documento.

## Agregar una fuente de publicaciones

Cada fuente debe encargarse de obtener sus publicaciones y convertirlas a un formato que su proceso de envío pueda manejar. Mantén las particularidades de extracción y del correo dentro de su propio paquete bajo `src/publicaciones/`; reutiliza los servicios comunes cuando corresponda.

Pasos recomendados:

1. **Crea un paquete para la fuente** dentro de `src/publicaciones/`, por ejemplo `src/publicaciones/nueva_fuente/`.
2. **Implementa la extracción** en un módulo como `fuente_extractor.py`. Devuelve registros consistentes con los datos que la fuente necesita enviar, por ejemplo título, fecha, enlace y documentos adjuntos.
3. **Implementa el proceso de integración** en un módulo propio. Sigue el patrón de `consulta_publica_banxico.py`: consultar publicaciones, omitir las ya registradas, preparar y enviar el correo, y registrar solo los envíos exitosos.
4. **Prepara el correo** en un módulo específico si el asunto o el contenido varían por fuente.
5. **Conecta la fuente en `src/main.py`** llamando a su función de envío. Una fuente que no se invoque desde el punto de entrada no se ejecutará en la automatización.
6. **Añade pruebas** en una ruta equivalente bajo `tests/publicaciones/`. Usa mocks para Selenium, descargas, correo y registro; las pruebas no deberían enviar correos reales ni depender de que el sitio externo esté disponible.
7. **Revisa la deduplicación**. `LogService` identifica publicaciones por el texto de `publication_name`, compartido por todas las fuentes. Usa un identificador estable que incluya la fuente (por ejemplo, `nueva_fuente:<id>`) para evitar colisiones entre publicaciones con nombres iguales.
8. **Actualiza este README** si cambian las fuentes activas, la configuración, el horario o los pasos para ejecutar el proyecto.

Los servicios existentes en `src/services/` incluyen el envío de correo, la descarga de archivos, la limpieza de texto y el registro SQLite. No es necesario duplicarlos si sirven para la nueva fuente.

### Situación del DOF

Los módulos de extracción y envío del DOF están en `src/publicaciones/dof/`, pero la llamada a `enviar_publicaciones_dof()` está comentada en `src/main.py`. Antes de activarla, revisa y prueba los criterios de relevancia, los identificadores de deduplicación y el contenido de los correos para esa fuente.

## Contribuciones

Los cambios se validan en GitHub Actions: el flujo de CI ejecuta Ruff y las pruebas de `tests/` en cambios dirigidos a las ramas `main` y `develop`. Para contribuir, crea una rama, realiza el cambio, ejecuta las validaciones localmente y abre un pull request.
