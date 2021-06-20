from PyQt5.QtWidgets import QGraphicsBlurEffect


def blur_widget(widgets):
    for widget in widgets:
        blur_effect = QGraphicsBlurEffect()
        widget.setGraphicsEffect(blur_effect)
