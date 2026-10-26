# Gestionar un cambio con SDD

Usa este flujo para especificar y planificar un cambio significativo en un
repositorio de código existente. No genera aplicaciones ni elige frameworks.

Antes de proponer artefactos:

1. Lee las instrucciones del repositorio, su arquitectura relevante, pruebas y
   cualquier sistema o documento de especificación existente.
2. Conserva las convenciones encontradas. No dupliques OpenSpec u otro sistema.
3. Aclara el objetivo, límites, compatibilidad esperada y evidencia de éxito.
   Registra lo desconocido como pregunta abierta, no como supuesto silencioso.
4. Usa `docs/specs/<initiative-id>/` solo si el repositorio no tiene otra
   ubicación o sistema de especificación.
5. Mantén aprobación humana entre capability map (si aplica), especificación,
   plan/tareas e implementación. Detente después de presentar cada fase hasta
   recibir aprobación.
6. Tras aprobar tareas, implementa solo su alcance en el repositorio existente y
   verifica los criterios contra sus pruebas y comandos reales.

Registra el proyecto en la wiki Second Brain con
`projects/<project-id>/PROJECT.md` si el usuario quiere seguimiento duradero.
Ese registro enlaza a los artefactos del repo; no los copia. La publicación en
portfolio es una decisión aparte y requiere aprobación explícita.