# Mi API de Algoritmos

## Flujo de Uso

```mermaid
flowchart TD
    A[Usuario] --> B[Registrarse: POST /register]
    B --> C[Iniciar sesión: POST /login]
    C --> D[Obtener Token]
    D --> E[Usar API: POST /bubble-sort?token=<token>]
    D --> F[Usar API: POST /quick-sort?token=<token>]
    D --> G[Usar API: POST /merge-sort?token=<token>]
    E --> H[Respuesta: Lista Ordenada]
    F --> H
    G --> H
