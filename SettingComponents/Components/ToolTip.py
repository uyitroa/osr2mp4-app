from PyQt5 import QtWidgets, QtCore, QtGui


class ClickableTooltip(QtWidgets.QLabel):
	__instance = None
	refWidget = None
	refPos = None
	menuShowing = False

	def __init__(self):
		super().__init__(flags=QtCore.Qt.ToolTip)
		margin = self.style().pixelMetric(
			QtWidgets.QStyle.PM_ToolTipLabelFrameWidth, None, self)
		self.setMargin(margin + 1)
		self.setForegroundRole(QtGui.QPalette.ToolTipText)
		self.setWordWrap(True)

		self.mouseTimer = QtCore.QTimer(interval=250, timeout=self.checkCursor)
		self.hideTimer = QtCore.QTimer(singleShot=True, timeout=self.hide)

		self.setStyleSheet("""background-color: rgb(40, 40, 43); color: white;""")

	def checkCursor(self):
		# ignore if the link context menu is visible
		for menu in self.findChildren(
			QtWidgets.QMenu, options=QtCore.Qt.FindDirectChildrenOnly):
				if menu.isVisible():
					return

		# an arbitrary check for mouse position; since we have to be able to move
		# inside the tooltip margins (standard QToolTip hides itself on hover),
		# let's add some margins just for safety
		region = QtGui.QRegion(self.geometry().adjusted(-10, -10, 10, 10))
		if self.refWidget:
			rect = self.refWidget.rect()
			rect.moveTopLeft(self.refWidget.mapToGlobal(QtCore.QPoint()))
			region |= QtGui.QRegion(rect)
		else:
			# add a circular region for the mouse cursor possible range
			rect = QtCore.QRect(0, 0, 16, 16)
			rect.moveCenter(self.refPos)
			region |= QtGui.QRegion(rect, QtGui.QRegion.Ellipse)
		if QtGui.QCursor.pos() not in region:
			self.hide()

	def show(self):
		super().show()
		QtWidgets.QApplication.instance().installEventFilter(self)

	def event(self, event):
		# just for safety...
		if event.type() == QtCore.QEvent.WindowDeactivate:
			self.hide()
		return super().event(event)

	def eventFilter(self, source, event):
		# if we detect a mouse button or key press that's not originated from the
		# label, assume that the tooltip should be closed; note that widgets that
		# have been just mapped ("shown") might return events for their QWindow
		# instead of the actual QWidget
		if source not in (self, self.windowHandle()) and event.type() in (
			QtCore.QEvent.MouseButtonPress, QtCore.QEvent.KeyPress):
				self.hide()
		return super().eventFilter(source, event)

	def move(self, pos):
		# ensure that the style has "polished" the widget (font, palette, etc.)
		self.ensurePolished()
		# ensure that the tooltip is shown within the available screen area
		geo = QtCore.QRect(pos, self.sizeHint())
		try:
			screen = QtWidgets.QApplication.screenAt(pos)
		except:
			# support for Qt < 5.10
			for screen in QtWidgets.QApplication.screens():
				if pos in screen.geometry():
					break
			else:
				screen = None
		if not screen:
			screen = QtWidgets.QApplication.primaryScreen()
		screenGeo = screen.availableGeometry()
		# screen geometry correction should always consider the top-left corners
		# *last* so that at least their beginning text is always visible (that's
		# why I used pairs of "if" instead of "if/else"); also note that this
		# doesn't take into account right-to-left languages, but that can be
		# accounted for by checking QGuiApplication.layoutDirection()
		if geo.bottom() > screenGeo.bottom():
			geo.moveBottom(screenGeo.bottom())
		if geo.top() < screenGeo.top():
			geo.moveTop(screenGeo.top())
		if geo.right() > screenGeo.right():
			geo.moveRight(screenGeo.right())
		if geo.left() < screenGeo.left():
			geo.moveLeft(screenGeo.left())
		super().move(geo.topLeft())

	def contextMenuEvent(self, event):
		# check the children QMenu objects before showing the menu (which could
		# potentially hide the label)
		knownChildMenus = set(self.findChildren(
			QtWidgets.QMenu, options=QtCore.Qt.FindDirectChildrenOnly))
		self.menuShowing = True
		super().contextMenuEvent(event)
		newMenus = set(self.findChildren(
			QtWidgets.QMenu, options=QtCore.Qt.FindDirectChildrenOnly))
		if knownChildMenus == newMenus:
			# no new context menu? hide!
			self.hide()
		else:
			# hide ourselves as soon as the (new) menus close
			for m in knownChildMenus ^ newMenus:
				m.aboutToHide.connect(self.hide)
				m.aboutToHide.connect(lambda m=m: m.aboutToHide.disconnect())
			self.menuShowing = False

	def mouseReleaseEvent(self, event):
		# click events on link are delivered on button release!
		super().mouseReleaseEvent(event)
		self.hide()

	def hide(self):
		if not self.menuShowing:
			super().hide()

	def hideEvent(self, event):
		super().hideEvent(event)
		QtWidgets.QApplication.instance().removeEventFilter(self)
		if self.refWidget:
			self.refWidget.window().removeEventFilter(self)
		self.refWidget = self.refPos = None
		self.mouseTimer.stop()
		self.hideTimer.stop()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		# on some systems the tooltip is not a rectangle, let's "mask" the label
		# according to the system defaults
		opt = QtWidgets.QStyleOption()
		opt.initFrom(self)
		mask = QtWidgets.QStyleHintReturnMask()
		if self.style().styleHint(
			QtWidgets.QStyle.SH_ToolTip_Mask, opt, self, mask):
				self.setMask(mask.region)

	def paintEvent(self, event):
		# we cannot directly draw the label, since a tooltip could have an inner
		# border, so let's draw the "background" before that
		qp = QtGui.QPainter(self)
		opt = QtWidgets.QStyleOption()
		opt.initFrom(self)
		style = self.style()
		style.drawPrimitive(style.PE_PanelTipLabel, opt, qp, self)
		# now we paint the label contents
		super().paintEvent(event)

	@staticmethod
	def showText(pos, text:str, parent=None, rect=None, delay=0):
		# this is a method similar to QToolTip.showText;
		# it reuses an existent instance, but also returns the tooltip so that
		# its linkActivated signal can be connected
		if ClickableTooltip.__instance is None:
			if not text:
				return
			ClickableTooltip.__instance = ClickableTooltip()
		toolTip = ClickableTooltip.__instance

		toolTip.mouseTimer.stop()
		toolTip.hideTimer.stop()

		# disconnect all previously connected signals, if any
		try:
			toolTip.linkActivated.disconnect()
		except:
			pass

		if not text:
			toolTip.hide()
			return
		toolTip.setText(text)

		if parent:
			toolTip.refRect = rect
		else:
			delay = 0

		pos += QtCore.QPoint(16, 16)

		# adjust the tooltip position if necessary (based on arbitrary margins)
		if not toolTip.isVisible() or parent != toolTip.refWidget or (
			not parent and toolTip.refPos and
			(toolTip.refPos - pos).manhattanLength() > 10):
				toolTip.move(pos)

		# we assume that, if no parent argument is given, the current activeWindow
		# is what we should use as a reference for mouse detection
		toolTip.refWidget = parent or QtWidgets.QApplication.activeWindow()
		toolTip.refPos = pos
		toolTip.show()
		toolTip.mouseTimer.start()
		if delay:
			toolTip.hideTimer.start(delay)

		return toolTip
