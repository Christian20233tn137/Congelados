   # Requisitos del Sistema — Código Congelado
   **Metodología:** Cascada  
   **Fase:** 1 — Levantamiento de Requisitos  
   **Fecha:** 2026-05-07

   ---

   ## 1. Descripción general del sistema

   **Código Congelado** es un mini juego web educativo dirigido a alumnos de primer cuatrimestre. El objetivo del juego es que el jugador practique conceptos básicos de programación (variables, condicionales, ciclos y funciones) mediante preguntas de opción múltiple. El jugador avanza de nivel respondiendo correctamente y pierde vidas si se equivoca.

   ---

   ## 2. Usuarios del sistema

   | ID | Rol | Descripción |
   |----|-----|-------------|
   | U1 | Jugador (Alumno) | Alumno que accede al juego para practicar programación básica. |
   | U2 | Docente | Persona que supervisa que el juego cumpla el objetivo educativo. |

   ---

   ## 3. Requisitos Funcionales

   Los requisitos funcionales describen **qué debe hacer** el sistema.

   | ID | Requisito | Prioridad |
   |----|-----------|-----------|
   | RF-01 | El sistema debe mostrar una pantalla de inicio con el nombre del juego, una breve descripción y un botón "Iniciar". | Alta |
   | RF-02 | El jugador debe poder iniciar una partida desde la pantalla principal. | Alta |
   | RF-03 | El sistema debe presentar preguntas de opción múltiple con cuatro opciones (A, B, C, D) por nivel. | Alta |
   | RF-04 | El sistema debe validar si la respuesta seleccionada por el jugador es correcta o incorrecta. | Alta |
   | RF-05 | Si la respuesta es correcta, el sistema debe sumar 10 puntos al marcador del jugador. | Alta |
   | RF-06 | Si la respuesta es incorrecta, el sistema debe restar una vida al jugador. | Alta |
   | RF-07 | El jugador debe iniciar cada partida con 3 vidas. | Alta |
   | RF-08 | El sistema debe permitir al jugador avanzar al siguiente nivel únicamente si respondió correctamente. | Alta |
   | RF-09 | El sistema debe finalizar la partida y mostrar la pantalla de derrota cuando el jugador pierda todas sus vidas. | Alta |
   | RF-10 | El sistema debe finalizar la partida y mostrar la pantalla de victoria cuando el jugador responda todas las preguntas correctamente. | Alta |
   | RF-11 | La pantalla de pregunta debe mostrar en todo momento: número de nivel, pregunta, opciones de respuesta, vidas restantes y puntuación actual. | Alta |
   | RF-12 | El sistema debe mostrar la puntuación final del jugador en la pantalla de resultado. | Alta |
   | RF-13 | El sistema debe mostrar un mensaje diferenciado según el resultado: victoria o derrota. | Media |
   | RF-14 | El jugador debe poder reiniciar el juego desde la pantalla de resultado mediante un botón "Jugar de nuevo". | Alta |
   | RF-15 | Las preguntas deben cubrir los temas: variables, condicionales, ciclos y funciones. | Media |

   ---

   ## 4. Requisitos No Funcionales

   Los requisitos no funcionales describen **cómo debe comportarse** el sistema.

   ### 4.1 Usabilidad

   | ID | Requisito |
   |----|-----------|
   | RNF-01 | La interfaz debe ser intuitiva y comprensible para alumnos principiantes sin experiencia previa en videojuegos. |
   | RNF-02 | La navegación entre pantallas no debe requerir más de un clic por acción. |
   | RNF-03 | Los textos, botones e instrucciones deben estar escritos en español y con lenguaje claro. |

   ### 4.2 Rendimiento

   | ID | Requisito |
   |----|-----------|
   | RNF-04 | Las preguntas deben cargarse en menos de 2 segundos. |
   | RNF-05 | La validación de respuesta debe ejecutarse de forma inmediata tras la selección del jugador (< 1 segundo). |

   ### 4.3 Compatibilidad

   | ID | Requisito |
   |----|-----------|
   | RNF-06 | El juego debe funcionar correctamente en navegadores modernos: Chrome, Firefox, Edge y Safari. |
   | RNF-07 | El juego debe ser responsive: debe verse y funcionar correctamente en computadora y dispositivo móvil. |

   ### 4.4 Disponibilidad

   | ID | Requisito |
   |----|-----------|
   | RNF-08 | El juego debe poder ejecutarse desde un navegador web sin necesidad de instalación. |

   ### 4.5 Mantenibilidad

   | ID | Requisito |
   |----|-----------|
   | RNF-09 | Las preguntas deben estar organizadas en una estructura de datos separada para facilitar su edición sin modificar la lógica del juego. |

   ---

   ## 5. Reglas del negocio

   | ID | Regla |
   |----|-------|
   | RN-01 | El jugador inicia cada partida con 3 vidas. |
   | RN-02 | Cada respuesta correcta suma 10 puntos. |
   | RN-03 | Cada respuesta incorrecta resta 1 vida. |
   | RN-04 | Si el jugador pierde todas las vidas, la partida termina en derrota. |
   | RN-05 | Si el jugador responde todas las preguntas sin perder todas las vidas, la partida termina en victoria. |
   | RN-06 | La puntuación se muestra al finalizar la partida. |

   ---

   ## 6. Flujo general del sistema

   ```
   Pantalla de Inicio
         ↓
   [Iniciar]
         ↓
   Pregunta Nivel 1
         ↓
   ¿Respuesta correcta?
      ↙         ↘
   Sí          No
   ↓            ↓
   +10 pts     -1 vida
   ↓            ↓
   Siguiente    ¿Vidas = 0?
   nivel          ↙    ↘
               Sí     No
               ↓      ↓
            Derrota  Siguiente
               ↓      nivel
            Pantalla    ...
            resultado    ↓
                     Victoria
                        ↓
                     Pantalla
                     resultado
   ```

   ---

   ## 7. Restricciones del proyecto

   - El sistema se desarrollará como aplicación web (no nativa).
   - No se requiere base de datos ni autenticación de usuarios para la versión inicial.
   - El juego no guardará el historial de partidas entre sesiones.

   ---

   ## 8. Criterios de aceptación

   El sistema será aceptado si cumple con los siguientes puntos verificables:

   1. El jugador puede completar una partida de inicio a fin sin errores.
   2. La puntuación se incrementa correctamente con cada acierto.
   3. Las vidas disminuyen correctamente con cada fallo.
   4. La pantalla de derrota aparece al perder las 3 vidas.
   5. La pantalla de victoria aparece al responder todas las preguntas.
   6. El botón "Jugar de nuevo" reinicia la partida correctamente.
   7. El juego es funcional en pantalla de escritorio y móvil.
