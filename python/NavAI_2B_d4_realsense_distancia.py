"""
NavAI - Medición de distancia con cámara Intel RealSense (serie D4xx)

Uso:
    python NavAI_2B_d4_realsense_distancia.py

- Haz clic izquierdo en la imagen para medir la distancia a ese punto.
- Puedes marcar varios puntos (se guardan los últimos 10).
- Tecla C: borrar los puntos.
- Tecla Q o ESC: salir.
"""

import sys

import numpy as np
import cv2

try:
    import pyrealsense2 as rs
except ImportError:
    print("ERROR: no está instalado pyrealsense2.")
    print("Ejecuta: pip install -r requirements.txt")
    sys.exit(1)


ANCHO, ALTO, FPS = 640, 480, 30
MAX_PUNTOS = 10
VENTANA = "NavAI - Distancia RealSense (clic = medir, C = borrar, Q = salir)"

puntos = []  # lista de (x, y) donde ha hecho clic el usuario


def al_hacer_clic(evento, x, y, flags, param):
    if evento == cv2.EVENT_LBUTTONDOWN:
        puntos.append((x, y))
        if len(puntos) > MAX_PUNTOS:
            puntos.pop(0)


def distancia_en_punto(frame_profundidad, x, y):
    """Devuelve la distancia en metros, usando la mediana de una zona 5x5
    alrededor del punto para evitar valores 0 (sin dato)."""
    valores = []
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            px, py = x + dx, y + dy
            if 0 <= px < ANCHO and 0 <= py < ALTO:
                d = frame_profundidad.get_distance(px, py)
                if d > 0:
                    valores.append(d)
    if not valores:
        return 0.0
    return float(np.median(valores))


def dibujar_texto(img, texto, pos, color=(255, 255, 255)):
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(img, texto, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)


def main():
    # Comprobar que hay una cámara conectada
    ctx = rs.context()
    if len(ctx.query_devices()) == 0:
        print("ERROR: no se detecta ninguna cámara RealSense.")
        print("Conéctala a un puerto USB 3 (azul) y vuelve a intentarlo.")
        sys.exit(1)

    dispositivo = ctx.query_devices()[0]
    nombre = dispositivo.get_info(rs.camera_info.name)
    print(f"Cámara detectada: {nombre}")

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, ANCHO, ALTO, rs.format.z16, FPS)
    config.enable_stream(rs.stream.color, ANCHO, ALTO, rs.format.bgr8, FPS)

    try:
        pipeline.start(config)
    except RuntimeError as e:
        print("ERROR al iniciar la cámara:", e)
        print("Comprueba que está en un USB 3 y que ningún otro programa la está usando.")
        sys.exit(1)

    # Alinear la profundidad con la imagen de color (para que el clic coincida)
    alinear = rs.align(rs.stream.color)

    cv2.namedWindow(VENTANA)
    cv2.setMouseCallback(VENTANA, al_hacer_clic)

    print("Haz clic en la imagen para medir distancias. Q para salir.")

    try:
        while True:
            frames = pipeline.wait_for_frames()
            frames = alinear.process(frames)
            profundidad = frames.get_depth_frame()
            color = frames.get_color_frame()
            if not profundidad or not color:
                continue

            imagen = np.asanyarray(color.get_data()).copy()

            # Distancia en el centro de la imagen (siempre visible)
            cx, cy = ANCHO // 2, ALTO // 2
            d_centro = distancia_en_punto(profundidad, cx, cy)
            cv2.drawMarker(imagen, (cx, cy), (0, 255, 255), cv2.MARKER_CROSS, 20, 2)
            dibujar_texto(imagen, f"Centro: {d_centro:.2f} m", (10, 25), (0, 255, 255))

            # Puntos marcados por el usuario
            for i, (x, y) in enumerate(puntos, start=1):
                d = distancia_en_punto(profundidad, x, y)
                cv2.circle(imagen, (x, y), 6, (0, 0, 255), -1)
                if d > 0:
                    texto = f"{i}: {d:.2f} m ({d * 100:.0f} cm)"
                else:
                    texto = f"{i}: sin dato"
                dibujar_texto(imagen, texto, (x + 10, y - 10), (0, 255, 0))

            dibujar_texto(imagen, nombre, (10, ALTO - 15), (200, 200, 200))

            cv2.imshow(VENTANA, imagen)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla in (ord("q"), ord("Q"), 27):
                break
            if tecla in (ord("c"), ord("C")):
                puntos.clear()
            # Salir también si se cierra la ventana con la X
            if cv2.getWindowProperty(VENTANA, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
