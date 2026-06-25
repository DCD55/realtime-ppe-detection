from ultralytics import YOLO

def main():
    model = YOLO("yolo11n.pt")
    model.train(
        data="construction-ppe.yaml",
        epochs=15,
        imgsz=640,
        name="yolo11n-construction-ppe",
        project="runs/detect/train"
    )

if __name__ == "__main__":
    main()
