# # main.py
# from fastapi import FastAPI, HTTPException, Query
# from typing import List
# from pydantic import BaseModel
# from passlib.context import CryptContext
# import jwt
# import logging

# # Configuración de logging para rastrear operaciones
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Base de datos simulada en memoria
# fake_db = {"users": {}}

# # Configuración de JWT
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"

# # Contexto para cifrado de contraseñas
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Modelos de entrada
# class Payload(BaseModel):
#     numbers: List[int]
#     """Lista de números enteros para procesar."""

# class BinarySearchPayload(BaseModel):
#     numbers: List[int]
#     """Lista de números enteros ordenados para búsqueda."""
#     target: int
#     """Número objetivo a buscar en la lista."""

# class Credentials(BaseModel):
#     username: str
#     """Nombre de usuario para registro o login."""
#     password: str
#     """Contraseña del usuario."""

# # Modelos de respuesta
# class BubbleSortResponse(BaseModel):
#     numbers: List[int]
#     """Lista de números ordenada."""

# class EvenNumbersResponse(BaseModel):
#     even_numbers: List[int]
#     """Lista de números pares filtrados."""
#     total: int
#     """Cantidad total de números pares encontrados."""
#     page: int
#     """Página actual de los resultados."""
#     page_size: int
#     """Cantidad de elementos por página."""

# class SumResponse(BaseModel):
#     sum: int
#     """Suma de los números en la lista."""

# class MaxResponse(BaseModel):
#     max: int
#     """Valor máximo en la lista."""

# class BinarySearchResponse(BaseModel):
#     found: bool
#     """Indica si el número objetivo fue encontrado."""
#     index: int
#     """Índice del número encontrado o -1 si no está."""

# class QuickSortResponse(BaseModel):
#     numbers: List[int]
#     """Lista de números ordenada con Quick Sort."""

# # Funciones de autenticación
# def create_access_token(data: dict) -> str:
#     """
#     Genera un token JWT a partir de los datos proporcionados.

#     Args:
#         data (dict): Diccionario con los datos a codificar (ej. {"sub": "username"}).

#     Returns:
#         str: Token JWT codificado con el algoritmo HS256.

#     Example:
#         >>> create_access_token({"sub": "user1"})
#         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
#     """
#     to_encode = data.copy()
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_password_hash(password: str) -> str:
#     """
#     Cifra una contraseña usando el esquema bcrypt.

#     Args:
#         password (str): Contraseña en texto plano.

#     Returns:
#         str: Hash de la contraseña cifrada.
#     """
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verifica si una contraseña en texto plano coincide con su hash.

#     Args:
#         plain_password (str): Contraseña en texto plano ingresada por el usuario.
#         hashed_password (str): Hash almacenado de la contraseña.

#     Returns:
#         bool: True si la contraseña es válida, False si no.
#     """
#     logger.debug(f"Verificando contraseña para hash: {hashed_password}")
#     return pwd_context.verify(plain_password, hashed_password)

# def get_current_user(token: str) -> None:
#     """
#     Verifica un token JWT y valida la autenticación del usuario.

#     Args:
#         token (str): Token JWT pasado como query parameter.

#     Raises:
#         HTTPException: 401 si el token es inválido o el usuario no existe.
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None or username not in fake_db["users"]:
#             raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#         logger.info(f"Usuario autenticado: {username}")
#     except Exception as e:
#         logger.error(f"Error al verificar token: {str(e)}")
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# # Aplicación FastAPI
# app = FastAPI(
#     title="API de Algoritmos con Autenticación",
#     description="Una API que implementa algoritmos básicos como Bubble Sort, Quick Sort, y búsqueda binaria, con autenticación basada en JWT.",
#     version="1.0.0",
#     docs_url="/docs",
#     openapi_url="/openapi.json"
# )

# # Endpoints
# @app.post("/register")
# def register(payload: Credentials):
#     """
#     Registra un nuevo usuario con una contraseña cifrada.

#     Args:
#         payload (Credentials): Objeto con 'username' y 'password'.

