import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': os.getenv('MYSQL_HOST'),
            'port': int(os.getenv('MYSQL_PORT')),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'autocommit': True
        }
    
    def get_connection(self):
        try:
            return mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Error de conexión a MySQL: {err}")
            return None
    
    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error ejecutando query: {err}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def execute_insert(self, query, params=None):
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error en insert: {err}")
            return None
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Métodos específicos para el proyecto
    def registrar_cliente(self, nombre, telefono=None):
        """Registra un cliente o lo actualiza si ya existe"""
        if telefono:
            # Verificar si ya existe por teléfono
            query = "SELECT id FROM clientes WHERE telefono = %s"
            result = self.execute_query(query, (telefono,))
            if result:
                # Cliente ya existe, actualizar nombre si es diferente
                query = "UPDATE clientes SET nombre = %s WHERE telefono = %s"
                self.execute_query(query, (nombre, telefono))
                return result[0]['id']
        
        # Verificar si existe por nombre
        query = "SELECT id FROM clientes WHERE nombre = %s"
        result = self.execute_query(query, (nombre,))
        if result:
            return result[0]['id']
        
        # Crear nuevo cliente
        query = "INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)"
        return self.execute_insert(query, (nombre, telefono))
    
    def crear_pedido(self, cliente_id, productos, cantidades, telefono_cliente=None):
        """Crea un pedido con múltiples productos"""
        # Crear el pedido principal
        query = "INSERT INTO pedidos (cliente_id) VALUES (%s)"
        pedido_id = self.execute_insert(query, (cliente_id,))
        
        if not pedido_id:
            return None
        
        total = 0
        # Agregar productos al pedido
        for i, producto in enumerate(productos):
            cantidad = cantidades[i] if i < len(cantidades) else 1
            
            # Buscar si el producto existe en la tabla productos
            query_producto = "SELECT id, precio FROM productos WHERE nombre LIKE %s"
            resultado_producto = self.execute_query(query_producto, (f"%{producto}%",))
            
            if resultado_producto:
                # Producto existe en la tabla
                producto_id = resultado_producto[0]['id']
                precio_unitario = resultado_producto[0]['precio']
            else:
                # Producto no existe, crearlo con precio 0 (se puede actualizar después)
                query_crear_producto = "INSERT INTO productos (nombre, precio, descripcion) VALUES (%s, %s, %s)"
                producto_id = self.execute_insert(query_crear_producto, (producto, 0.0, f"Producto agregado automáticamente: {producto}"))
                precio_unitario = 0.0
            
            subtotal = precio_unitario * cantidad
            total += subtotal
            
            # Insertar detalle del pedido
            query_detalle = """
                INSERT INTO pedido_detalle (pedido_id, producto_id, cantidad, precio_unitario) 
                VALUES (%s, %s, %s, %s)
            """
            self.execute_insert(query_detalle, (pedido_id, producto_id, cantidad, precio_unitario))
        
        # Actualizar total del pedido
        query_total = "UPDATE pedidos SET total = %s WHERE id = %s"
        self.execute_query(query_total, (total, pedido_id))
        
        return pedido_id
    
    def consultar_pedidos_cliente(self, telefono):
        """Consulta los pedidos de un cliente por teléfono"""
        query = """
            SELECT p.id, p.fecha, p.estado, p.total,
                   GROUP_CONCAT(CONCAT(pd.cantidad, 'x ', pr.nombre) SEPARATOR ', ') as productos
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN pedido_detalle pd ON p.id = pd.pedido_id
            LEFT JOIN productos pr ON pd.producto_id = pr.id
            WHERE c.telefono = %s
            GROUP BY p.id, p.fecha, p.estado, p.total
            ORDER BY p.fecha DESC
            LIMIT 5
        """
        return self.execute_query(query, (telefono,))
    
    def log_conversacion(self, cliente_id, mensaje_usuario, intent_detectado, respuesta_enviada):
        """Guarda log de la conversación"""
        query = """
            INSERT INTO chat_logs (cliente_id, user_message, intent_detected, response_sent) 
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_insert(query, (cliente_id, mensaje_usuario, intent_detectado, respuesta_enviada))

# Función de conveniencia para compatibilidad con scripts existentes
def get_db_connection():
    """Función de conveniencia para obtener conexión a la base de datos"""
    db_manager = DatabaseManager()
    return db_manager.get_connection()

# Crear instancia global para fácil acceso
db = DatabaseManager()
