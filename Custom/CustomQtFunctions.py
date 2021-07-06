from PyQt5.QtWidgets import QGraphicsBlurEffect


def blur_widget(widgets):
    for widget in widgets:
        blur_effect = QGraphicsBlurEffect()
        widget.setGraphicsEffect(blur_effect)
        widget.blur_effect = blur_effect


def unblur_widget(widgets):
    for widget in widgets:
        widget.blur_effect.setEnabled(False)