#     Returns:
#         dict: Mensaje de éxito {"message": "User registered successfully"}.

#     Raises:
#         HTTPException: 400 si el usuario ya existe.

#     Example:
#         Request: POST /register {"username": "user1", "password": "pass1"}
#         Response: {"message": "User registered successfully"}
#     """
#     username = payload.username
#     password = payload.password
#     if username in fake_db["users"]:
#         logger.warning(f"Intento de registro de usuario existente: {username}")
#         raise HTTPException(status_code=400, detail="User already exists")
#     hashed_password = get_password_hash(password)
#     fake_db["users"][username] = {"password": hashed_password}
#     logger.info(f"Usuario registrado: {username}")
#     return {"message": "User registered successfully"}

# @app.post("/login")
# def login(payload: Credentials):
#     """
#     Inicia sesión y devuelve un token JWT para autenticación.

#     Args:
#         payload (Credentials): Objeto con 'username' y 'password'.

#     Returns:
#         dict: Diccionario con el token {"access_token": "<token>"}.

#     Raises:
#         HTTPException: 401 si las credenciales son inválidas.

#     Example:
#         Request: POST /login {"username": "user1", "password": "pass1"}
#         Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
#     """
#     username = payload.username
#     password = payload.password
#     if username not in fake_db["users"]:
#         logger.warning(f"Intento de login con usuario no existente: {username}")
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     user = fake_db["users"][username]
#     if not verify_password(password, user["password"]):
#         logger.warning(f"Contraseña incorrecta para usuario: {username}")
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": username})
#     logger.info(f"Login exitoso para usuario: {username}")
#     return {"access_token": access_token}

# @app.post("/bubble-sort", response_model=BubbleSortResponse)
# def bubble_sort(payload: Payload, token: str):
#     """
#     Ordena una lista de números usando el algoritmo Bubble Sort optimizado.

#     Args:
#         payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
#         token (str): Token JWT para autenticación, pasado como query parameter.

#     Returns:
#         BubbleSortResponse: Diccionario con la clave 'numbers' y la lista ordenada.

#     Raises:
#         HTTPException: 400 si la lista está vacía.
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /bubble-sort?token=<token> {"numbers": [3, 2, 1]}
#         Response: {"numbers": [1, 2, 3]}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     if not numbers:
#         logger.error("Lista vacía recibida en /bubble-sort")
#         raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
#     logger.info(f"Ordenando lista con Bubble Sort: {numbers}")
#     n = len(numbers)
#     for i in range(n):
#         swapped = False
#         for j in range(0, n - i - 1):
#             if numbers[j] > numbers[j + 1]:
#                 numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
#                 swapped = True
#         if not swapped:
#             break
#     logger.info(f"Lista ordenada: {numbers}")
#     return {"numbers": numbers}

# @app.post("/filter-even", response_model=EvenNumbersResponse)
# def filter_even(
#     payload: Payload,
#     token: str,
#     page: int = Query(1, ge=1, description="Número de página (mínimo 1)"),
#     page_size: int = Query(10, ge=1, le=100, description="Elementos por página (1-100)")
# ):
#     """
#     Filtra números pares de una lista con soporte para paginación.

#     Args:
#         payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
#         token (str): Token JWT para autenticación, pasado como query parameter.
#         page (int): Número de página a devolver (default: 1).
#         page_size (int): Cantidad de elementos por página (default: 10, máximo 100).

#     Returns:
#         EvenNumbersResponse: Números pares paginados, total, página actual y tamaño.

#     Raises:
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /filter-even?token=<token>&page=1&page_size=2 {"numbers": [1, 2, 3, 4, 5, 6]}
#         Response: {"even_numbers": [2, 4], "total": 3, "page": 1, "page_size": 2}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     logger.info(f"Filtrando números pares de: {numbers}")
#     even_numbers = [number for number in numbers if number % 2 == 0]
#     total = len(even_numbers)
#     start = (page - 1) * page_size
#     end = start + page_size
#     paginated_numbers = even_numbers[start:end]
#     logger.info(f"Números pares filtrados: {paginated_numbers}")
#     return {
#         "even_numbers": paginated_numbers,
#         "total": total,
#         "page": page,
#         "page_size": page_size
#     }

