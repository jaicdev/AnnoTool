class ExportFormats:
    @staticmethod
    def export_to_coco(annotations, image_id, category_mapping):
        coco_annotations = []
        for i, anno in enumerate(annotations):
            coco_anno = {
                "image_id": image_id,
                "category_id": category_mapping.get(anno.get("class"), 0),
                "bbox": anno["coords"],
                "area": anno["coords"][2] * anno["coords"][3],
                "iscrowd": 0,
                "id": i
            }
            coco_annotations.append(coco_anno)
        return coco_annotations

    @staticmethod
    def export_to_pascal_voc(annotations):
        voc_annotations = []
        for anno in annotations:
            voc_annotations.append(
                f"<object><name>{anno.get('class', 'Unknown')}</name><bndbox>"
                f"<xmin>{anno['coords'][0]}</xmin>"
                f"<ymin>{anno['coords'][1]}</ymin>"
                f"<xmax>{anno['coords'][0] + anno['coords'][2]}</xmax>"
                f"<ymax>{anno['coords'][1] + anno['coords'][3]}</ymax>"
                f"</bndbox></object>"
            )
        return voc_annotations

    @staticmethod
    def export_to_yolo(annotations, image_width, image_height, class_mapping):
        yolo_annotations = []
        for anno in annotations:
            class_id = class_mapping.get(anno.get("class"), 0)
            x_center = (anno["coords"][0] + anno["coords"][2] / 2) / image_width
            y_center = (anno["coords"][1] + anno["coords"][3] / 2) / image_height
            width = anno["coords"][2] / image_width
            height = anno["coords"][3] / image_height
            yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        return yolo_annotations
