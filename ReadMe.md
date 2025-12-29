# `b-hyoung/config.py`: About Me

> 이 문서는 개발자 **b-hyoung**의 생각과 기술 스택을 Django 프로젝트 구조에 빗대어 설명합니다.

---

## `settings.py`: The Core Philosophy

```python
# settings.py

"""
단순히 기능을 구현하는 것을 넘어, 
'왜 이렇게 동작해야 하는가?'에 대한 근본적인 고민을 즐깁니다.
코드를 통해 사용자에게 더 나은 경험을 제공하고, 
그 과정에서 얻은 성장의 경험과 고민을 기록하는 것을 중요하게 생각합니다.
"""

# Django의 심장인 settings.py처럼, 저의 개발 철학은 다음과 같습니다.
DEBUG = True  # 끊임없이 배우고, 스스로를 디버깅하며 성장합니다.
SECRET_KEY = "새로운_기술에_대한_강력한_호기심"
```

---

## `INSTALLED_APPS`: My Core Features

제가 현재 주력하고 있고, 앞으로 발전시켜 나갈 핵심 역량들입니다.

```python
INSTALLED_APPS = [
    'blog',          # 지식 기록 및 공유 (Documentation & Sharing)
    'projects',      # 아이디어의 현실화 (Building & Shipping)
    'pages',         # 나를 표현하는 공간 (Branding & Identity)
    'ai_search',     # 새로운 기술 탐구 (AI & Future Tech)
    'django.contrib.admin',  # 체계적인 관리 능력 (Systematic Management)
]
```

---

## The Architecture: How I Work

Django의 MTV 패턴처럼, 저는 다음과 같은 방식으로 문제를 해결하고 결과물을 만들어냅니다.

### 1. `models.py`: The Foundation (체계적인 설계)
> 모든 좋은 소프트웨어는 잘 설계된 데이터 모델에서 시작된다고 믿습니다. 문제의 본질을 파악하고, 명확하고 확장 가능한 데이터 구조를 설계하는 것을 가장 중요하게 생각합니다.

### 2. `views.py`: The Logic (논리적인 문제 해결)
> 설계된 구조 위에서, 비즈니스 로직을 효율적으로 구현합니다. 복잡한 문제를 단순한 단계로 나누고, Python과 Django의 강력한 기능들을 활용하여 깨끗하고 유지보수하기 좋은 코드를 작성하려 노력합니다.

### 3. `templates/`: The User Experience (사용자 중심의 경험)
> 아무리 뛰어난 로직도 사용자에게 잘 전달되지 않으면 의미가 없다고 생각합니다. 사용자의 입장에서 가장 편하고 직관적인 UI/UX를 고민하고, 인터랙티브한 웹 경험을 만드는 것에 큰 흥미를 느낍니다.

---

## `urls.py`: Let's Connect

저의 성장 과정과 결과물이 궁금하시다면, 아래 경로를 통해 확인하실 수 있습니다.

```python
from django.urls import path

urlpatterns = [
    path('blog/',       # 저의 학습과 고민의 기록들),
    path('projects/',   # 아이디어를 현실로 만든 결과물들),
    path('about/',      # 그리고, 저라는 사람에 대하여),
    path('contact/',    # 함께 나눌 이야기가 있다면),
]
```

감사합니다.