# @app.post("/sum-elements", response_model=SumResponse)
# def sum_elements(payload: Payload, token: str):
#     """
#     Calcula la suma de los elementos de una lista de números.

#     Args:
#         payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
#         token (str): Token JWT para autenticación, pasado como query parameter.

#     Returns:
#         SumResponse: Diccionario con la clave 'sum' y el valor de la suma.

#     Raises:
#         HTTPException: 400 si la lista está vacía.
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /sum-elements?token=<token> {"numbers": [1, 2, 3]}
#         Response: {"sum": 6}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     if not numbers:
#         logger.error("Lista vacía recibida en /sum-elements")
#         raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
#     result = sum(numbers)
#     logger.info(f"Suma de {numbers}: {result}")
#     return {"sum": result}

# @app.post("/max-value", response_model=MaxResponse)
# def max_value(payload: Payload, token: str):
#     """
#     Encuentra el valor máximo en una lista de números.

#     Args:
#         payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
#         token (str): Token JWT para autenticación, pasado como query parameter.

#     Returns:
#         MaxResponse: Diccionario con la clave 'max' y el valor máximo.

#     Raises:
#         HTTPException: 400 si la lista está vacía.
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /max-value?token=<token> {"numbers": [1, 2, 3]}
#         Response: {"max": 3}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     if not numbers:
#         logger.error("Lista vacía recibida en /max-value")
#         raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
#     result = max(numbers)
#     logger.info(f"Valor máximo de {numbers}: {result}")
#     return {"max": result}

# @app.post("/binary-search", response_model=BinarySearchResponse)
# def binary_search(payload: BinarySearchPayload, token: str):
#     """
#     Realiza una búsqueda binaria en una lista ordenada para encontrar un número.

#     Args:
#         payload (BinarySearchPayload): Objeto con 'numbers' (lista ordenada) y 'target' (número a buscar).
#         token (str): Token JWT para autenticación, pasado como query parameter.

#     Returns:
#         BinarySearchResponse: Diccionario con 'found' (bool) e 'index' (int, -1 si no encontrado).

#     Raises:
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /binary-search?token=<token> {"numbers": [1, 2, 3, 4], "target": 3}
#         Response: {"found": true, "index": 2}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     target = payload.target
#     logger.info(f"Buscando {target} en {numbers}")
#     left, right = 0, len(numbers) - 1
#     while left <= right:
#         mid = (left + right) // 2
#         if numbers[mid] == target:
#             logger.info(f"Encontrado {target} en índice {mid}")
#             return {"found": True, "index": mid}
#         elif numbers[mid] < target:
#             left = mid + 1
#         else:
#             right = mid - 1
#     logger.info(f"No se encontró {target}")
#     return {"found": False, "index": -1}

# @app.post("/quick-sort", response_model=QuickSortResponse)
# def quick_sort(payload: Payload, token: str):
#     """
#     Ordena una lista de números usando el algoritmo Quick Sort.

#     Args:
#         payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
#         token (str): Token JWT para autenticación, pasado como query parameter.

#     Returns:
#         QuickSortResponse: Diccionario con la clave 'numbers' y la lista ordenada.

#     Raises:
#         HTTPException: 400 si la lista está vacía.
#         HTTPException: 401 si el token es inválido o el usuario no está autenticado.

#     Example:
#         Request: POST /quick-sort?token=<token> {"numbers": [3, 1, 4, 1, 5]}
#         Response: {"numbers": [1, 1, 3, 4, 5]}
#     """
#     get_current_user(token)
#     numbers = payload.numbers
#     if not numbers:
#         logger.error("Lista vacía recibida en /quick-sort")
#         raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
#     logger.info(f"Ordenando lista con Quick Sort: {numbers}")
    
