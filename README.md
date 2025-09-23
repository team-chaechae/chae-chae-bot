# 테스트셋 실행 환경 세팅 가이드

>macOS / Linux 기준)
---

## 1) 작업 디렉터리 이동
```bash
cd notebooks
```

## 2) 가상환경 생성 & 활성화
>원하는 가상환경 이름으로 바꿔 쓰세요. 예: .venv-notebook
```bash
python3 -m venv .venv-notebook
source .venv-notebook/bin/activate
```

>(선택) pip 최신화
```bash
python -m pip install --upgrade pip
```

## 3) 필수 패키지 설치
```bash
python -m pip install -r requirements/requirements.txt
```
```bash
pip install --no-deps krag
```

## 4) Jupyter 커널 등록 (ipykernel)
```bash
python -m ipykernel install --user --name .venv-notebook --display-name "Python (.venv-notebook)"
```

## 5) 노트북에서 커널 선택
- JupyterLab / Notebook: 상단 메뉴 Kernel → Change Kernel 에서 “Python (.venv-notebook)” 선택
- VS Code: 우측 상단 커널 선택기에서 “Python (.venv-notebook)” 선택
