# 📘 서버/노트북 실행 가이드

## 목차

- [🚀 서버 가동 가이드](#server-run)
  - [1) 가상환경 활성화](#server-run-activate)
  - [2) API 서버 실행](#server-run-api)
  - [3) Redis Streams 워커 실행](#server-run-streams)
    - [(A) 퍼블리셔](#server-run-publisher)
    - [(B) 컨슈머](#server-run-consumer)
- [🧪 테스트셋 실행 환경 세팅 가이드 (macOS / Linux)](#notebook-setup)
  - [1) 작업 디렉터리 이동](#notebook-setup-cd)
  - [2) 가상환경 생성 & 활성화](#notebook-setup-venv)
  - [3) 필수 패키지 설치](#notebook-setup-reqs)
  - [4) Jupyter 커널 등록](#notebook-setup-kernel)
  - [5) 노트북에서 커널 선택](#notebook-setup-select)

---

<a id="server-run"></a>
## 🚀 서버 가동 가이드
> **루트 디렉터리 기준**  
> 서버/워커는 **각각 별도 터미널**에서 실행하며, 코드 변경 시 해당 터미널에서 재시작하세요.

<a id="server-run-activate"></a>
### 1) 가상환경 활성화
```bash
source .venv-notebook/bin/activate
```

<a id="server-run-api"></a>
### 2) API 서버 실행
```bash
uvicorn app.main:app --reload
```

<a id="server-run-streams"></a>
### 3) Redis Streams 워커 실행
> 퍼블리셔/컨슈머는 **별도 터미널**을 열어 각각 실행합니다. (둘 다 가상환경 활성화 필요)

<a id="server-run-publisher"></a>
#### (A) 퍼블리셔
```bash
# 새 터미널
source .venv/bin/activate
python -m app.runners.publisher
```

<a id="server-run-consumer"></a>
#### (B) 컨슈머
```bash
# 새 터미널
source .venv/bin/activate
python -m app.runners.consumer
```
> ℹ️ **참고**  
> - 변경 사항 반영을 위해 **각 터미널에서 재시작**하세요.

---

<a id="notebook-setup"></a>
## 🧪 테스트셋 실행 환경 세팅 가이드 (macOS / Linux)

<a id="notebook-setup-cd"></a>
### 1) 작업 디렉터리 이동
```bash
cd notebooks
```

<a id="notebook-setup-venv"></a>
### 2) 가상환경 생성 & 활성화
> 앞서 생성한 서버용 가상환경과 **별도**의 환경을 구성합니다.  
> 원하는 이름으로 바꿔 쓰세요 (예: `.venv-notebook`)
```bash
python3 -m venv .venv-notebook
source .venv-notebook/bin/activate
```

### (선택) pip 최신화
```bash
python -m pip install --upgrade pip
```

<a id="notebook-setup-reqs"></a>
### 3) 필수 패키지 설치
```bash
python -m pip install -r requirements/requirements.txt
```
```bash
pip install --no-deps krag
```

<a id="notebook-setup-kernel"></a>
### 4) Jupyter 커널 등록 (ipykernel)
```bash
python -m ipykernel install --user --name .venv-notebook --display-name "Python (.venv-notebook)"
```

<a id="notebook-setup-select"></a>
### 5) 노트북에서 커널 선택
- **JupyterLab / Notebook**: 상단 메뉴 `Kernel → Change Kernel` 에서 **Python (.venv-notebook)** 선택  
- **VS Code**: 우측 상단 커널 선택기에서 **Python (.venv-notebook)** 선택

---

### ✅ 운영 팁
- 서버/워커 로그는 각 실행 터미널에서 바로 확인하세요.  
- 장시간 실행 후 이슈가 생기면: `Ctrl+C`로 종료 → 가상환경 재활성화 → 재실행을 수행하세요.
