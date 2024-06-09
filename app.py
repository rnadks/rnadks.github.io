from flask import Flask, render_template, request, jsonify
import librosa
import pyaudio

app = Flask(__name__) # 객체 생성성

# 오디오 입력 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()

# 튜닝 방식 설정
tuning_options = {
    "Standard": {
        "E2": 82.41,
        "A2": 110.00,
        "D3": 146.83,
        "G3": 196.00,
        "B3": 246.94,
        "E4": 329.63
    },
    "Half Step Down": {
        "E2": 77.78,
        "A2": 103.83,
        "D3": 138.59,
        "G3": 185.00,
        "B3": 233.08,
        "E4": 311.13
    },
    # ...
}

selected_tuning = "Standard" # 튜닝 방식 선택

# 스트림 열기
stream = audio.open(format=FORMAT, # PyAudio 스트림 객체 생성
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

@app.route("/", methods=["GET", "POST"]) # 메인 페이지 라우트 함수
def index():
    global selected_tuning
    if request.method == "POST":
        selected_tuning = request.form["tuning_select"] # 사용자가 선택한 튜닝 방식
    return render_template("index.html", tuning_options=tuning_options, selected_tuning=selected_tuning)

def find_pitch(data, sr): # 음높이를 찾는 함수
    pitches, _, _ = librosa.pyin(data, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('E4')) # Pyin 알고리즘을 사용하여 음높이 추출
    valid_pitches = [pitch for pitch in pitches if pitch is not None]
    pitch = sum(valid_pitches) / len(valid_pitches) if valid_pitches else None
    return pitch

@app.route("/tuning_results") # 튜닝 결과 페이지 라우트 함수
def tuning_results():
    data = stream.read(CHUNK, exception_on_overflow=False)
    data = librosa.util.buf_to_float(data, n_bytes=2, dtype='float32')
    pitch = find_pitch(data, RATE)

    tuning_errors = []
    if pitch:
        for string_name, tuning_freq in tuning_options[selected_tuning].items():
            tuning_error = pitch - tuning_freq
            tuning_errors.append((string_name, tuning_error))

    return jsonify(tuning_errors)

if __name__ == "__main__": # 스크립트 실행
    app.run(debug=True)
