class Score:
    def __init__(self, file_name="highscore.txt"):
        self.current_score = 0
        self.file_name = file_name
        self.high_score = self._load_high_score()

    def _load_high_score(self):
        try:
            with open(self.file_name, "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_high_score(self):
        with open(self.file_name, "w") as file:
            file.write(str(self.high_score))

    def update(self):
        self.current_score += 1
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self._save_high_score()

    def reset(self):
        self.current_score = 0
