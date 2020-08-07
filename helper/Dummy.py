from osr2mp4.Parser.osuparser import Beatmap


class BeatmapDummy(Beatmap):
	def __init__(self):
		super().__init__({"General": "", "Metadata": "", "Difficulty": "", "Events": "", "TimingPoints": "", "HitObjects": ""})
		self.start_time = 0
		self.end_time = 1

