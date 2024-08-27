import cv2

''' Drawing boxes and annotate detected objects
    Called by execute_detection_model() '''
def draw_box(frame, result, class_list):
    xyxy = result.boxes.xyxy.numpy()
    confidence = result.boxes.conf.numpy()
    class_id = result.boxes.cls.numpy().astype(int)
    class_name = [class_list[x] for x in class_id]
    sum_output = list(zip(class_name, confidence, xyxy))

    out_image = frame.copy()
    for run_output in sum_output:
        label, con, box = run_output
        box_color = (0, 0, 255)
        text_color = (255, 255, 255)
        first_half_box = (int(box[0]), int(box[1]))
        second_half_box= (int(box[2]), int(box[3]))
        cv2.rectangle(out_image, first_half_box, second_half_box, box_color, 2)
        text_print = '{label} {con:.2f}'.format(label=label, con=con)
        text_location = (int(box[0]), int(box[1] - 10))
        label_size, base_line = cv2.getTextSize(text_print, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.rectangle(out_image,
                      (int(box[0]), int(box[1] - label_size[1] - 10)),
                      (int(box[0]) + label_size[0], int(box[1] + base_line - 10)),
                      box_color, cv2.FILLED)
        cv2.putText(out_image, text_print, text_location, cv2.FONT_HERSHEY_SIMPLEX, 1,
                    text_color, 2, cv2.FILLED)
    return out_image

''' Detection mode execution '''
def execute_detection_model(model, frame, selected_class):
    # class_list = model.model.names
    class_list = model.model.names
    results = model.predict(frame, classes=selected_class)
    labeled_img = draw_box(frame, results[0], class_list)
    return labeled_img

''' Tracking mode execution '''
def execute_tracking_mode(model, frame, selected_classes):
    results = model.track(frame, persist=True, classes=selected_classes)
    annotated_frame = results[0].plot()
    # cv2.imshow("POSENET", annotated_frame)
    return annotated_frame

''' Pose-estimation mode execution '''
def execute_pose_mode(model, frame):
    results = model(frame)
    annotated_frame = results[0].plot()
    # cv2.imshow("POSENET", annotated_frame)
    return annotated_frame

''' Can be implemented in the future: classification mode, segmentation mode '''
def execute_classification_model(model, frame):
    pass

def execute_segmentation_model(model, frame):
    pass