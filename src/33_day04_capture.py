from pathlib import Path
import cv2


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

stream_url = "http://192.168.40.114:4747/video"

output_dir = Path("samples/day04/my_challenge")
output_dir.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# ROI 선택 상태
# --------------------------------------------------

drawing = False

start_x = 0
start_y = 0

end_x = 0
end_y = 0

roi_selected = False


# --------------------------------------------------
# 마우스로 ROI 선택
# --------------------------------------------------

def mouse_callback(event, x, y, flags, param):

    global drawing
    global start_x, start_y
    global end_x, end_y
    global roi_selected

    # 마우스 왼쪽 버튼을 누르면 시작점 기록
    if event == cv2.EVENT_LBUTTONDOWN:

        drawing = True

        start_x = x
        start_y = y

        end_x = x
        end_y = y

        roi_selected = False


    # 마우스를 움직이는 동안 영역 표시
    elif event == cv2.EVENT_MOUSEMOVE and drawing:

        end_x = x
        end_y = y


    # 마우스 버튼을 놓으면 ROI 확정
    elif event == cv2.EVENT_LBUTTONUP:

        drawing = False

        end_x = x
        end_y = y

        roi_selected = True

        print(
            "ROI 선택:",
            start_x,
            start_y,
            end_x,
            end_y
        )


# --------------------------------------------------
# 스마트폰 영상 연결
# --------------------------------------------------

cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    raise RuntimeError(
        "스마트폰 영상을 열 수 없습니다."
    )


window_name = "Phone Camera"

cv2.namedWindow(window_name)

cv2.setMouseCallback(
    window_name,
    mouse_callback
)


print()
print("===================================")
print("스마트폰 실시간 ROI 실습")
print("===================================")
print("마우스 드래그 : ROI 선택")
print("r            : ROI 다시 선택")
print("1 : 기준 정면 사진")
print("2 : 위치 이동 사진")
print("3 : 회전 사진")
print("4 : 거리 변화 사진")
print("5 : 기울기/반사 사진")
print("q / ESC      : 종료")
print("Ctrl + C     : 터미널에서 강제 종료")
print("===================================")
print()


try:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Frame을 읽을 수 없습니다.")
            break

        # 카메라 영상을 시계 방향으로 90도 회전
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)


        preview = frame.copy()


        # ------------------------------------------
        # ROI 선택 중
        # ------------------------------------------

        if drawing:

            cv2.rectangle(
                preview,
                (start_x, start_y),
                (end_x, end_y),
                (0, 255, 255),
                2
            )


        # ------------------------------------------
        # ROI가 선택된 경우
        # ------------------------------------------

        if roi_selected:

            x1 = min(start_x, end_x)
            y1 = min(start_y, end_y)

            x2 = max(start_x, end_x)
            y2 = max(start_y, end_y)


            # 전체 화면에 ROI 표시
            cv2.rectangle(
                preview,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )


            cv2.putText(
                preview,
                "CAP ROI",
                (x1, max(30, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


            # ROI 자르기
            roi = frame[y1:y2, x1:x2]


            if roi.size > 0:

                cv2.imshow(
                    "Cap ROI",
                    roi
                )


        # 전체 실시간 영상
        cv2.imshow(
            window_name,
            preview
        )


        # ------------------------------------------
        # 키 입력
        # ------------------------------------------

        key = cv2.waitKey(1) & 0xFF


        # q 또는 ESC → 종료
        if key == ord("q") or key == 27:
            print("프로그램을 종료합니다.")
            break


        # r → ROI 초기화
        elif key == ord("r"):

            roi_selected = False

            print("ROI를 다시 선택하세요.")

            try:
                cv2.destroyWindow("Cap ROI")
            except cv2.error:
                pass


                # 1~5 키로 4일차 사진 저장
        elif key in [ord("1"), ord("2"), ord("3"), ord("4"), ord("5")]:

            filenames = {
                ord("1"): "full_front.jpg",
                ord("2"): "shift.jpg",
                ord("3"): "rotate.jpg",
                ord("4"): "distance.jpg",
                ord("5"): "tilt_glare.jpg",
            }

            output_path = output_dir / filenames[key]

            # ROI가 아니라 전체 프레임 저장
            cv2.imwrite(str(output_path), frame)

            print("사진 저장:", output_path)


        # 창의 X 버튼으로 닫았는지도 확인
        try:

            if (
                cv2.getWindowProperty(
                    window_name,
                    cv2.WND_PROP_VISIBLE
                )
                < 1
            ):
                print("창이 닫혀 프로그램을 종료합니다.")
                break

        except cv2.error:
            break


# Ctrl + C 처리
except KeyboardInterrupt:

    print()
    print("Ctrl + C가 입력되었습니다.")
    print("프로그램을 종료합니다.")


# 어떤 상황에서도 자원 정리
finally:

    cap.release()

    cv2.destroyAllWindows()

    print("카메라 연결을 종료했습니다.")