#     def quicksort(arr, low, high):
#         if low < high:
#             pivot_idx = partition(arr, low, high)
#             quicksort(arr, low, pivot_idx - 1)
#             quicksort(arr, pivot_idx + 1, high)
    
#     def partition(arr, low, high):
#         pivot = arr[high]
#         i = low - 1
#         for j in range(low, high):
#             if arr[j] <= pivot:
#                 i += 1
#                 arr[i], arr[j] = arr[j], arr[i]
#         arr[i + 1], arr[high] = arr[high], arr[i + 1]
#         return i + 1
    
#     quicksort(numbers, 0, len(numbers) - 1)
#     logger.info(f"Lista ordenada: {numbers}")
#     return {"numbers": numbers}

from fastapi import FastAPI, HTTPException, Query
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import logging

# Configuración de logging para rastrear operaciones
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base de datos simulada en memoria
fake_db = {"users": {}}

# Configuración de JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Contexto para cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos de entrada
class Payload(BaseModel):
    numbers: List[int]
    """Lista de números enteros para procesar."""

class BinarySearchPayload(BaseModel):
    numbers: List[int]
    """Lista de números enteros ordenados para búsqueda."""
    target: int
    """Número objetivo a buscar en la lista."""

class Credentials(BaseModel):
    username: str
    """Nombre de usuario para registro o login."""
    password: str
    """Contraseña del usuario."""

# Modelos de respuesta
class BubbleSortResponse(BaseModel):
    numbers: List[int]
    """Lista de números ordenada."""

class EvenNumbersResponse(BaseModel):
    even_numbers: List[int]
    """Lista de números pares filtrados."""
    total: int
    """Cantidad total de números pares encontrados."""
    page: int
    """Página actual de los resultados."""
    page_size: int
    """Cantidad de elementos por página."""

class SumResponse(BaseModel):
    sum: int
    """Suma de los números en la lista."""

class MaxResponse(BaseModel):
    max: int
    """Valor máximo en la lista."""

class BinarySearchResponse(BaseModel):
    found: bool
    """Indica si el número objetivo fue encontrado."""
    index: int
    """Índice del número encontrado o -1 si no está."""

class QuickSortResponse(BaseModel):
    numbers: List[int]
    """Lista de números ordenada con Quick Sort."""

class MergeSortResponse(BaseModel):
    numbers: List[int]
    """Lista de números ordenada con Merge Sort."""

