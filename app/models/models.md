# Modelo ER — reclutamiento

`Usuario` no tiene llave foránea: es la cuenta del admin y del reclutador. El correo que llega es un `Mensaje`. Solo si la persona acepta se guarda su archivo en `HojaVida` y la IA escribe `Clasificacion`. `Evaluacion` solo existe si esa clasificación quedó asignada. `Revision` la escribe el reclutador después de la evaluación.

```mermaid
erDiagram
    VACANTE ||--o{ CARACTERISTICA : tiene
    VACANTE |o--o{ CLASIFICACION : asigna
    MENSAJE ||--o| CONSENTIMIENTO : responde
    MENSAJE ||--o| HOJA_VIDA : carga
    MENSAJE ||--o| CLASIFICACION : clasifica
    MENSAJE ||--o| EVALUACION : evalua
    MENSAJE ||--o| REVISION : decide

    USUARIO {
        int id PK
        string correo UK
        string clave_hash
        string rol
    }

    VACANTE {
        int id PK
        string titulo
        string descripcion
        string ciudad
        string estado
        string modalidad
        datetime creada_en
    }

    CARACTERISTICA {
        int id PK
        int vacante_id FK
        string tipo
        string valor
        string texto
    }

    MENSAJE {
        int id PK
        string message_id UK
        string de
        string asunto
        datetime fecha
        string token UK
        string estado
    }

    CONSENTIMIENTO {
        int id PK
        int mensaje_id FK
        bool acepta
        string texto_aviso
        string version_aviso
        datetime fecha
    }

    HOJA_VIDA {
        int id PK
        int mensaje_id FK
        string nombre_archivo
        string tipo_archivo
        blob archivo
        datetime recibida_en
    }

    CLASIFICACION {
        int id PK
        int mensaje_id FK
        int vacante_id FK
        string resultado
        string motivo
        datetime fecha
    }

    EVALUACION {
        int id PK
        int mensaje_id FK
        string fase_final
        int puntaje
        string detalle
        datetime fecha
    }

    REVISION {
        int id PK
        int mensaje_id FK
        string decision
        string nota
        datetime fecha
    }
