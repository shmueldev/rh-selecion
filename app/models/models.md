# Modelo ER — reclutamiento

`Usuario` no tiene llave foránea: es la cuenta del admin y del reclutador. Las demás tablas se amarran así: una vacante tiene varias características y varias invitaciones; cada invitación tiene como máximo un consentimiento, una hoja de vida, una evaluación y una revisión.

```mermaid
erDiagram
    VACANTE ||--o{ CARACTERISTICA : tiene
    VACANTE ||--o{ INVITACION : recibe
    INVITACION ||--o| CONSENTIMIENTO : responde
    INVITACION ||--o| HOJA_VIDA : carga
    INVITACION ||--o| EVALUACION : evalua
    INVITACION ||--o| REVISION : decide

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

    INVITACION {
        int id PK
        int vacante_id FK
        string correo
        string token UK
        string estado
        datetime creada_en
        datetime vence_en
    }

    CONSENTIMIENTO {
        int id PK
        int invitacion_id FK
        bool acepta
        string texto_aviso
        string version_aviso
        datetime fecha
    }

    HOJA_VIDA {
        int id PK
        int invitacion_id FK
        string contenido
        datetime recibida_en
    }

    EVALUACION {
        int id PK
        int invitacion_id FK
        string fase_final
        int puntaje
        string detalle
        datetime fecha
    }

    REVISION {
        int id PK
        int invitacion_id FK
        string decision
        string nota
        datetime fecha
    }