# Funciones de autenticación
def create_access_token(data: dict) -> str:
    """
    Genera un token JWT a partir de los datos proporcionados.

    Args:
        data (dict): Diccionario con los datos a codificar (ej. {"sub": "username"}).

    Returns:
        str: Token JWT codificado con el algoritmo HS256.

    Example:
        >>> create_access_token({"sub": "user1"})
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    """
    Cifra una contraseña usando el esquema bcrypt.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: Hash de la contraseña cifrada.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.

    Args:
        plain_password (str): Contraseña en texto plano ingresada por el usuario.
        hashed_password (str): Hash almacenado de la contraseña.

    Returns:
        bool: True si la contraseña es válida, False si no.
    """
    logger.debug(f"Verificando contraseña para hash: {hashed_password}")
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(token: str) -> None:
    """
    Verifica un token JWT y valida la autenticación del usuario.

    Args:
        token (str): Token JWT pasado como query parameter.

    Raises:
        HTTPException: 401 si el token es inválido o el usuario no existe.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_db["users"]:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        logger.info(f"Usuario autenticado: {username}")
    except Exception as e:
        logger.error(f"Error al verificar token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Aplicación FastAPI
app = FastAPI(
    title="API de Algoritmos con Autenticación",
    description="Una API que implementa algoritmos básicos como Bubble Sort, Quick Sort, Merge Sort y búsqueda binaria, con autenticación basada en JWT y soporte para paginación.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Endpoints
@app.post("/register")
def register(payload: Credentials):
    """
    Registra un nuevo usuario con una contraseña cifrada.

    Args:
        payload (Credentials): Objeto con 'username' y 'password'.

    Returns:
        dict: Mensaje de éxito {"message": "User registered successfully"}.

    Raises:
        HTTPException: 400 si el usuario ya existe.

    Example:
        Request: POST /register {"username": "user1", "password": "pass1"}
        Response: {"message": "User registered successfully"}
    """
    username = payload.username
    password = payload.password
    if username in fake_db["users"]:
        logger.warning(f"Intento de registro de usuario existente: {username}")
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(password)
    fake_db["users"][username] = {"password": hashed_password}
    logger.info(f"Usuario registrado: {username}")
    return {"message": "User registered successfully"}

@app.post("/login")
def login(payload: Credentials):
    """
    Inicia sesión y devuelve un token JWT para autenticación.

    Args:
        payload (Credentials): Objeto con 'username' y 'password'.

    Returns:
        dict: Diccionario con el token {"access_token": "<token>"}.

    Raises:
        HTTPException: 401 si las credenciales son inválidas.

    Example:
        Request: POST /login {"username": "user1", "password": "pass1"}
        Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    """
    username = payload.username
    password = payload.password
    if username not in fake_db["users"]:
        logger.warning(f"Intento de login con usuario no existente: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user = fake_db["users"][username]
    if not verify_password(password, user["password"]):
        logger.warning(f"Contraseña incorrecta para usuario: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": username})
    logger.info(f"Login exitoso para usuario: {username}")
    return {"access_token": access_token}

@app.post("/bubble-sort", response_model=BubbleSortResponse)
def bubble_sort(payload: Payload, token: str):
    """
    Ordena una lista de números usando el algoritmo Bubble Sort optimizado.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        BubbleSortResponse: Diccionario con la clave 'numbers' y la lista ordenada.

    Raises:
        HTTPException: 400 si la lista está vacía.
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /bubble-sort?token=<token> {"numbers": [3, 2, 1]}
        Response: {"numbers": [1, 2, 3]}
    """
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        logger.error("Lista vacía recibida en /bubble-sort")
        raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
    logger.info(f"Ordenando lista con Bubble Sort: {numbers}")
    n = len(numbers)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                swapped = True
        if not swapped:
            break
    logger.info(f"Lista ordenada: {numbers}")
    return {"numbers": numbers}

@app.post("/filter-even", response_model=EvenNumbersResponse)
def filter_even(
    payload: Payload,
    token: str,
    page: int = Query(1, ge=1, description="Número de página (mínimo 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página (1-100)")
):
    """
    Filtra números pares de una lista con soporte para paginación.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.
        page (int): Número de página a devolver (default: 1).
        page_size (int): Cantidad de elementos por página (default: 10, máximo 100).

    Returns:
        EvenNumbersResponse: Números pares paginados, total, página actual y tamaño.

    Raises:
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /filter-even?token=<token>&page=1&page_size=2 {"numbers": [1, 2, 3, 4, 5, 6]}
        Response: {"even_numbers": [2, 4], "total": 3, "page": 1, "page_size": 2}
    """
    get_current_user(token)
    numbers = payload.numbers
    logger.info(f"Filtrando números pares de: {numbers}")
    even_numbers = [number for number in numbers if number % 2 == 0]
    total = len(even_numbers)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_numbers = even_numbers[start:end]
    logger.info(f"Números pares filtrados: {paginated_numbers}")
    return {
        "even_numbers": paginated_numbers,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@app.post("/sum-elements", response_model=SumResponse)
def sum_elements(payload: Payload, token: str):
    """
    Calcula la suma de los elementos de una lista de números.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        SumResponse: Diccionario con la clave 'sum' y el valor de la suma.

    Raises:
        HTTPException: 400 si la lista está vacía.
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /sum-elements?token=<token> {"numbers": [1, 2, 3]}
        Response: {"sum": 6}
    """
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        logger.error("Lista vacía recibida en /sum-elements")
        raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
    result = sum(numbers)
    logger.info(f"Suma de {numbers}: {result}")
    return {"sum": result}

@app.post("/max-value", response_model=MaxResponse)
def max_value(payload: Payload, token: str):
    """
    Encuentra el valor máximo en una lista de números.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        MaxResponse: Diccionario con la clave 'max' y el valor máximo.

    Raises:
        HTTPException: 400 si la lista está vacía.
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /max-value?token=<token> {"numbers": [1, 2, 3]}
        Response: {"max": 3}
    """
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        logger.error("Lista vacía recibida en /max-value")
        raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
    result = max(numbers)
    logger.info(f"Valor máximo de {numbers}: {result}")
    return {"max": result}

@app.post("/binary-search", response_model=BinarySearchResponse)
def binary_search(payload: BinarySearchPayload, token: str):
    """
    Realiza una búsqueda binaria en una lista ordenada para encontrar un número.

    Args:
        payload (BinarySearchPayload): Objeto con 'numbers' (lista ordenada) y 'target' (número a buscar).
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        BinarySearchResponse: Diccionario con 'found' (bool) e 'index' (int, -1 si no encontrado).

    Raises:
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /binary-search?token=<token> {"numbers": [1, 2, 3, 4], "target": 3}
        Response: {"found": true, "index": 2}
    """
    get_current_user(token)
    numbers = payload.numbers
    target = payload.target
    logger.info(f"Buscando {target} en {numbers}")
    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            logger.info(f"Encontrado {target} en índice {mid}")
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    logger.info(f"No se encontró {target}")
    return {"found": False, "index": -1}

@app.post("/quick-sort", response_model=QuickSortResponse)
def quick_sort(payload: Payload, token: str):
    """
    Ordena una lista de números usando el algoritmo Quick Sort.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        QuickSortResponse: Diccionario con la clave 'numbers' y la lista ordenada.

    Raises:
        HTTPException: 400 si la lista está vacía.
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /quick-sort?token=<token> {"numbers": [3, 1, 4, 1, 5]}
        Response: {"numbers": [1, 1, 3, 4, 5]}
    """
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        logger.error("Lista vacía recibida en /quick-sort")
        raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
    logger.info(f"Ordenando lista con Quick Sort: {numbers}")
    
    def quicksort(arr, low, high):
        if low < high:
            pivot_idx = partition(arr, low, high)
            quicksort(arr, low, pivot_idx - 1)
            quicksort(arr, pivot_idx + 1, high)
    
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    quicksort(numbers, 0, len(numbers) - 1)
    logger.info(f"Lista ordenada: {numbers}")
    return {"numbers": numbers}

@app.post("/merge-sort", response_model=MergeSortResponse)
def merge_sort(payload: Payload, token: str):
    """
    Ordena una lista de números usando el algoritmo Merge Sort.

    Args:
        payload (Payload): Objeto con una lista de enteros en el campo 'numbers'.
        token (str): Token JWT para autenticación, pasado como query parameter.

    Returns:
        MergeSortResponse: Diccionario con la clave 'numbers' y la lista ordenada.

    Raises:
        HTTPException: 400 si la lista está vacía.
        HTTPException: 401 si el token es inválido o el usuario no está autenticado.

    Example:
        Request: POST /merge-sort?token=<token> {"numbers": [5, 2, 9, 1, 5, 6]}
        Response: {"numbers": [1, 2, 5, 5, 6, 9]}
    """
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        logger.error("Lista vacía recibida en /merge-sort")
        raise HTTPException(status_code=400, detail="La lista no puede estar vacía")
    logger.info(f"Ordenando lista con Merge Sort: {numbers}")

    def merge(arr, left, mid, right):
        left_half = arr[left:mid + 1]
        right_half = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    def mergesort(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            mergesort(arr, left, mid)
            mergesort(arr, mid + 1, right)
            merge(arr, left, mid, right)

    mergesort(numbers, 0, len(numbers) - 1)
    logger.info(f"Lista ordenada: {numbers}")
    return {"numbers": numbers}