# NavAI · Visión 3D para un robot móvil que vigila el pasillo

Proyecto de fin de ciclo · 2.º CFGS Automatización y Robótica Industrial · Grupo 2B
IES Antonio Machado (Torrejón de Ardoz) · Curso 2026-2027

## Autores
- Alexandro Petretchi Atodiresei: hardware, soporte, MQTT y panel Node-RED
- Ahmed Kadoussi: visión, modelo YOLO y medida de distancia

## Qué es
Una cámara Intel RealSense D435 recorre el pasillo montada en un carro. Un portátil
detecta personas y mochilas con un modelo YOLO, mide a qué distancia está cada una con
la imagen de profundidad y publica cada detección por MQTT (broker Mosquitto). Las
detecciones aparecen en un panel de Node-RED. Como mejora (Nivel 2), el sistema se
monta en el robot móvil Omron LD-90 y lo para por ARCL cuando hay una persona cerca.

## Material
- Cámara Intel RealSense D435 (color + profundidad)
- Portátil con Python 3
- Carro o trípode para el pasillo
- Robot móvil Omron LD-90 (solo al final, por turnos)

## Software
- Python: pyrealsense2, OpenCV, Ultralytics YOLO
- Mosquitto (MQTT) y Node-RED
- Fusion 360 (soporte de la cámara)

## Cómo se arranca
Pendiente: se completará cuando el código esté listo (ver `doc/` para el manual).

## Estructura del repositorio
| Carpeta | Contenido |
|---|---|
| `doc/` | Plan, riesgos, bitácora, memoria, manual, presupuesto y cartel |
| `cad/` | Soporte de la cámara (STEP y STL) |
| `esquemas/` | Esquemas eléctricos y de red |
| `plc/` | Proyecto de TIA Portal (.zap), si se usa |
| `robot/` | Órdenes ARCL del LD-90 |
| `python/` | Scripts y requirements.txt |
| `pruebas/` | Protocolos y resultados de las pruebas |
| `media/` | Fotos y vídeos |

## Nombre de los ficheros
`NavAI_2B_<documento>_v<versión>`, por ejemplo `NavAI_2B_memoria_v1.2.pdf`

## Seguridad y privacidad
La visión no es una función de seguridad: el LD-90 se protege con su propio láser, que
no se toca. Fotos solo con autorización, caras pixeladas y no se identifica a nadie.
