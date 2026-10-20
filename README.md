# Regolith

Prototipo de un juego de vida y construcción en la Luna, hecho con Pygame.

## Ejecutar

Con el entorno preparado: `make run`. Para instalarlo desde cero: `make install`.

## Controles

- **WASD / flechas:** mover al personaje.
- **B:** alternar exploración y construcción.
- **1–5 / clic en la toolbar:** seleccionar una de las primeras cinco casillas del inventario.
- **Clic en el tablero:** colocar el módulo seleccionado en modo construcción.
- **Tab:** abrir o cerrar el inventario. Haz clic en dos casillas para intercambiarlas.
- **E:** inspeccionar un módulo cercano; vuelve a pulsar E para cerrar.
- **R en la ventana del módulo:** recogerlo al inventario.
- **Escape:** cerrar la ventana actual, salir de construcción o salir del juego.

La partida empieza con tres unidades de cada módulo. Colocar consume una unidad;
recoger la devuelve. La toolbar muestra las mismas cantidades que el inventario.
Las ventanas pausan el movimiento y bloquean la construcción.

Esta versión permite colocar, explorar, inspeccionar y recuperar módulos. Todavía
no hay producción de recursos, consumo de estadísticas ni guardado de partidas.
