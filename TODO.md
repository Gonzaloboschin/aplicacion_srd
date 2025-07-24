🎯 Funcionalidades Prioritarias

🔒 1. Panel de administrador

 Crear abrir_interfaz_admin(nombre_usuario)
 Visualizar eventos pendientes, aprobados, históricos
 Aprobar / rechazar eventos de operarios
 Exportación masiva a Excel / PDF
 Acceso a configuración de empresas y códigos

☁️ 2. Sincronización con base de datos

 Reemplazar almacenamiento local por base de datos (PostgreSQL / SQLite)
 Soporte offline con sincronización cuando hay conexión
 API para enviar y recibir datos desde tablet o escritorio

📱 3. Versión táctil / responsive

 Adaptar botones y formularios a pantallas táctiles (modo tablet)
 Aumentar tamaño de fuente y márgenes en campos de entrada

📊 4. Dashboard para clientes

 Construcción de tablero visual de control (tipo Power BI / Dash / Web)
 Acceso autenticado por empresa
 Visualización por zona, tipo de trampa, y estado

🧪 Mejoras técnicas

 Modularizar lógica de roles (role_router.py)
 Modo oscuro opcional
 Guardar logs de auditoría (acciones por usuario)
 Agregar validación de formato al campo “Número de estación”
 Unificar nombres: Operario, Usuario, User

✨ Interfaz y experiencia de usuario

 Transiciones suaves entre pantallas
 Barra superior con logo fijo y usuario visible
 Tooltips explicativos al pasar el mouse
 Feedback visual en botones (hover y activo)
 Mensajes de error consistentes (formato y estilo)