def get_precision(precision):
    precisions = {
        'Product Price': (16, 2),  # Ejemplo de precisión para precios de productos
        'Account': (16, 2),       # Ejemplo de precisión para cuentas contables
        # Agrega más precisiones según sea necesario
    }
    return precisions.get(precision, (16, 2))  # Valor predeterminado si no se encuentra la precisión