class CapMarksController:
    def __init__(self):
        self.marks = {}
        self.selected_char = None
        for a in ["A", "B", "C", "D", "E"]:
            self.marks[a] ={
                                "position":[0,0],
                                "active":False,
                                "selected": False
                            }
    def proceed_command(self, cmd: Command):
        action = cmd.get_action()
        params = cmd.get_params()
        match action:
            case "make_point":
                if self.selected_char not in self.marks: return
                self.marks[self.selected_char] = {
                    "position":params["position"],
                    "active":True
                }
                self.selected_char = None
            case "deactivate_point":
                if params["char"] not in self.marks: return
                self.marks[params["char"]]["active"] = False

            case "select_point":
                if params["char"] not in self.marks: return
                for a in self.marks:
                    self.marks[a]["selected"] = False
                self.selected_char = params["char"]
                self.marks[self.selected_char]["selected"] = True

    def get_marks(self):
        return self.marks
