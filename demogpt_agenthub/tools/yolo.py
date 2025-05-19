from collections import defaultdict
from demogpt_agenthub.tools.base import BaseTool
from ultralytics import YOLO

class YoloTool(BaseTool):
    def __init__(self):
        self.model = YOLO("yolo11n.pt")
        super().__init__()
        self.name = "YOLO Object Detection"
        self.description = """A tool that can execute YOLO object detection by using the YOLO model.
        It returns a detailed description of the detected objects in the image.
        It gets the path of the image as an argument."""
        
    def run(self, path):
        results = self.model(path)[0]
        boxes = results.boxes
        names = results.names
        classes = results.boxes.cls
        resulting_str = ""
        object2count = defaultdict(int)
        for box, cls in zip(boxes, classes):
            
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            _class = names[int(cls)]
            object2count[_class] += 1
            resulting_str += f"The {_class}[{object2count[_class]}] is from ({x1}, {y1}) to ({x2}, {y2}).\n"
        intro = ""
        for obj, count in object2count.items():
            intro += f"{count} {obj}, "
        intro = intro.strip(", ")
        if len(intro) > 0:
            intro = "There are " + intro + " in the image.\n"
        else:
            intro = "There are no objects in the image.\n"
        resulting_str = intro + resulting_str
        if len(resulting_str) > 0:
            resulting_str = "in the image.\n" + resulting_str
        return resulting_str
    
if __name__ == "__main__":
    tool = YoloTool()
    path = "/home/melih/Downloads/bus.jpg"
    print(tool.run(path))