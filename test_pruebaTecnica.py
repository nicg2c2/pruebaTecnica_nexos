import pytest
from AppTecnica import app

# fixture es una función que puede ser utilizada por las pruebas para obtener recursos y configuraciones.
@pytest.fixture
def client(): # Método que crea un cliente de prueba
    app.config['TESTING'] = True # Configura la aplicación Flask para el modo de prueba
    with app.test_client() as client: # Crea un cliente de prueba
        yield client # Devuelve el cliente de prueba. El código después de yield (si lo hubiera) se ejecutará después de que la prueba haya terminado, lo que permite la limpieza si es necesario.

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200, f"El código de respuesta es {response.status_code}"
    assert "¡Bienvenido NEXOS!".encode('utf-8') in response.data, "¡Bienvenido NEXOS! no está presente en la respuesta"
    assert "La fecha y hora actuales son:".encode('utf-8') in response.data, "La fecha y hora actuales son: no está presente en la respuesta"
