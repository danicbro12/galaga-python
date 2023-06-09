from .control_point_quartet_collection import ControlPointQuartetCollection
from .path_point_selector import PathPointSelector
from .control_point_handler import ControlPointHandler


class ControlHandlerMover():
    def __init__(self,
                 control_point_quartet_collection: ControlPointQuartetCollection,
                 path_point_selector: PathPointSelector):
        self.control_point_quartet_collection = control_point_quartet_collection
        self.path_point_selector = path_point_selector

    def move_control_handler(self, control_point_handler: ControlPointHandler, x: int, y: int):
        dx = self.control_point_quartet_collection.get_control_point(control_point_handler).x - x
        dy = self.control_point_quartet_collection.get_control_point(control_point_handler).y - y

        self.control_point_quartet_collection.get_control_point(control_point_handler).x = x
        self.control_point_quartet_collection.get_control_point(control_point_handler).y = y

        if self.path_point_selector.is_path_point(control_point_handler):
            related_path_point = self.path_point_selector.find_related_path_point(control_point_handler)
            self.control_point_quartet_collection.get_control_point(related_path_point).x = x
            self.control_point_quartet_collection.get_control_point(related_path_point).y = y

            related_control_points = self.path_point_selector.find_control_points_of_path_point(control_point_handler)
            self.control_point_quartet_collection.get_control_point(related_control_points[0]).x -= dx
            self.control_point_quartet_collection.get_control_point(related_control_points[0]).y -= dy
            self.control_point_quartet_collection.get_control_point(related_control_points[1]).x -= dx
            self.control_point_quartet_collection.get_control_point(related_control_points[1]).y -= dy

        else:
            related_control_point = self.path_point_selector.find_related_control_point(control_point_handler)
            related_path_point = self.path_point_selector.find_path_point_of_control_point(control_point_handler)

            xDistance = self.control_point_quartet_collection.get_control_point(related_path_point).x - x
            yDistance = self.control_point_quartet_collection.get_control_point(related_path_point).y - y

            self.control_point_quartet_collection.get_control_point(related_control_point).x = self.control_point_quartet_collection.get_control_point(related_path_point).x + xDistance
            self.control_point_quartet_collection.get_control_point(related_control_point).y = self.control_point_quartet_collection.get_control_point(related_path_point).y + yDistance


    def align_all(self):
        for quartet_index in range(self.control_point_quartet_collection.number_of_quartets()):
            quartet = self.control_point_quartet_collection.get_quartet(quartet_index)
            for point_index in range(4):
                control_point_handler = ControlPointHandler(quartet_index, point_index)
                point = quartet.get_point(point_index)
                self.move_control_handler(control_point_handler, point.x, point.y)
