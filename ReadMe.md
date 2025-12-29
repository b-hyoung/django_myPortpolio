# 🏗️ [2단계] 내 컴퓨터에 **나만의 블로그** 짓기 (Django 실습 기본틀)

> 목표: Django로 학업/취미 기록 블로그 만들기
> 
> 
> 구성: `mysite(총괄)` + `blog(블로그 기능)` + `pages(소개/연락 페이지)`
> 
> 배포(Render/Neon)는 선택
> 

---

## ✅ 0. Django 구조 먼저 이해하기 (중요)

Django는 “역할 분리”가 핵심.

- **Project (mysite)**: 사이트 전체 설정(총괄)
    - `settings.py` : 전체 설정(앱 등록, DB, static 등)
    - `urls.py` : 전체 URL(루트에서 어떤 앱으로 보낼지)
    - `wsgi.py / asgi.py` : 배포/서버 실행 입구
- **App (blog, pages …)**: 기능 단위
    - `models.py` : 데이터 설계(엑셀 표)
    - `views.py` : 로직(무엇을 보여줄지)
    - `templates/` : 화면(HTML)
    - `urls.py` : 앱 내부 주소 관리
    - `admin.py` : 관리자 사이트 설정

✅ 결론

- “전체 설정”은 `mysite`
- “블로그 기능”은 `blog`
- “소개/연락 페이지”는 `pages`

---

## 1) 장고 설치 및 프로젝트 생성

### ✅ 설치

```bash
pip install django

```

### ✅ 프로젝트 생성 (끝에 점(.) 중요)

```bash
django-admin startproject mysite .

```

### ✅ 서버 실행

```bash
python manage.py runserver

```

---

## 2) 앱 만들기 (blog 앱)

### ✅ blog 앱 생성

```bash
python manage.py startapp blog

```

### ✅ settings.py에 blog 등록

📌 파일: `mysite/settings.py`

```python
INSTALLED_APPS = [
# ...
"blog",
]

```

---

## 3) 데이터베이스 설계 (Models.py)

> “엑셀 표 만든다” 생각하면 이해 쉬움
> 

📌 파일: `blog/models.py`

```python
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # 여기!

    def __str__(self):
        return self.title

```

### ✅ 모델 변경 후 필수 명령 2개 (외우기)

```bash
python manage.py makemigrations
python manage.py migrate

```

✅ 자주 나오는 오류

- `OperationalError: no such table: blog_post`
    - 원인: migrate 안 함
    - 해결: `makemigrations` + `migrate`

---

## 4) 관리자 페이지(Admin) 사용하기

### ✅ 관리자 계정 만들기

```bash
python manage.py createsuperuser

```

### ✅ 관리자에서 Post 보이게 등록

📌 파일: `blog/admin.py`

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)

```

### ✅ 접속

- `http://127.0.0.1:8000/admin`

📌 비밀번호 잊으면?

- 새 관리자 만들기: `python manage.py createsuperuser`

---

## 5) 화면 보여주기 (Views & Templates)

### A) View 만들기 (글 목록)

📌 파일: `blog/views.py`

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})

```

### B) URL 연결하기 (가장 쉬운 방식)

📌 파일: `mysite/urls.py`

```python
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.post_list, name="post_list"),
]

```

### C) HTML 만들기 (템플릿)

📌 경로(중요): `blog/templates/blog/post_list.html`

초기 버전(디자인 전):

```html
<h1>나만의 블로그</h1>

{% for post in posts %}
<div>
<h2>{{ post.title }}</h2>
<p>{{ post.created_at }}</p>
<p>{{ post.content }}</p>
<hr>
</div>
{% endfor %}

```

✅ 핵심 문법

- `{% for %}` : 반복문 같은 “동작”
- `{{ }}` : 값 출력

---

# 🎨 6) 디자인 적용 (Bootstrap CDN 방식 + 테마 교체 가능)

> CSS를 직접 다 만들지 않고, Bootstrap이 제공하는 “디자인 부품”을 class로 조합하는 방식
> 

## ✅ 6-1) base.html 만들기 (공통 레이아웃)

📌 파일: `blog/templates/blog/base.html`

> 아래에서 CSS 링크 1줄이 “디자인 스위치”
> 
> 
> 다른 Bootstrap 테마로 바꾸려면 이 한 줄만 바꾸면 됨(주석 참고).
> 

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- ✅ [디자인 스위치] 기본 Bootstrap (현재 사용) -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <title>{% block title %}나만의 블로그{% endblock %}</title>
</head>

<body class="bg-light">

<nav class="navbar navbar-expand-lg bg-white border-bottom">
  <div class="container py-2">
    <a class="navbar-brand fw-bold" href="{% url 'post_list' %}">나만의 블로그</a>

    <div class="ms-auto d-flex gap-2">
      <a class="btn btn-outline-dark btn-sm" href="{% url 'post_list' %}">Home</a>
      <a class="btn btn-dark btn-sm" href="/admin/">Admin</a>
    </div>
  </div>
</nav>

<main class="container py-4">
  {% block content %}{% endblock %}
</main>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

```

## ✅ 6-2) post_list.html을 base.html 상속으로 변경(디자인 적용)

📌 파일: `blog/templates/blog/post_list.html`

```html
{% extends "blog/base.html" %}
{% block title %}글 목록 - 나만의 블로그{% endblock %}

{% block content %}
<h1class="h3 mb-3">글 목록</h1>

{% for post in posts %}
<divclass="card mb-3 shadow-sm">
<divclass="card-body">
<h2class="h5">{{ post.title }}</h2>
<pclass="text-muted small mb-2">{{ post.created_at }}</p>
<pclass="mb-0">{{ post.content|linebreaks }}</p>
</div>
</div>
{% empty %}
<divclass="alert alert-info">아직 글이 없어요. /admin에서 글을 작성해보자!</div>
{% endfor %}
{% endblock %}

```

---

## ✅ 6-3) “다른 Bootstrap 디자인(테마)” 예시 + 참고 링크

### A) Bootswatch (CSS 링크만 바꿔서 분위기 변경)

- **Litera / Journal**: 글 가독성 좋은 문서/학업 노트 느낌
- **Darkly / Cyborg / Slate**: 다크모드(개발자/테크 블로그 느낌)
- **Flatly / Lux / Yeti**: 깔끔하고 미니멀한 느낌
- **Sketchy**: 손그림 같은 개성(취미/가벼운 블로그)

📎 참고 링크(학생용)

- Bootswatch 테마 목록: `https://bootswatch.com/`
- Bootswatch CDN 링크 모음: `https://cdnjs.com/libraries/bootswatch`

### B) Bootstrap 공식 Examples (완성 레이아웃 참고)

- 레이아웃 예시를 보고 블로그 형태로 바꾸기 좋음
    
    📎 `https://getbootstrap.com/docs/5.3/examples/`
    

### C) Start Bootstrap 템플릿 (블로그 형태가 거의 완성)

- **Clean Blog**: 개인 블로그 느낌이 확 살아나는 유명 테마
    
    📎 `https://startbootstrap.com/theme/clean-blog`
    
    📎 소스: `https://github.com/StartBootstrap/startbootstrap-clean-blog`
    

---

# 🧾 7) 소개 페이지 앱(pages) 추가하기 (About/Contact)

## ✅ pages 앱 생성

```bash
python manage.py startapp pages

```

## ✅ settings.py 등록

📌 `mysite/settings.py`

```python
INSTALLED_APPS = [
# ...
"blog",
"pages",
]

```

## ✅ pages/views.py

📌 `pages/views.py`

```python
from django.shortcuts import render

def about(request):
    return render(request,"pages/about.html")

def contact(request):
    return render(request,"pages/contact.html")

```

## ✅ pages/urls.py (새 파일)

📌 `pages/urls.py`

```python
from django.urls import path
from .import views

urlpatterns = [
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]

```

## ✅ mysite/urls.py에 연결

📌 `mysite/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),# /about, /contact
    path("", views.post_list, name="post_list"),# /
]

```

## ✅ 템플릿 만들기

- `pages/templates/pages/about.html`
- `pages/templates/pages/contact.html`

## ✅ `pages/templates/pages/about.html` 예시 (Bootstrap 적용, base.html 상속)

```html
{% extends "blog/base.html" %}
{% block title %}About - 나만의 블로그{% endblock %}

{% block content %}
<h1class="h3 mb-3">소개</h1>
<divclass="card shadow-sm">
<divclass="card-body">
<p>여기에 내 소개를 적어보자!</p>
</div>
</div>
{% endblock %}
```

## ✅ `pages/templates/pages/contact.html` 예시 (Bootstrap 적용, base.html 상속)

```html
{% extends "blog/base.html" %}
{% block title %}Contact - 나만의 블로그{% endblock %}

{% block content %}
<divclass="row justify-content-center">
<divclass="col-lg-8">

<h1class="h3 mb-3">Contact</h1>

<divclass="card shadow-sm">
<divclass="card-body">
<pclass="text-muted mb-4">
          블로그에 대한 문의나 피드백은 아래로 연락해 주세요.
</p>

<ulclass="list-group">
<liclass="list-group-item">
<strong>Email:</strong> your_email@example.com
</li>
<liclass="list-group-item">
<strong>GitHub:</strong>
<ahref="https://github.com/yourname"target="_blank">https://github.com/yourname</a>
</li>
<liclass="list-group-item">
<strong>Instagram(선택):</strong>
<ahref="https://instagram.com/yourname"target="_blank">https://instagram.com/yourname</a>
</li>
</ul>

<divclass="mt-3">
<aclass="btn btn-outline-secondary btn-sm"href="{% url 'post_list' %}">← Home</a>
</div>
</div>
</div>

</div>
</div>
{% endblock %}

```

📌 파일: `blog/templates/blog/base.html`

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- ✅ [디자인 스위치] 기본 Bootstrap (현재 사용) -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <title>{% block title %}나만의 블로그{% endblock %}</title>
</head>

<body class="bg-light">

<nav class="navbar navbar-expand-lg bg-white border-bottom">
  <div class="container py-2">
    <a class="navbar-brand fw-bold" href="{% url 'post_list' %}">나만의 블로그</a>

    <div class="ms-auto d-flex gap-2">
      <a class="btn btn-outline-dark btn-sm" href="{% url 'post_list' %}">Home</a>
      <a class="btn btn-outline-dark btn-sm" href="{% url 'about' %}">About</a>
      <a class="btn btn-outline-dark btn-sm" href="{% url 'contact' %}">Contact</a>
      <a class="btn btn-dark btn-sm" href="/admin/">Admin</a>
    </div>
  </div>
</nav>

<main class="container py-4">
  {% block content %}{% endblock %}
</main>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

```

디자인 추가됨.

📌 파일: `blog/templates/blog/base.html`

```jsx
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <!-- Bootstrap -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- Bootstrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

  <title>{% block title %}나만의 블로그{% endblock %}</title>

  <style>
    /* 가볍게 분위기 업 */
    .hero {
      background: linear-gradient(135deg, rgba(13,110,253,.12), rgba(25,135,84,.10));
      border: 1px solid rgba(0,0,0,.06);
    }
    .hover-lift {
      transition: transform .15s ease, box-shadow .15s ease;
    }
    .hover-lift:hover {
      transform: translateY(-2px);
      box-shadow: 0 .5rem 1rem rgba(0,0,0,.08);
    }
    .text-truncate-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>
</head>

<body class="bg-light">

<!-- Top Nav -->
<nav class="navbar navbar-expand-lg bg-white border-bottom sticky-top">
  <div class="container py-2">
    <a class="navbar-brand fw-bold d-flex align-items-center gap-2" href="{% url 'post_list' %}">
      <i class="bi bi-journal-richtext"></i>
      <span>나만의 블로그</span>
    </a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#topNav">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="topNav">
      <!-- Left menu -->
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link" href="{% url 'post_list' %}"><i class="bi bi-house"></i> Home</a>
        </li>
        <!-- pages 앱 만들기 전이면 아래 2줄은 주석 처리하세요 -->
        <li class="nav-item">
          <a class="nav-link" href="{% url 'about' %}"><i class="bi bi-info-circle"></i> About</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'contact' %}"><i class="bi bi-chat-dots"></i> Contact</a>
        </li>
      </ul>

      <!-- Search (동작은 나중에 추가) -->
      <form class="d-flex me-lg-2 my-2 my-lg-0" role="search" method="get" action="">
        <input class="form-control form-control-sm" type="search" name="q" placeholder="검색어 입력…" aria-label="Search">
        <button class="btn btn-outline-primary btn-sm ms-2" type="submit">
          <i class="bi bi-search"></i>
        </button>
      </form>

      <!-- Right buttons -->
      <div class="d-flex gap-2">
        <a class="btn btn-outline-dark btn-sm" href="/admin/">
          <i class="bi bi-shield-lock"></i> Admin
        </a>
      </div>
    </div>
  </div>
</nav>

<!-- Hero -->
<header class="container py-4">
  <div class="hero rounded-4 p-4 p-md-5 hover-lift">
    <div class="row align-items-center g-3">
      <div class="col-md-8">
        <h1 class="display-6 fw-bold mb-2">오늘의 기록을 쌓는 블로그</h1>
        <p class="text-secondary mb-3">
          공부한 내용, 프로젝트 진행, 일상 메모를 보기 좋게 정리해보자.
          글은 <span class="fw-semibold">/admin</span>에서 작성할 수 있어요.
        </p>
        <div class="d-flex flex-wrap gap-2">
          <a class="btn btn-primary" href="{% url 'post_list' %}">
            <i class="bi bi-list-ul"></i> 글 목록 보기
          </a>
          <a class="btn btn-outline-success" href="/admin/blog/post/add/">
            <i class="bi bi-plus-circle"></i> 새 글 작성
          </a>
        </div>
      </div>

      <div class="col-md-4">
        <div class="bg-white rounded-4 p-3 border">
          <div class="d-flex align-items-center gap-3">
            <div class="rounded-circle bg-primary-subtle d-flex align-items-center justify-content-center" style="width:52px;height:52px;">
              <i class="bi bi-person-fill text-primary fs-4"></i>
            </div>
            <div>
              <div class="fw-bold">작성자</div>
              <div class="text-secondary small">나만의 블로그 운영자</div>
            </div>
          </div>
          <hr class="my-3">
          <div class="d-flex gap-2">
            <span class="badge text-bg-primary">Python</span>
            <span class="badge text-bg-success">Django</span>
            <span class="badge text-bg-warning">Study</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>

<!-- Main layout -->
<main class="container pb-5">
  <div class="row g-4">
    <!-- Content -->
    <section class="col-lg-8">
      {% block content %}{% endblock %}
    </section>

    <!-- Sidebar -->
    <aside class="col-lg-4">
      <!-- Profile card -->
      <div class="card shadow-sm hover-lift mb-3">
        <div class="card-body">
          <h5 class="card-title mb-2"><i class="bi bi-stars"></i> 한 줄 소개</h5>
          <p class="text-secondary mb-0">
            오늘 배운 걸 내일의 나에게 남기는 공간.
          </p>
        </div>
      </div>

      <!-- Categories -->
      <div class="card shadow-sm hover-lift mb-3">
        <div class="card-body">
          <h6 class="fw-bold mb-3"><i class="bi bi-folder2-open"></i> 카테고리</h6>
          <div class="d-flex flex-wrap gap-2">
            <a class="btn btn-outline-secondary btn-sm" href="#">Django</a>
            <a class="btn btn-outline-secondary btn-sm" href="#">Python</a>
            <a class="btn btn-outline-secondary btn-sm" href="#">Linux</a>
            <a class="btn btn-outline-secondary btn-sm" href="#">Project</a>
          </div>
          <div class="text-secondary small mt-2">
            (나중에 DB로 연결해서 진짜 카테고리로 만들 수 있어요)
          </div>
        </div>
      </div>

      <!-- Recent posts (임시 UI: 실제 최근글은 context로 연결 필요) -->
      <div class="card shadow-sm hover-lift mb-3">
        <div class="card-body">
          <h6 class="fw-bold mb-3"><i class="bi bi-clock-history"></i> 최근 글</h6>

          <!-- 나중에 base에 posts를 넘겨주면 for문으로 바꾸면 됨 -->
          <div class="list-group list-group-flush">
            <a href="#" class="list-group-item list-group-item-action">
              <div class="fw-semibold text-truncate">최근 글 예시 제목 1</div>
              <div class="text-secondary small text-truncate-2">짧은 미리보기 내용이 들어갑니다…</div>
            </a>
            <a href="#" class="list-group-item list-group-item-action">
              <div class="fw-semibold text-truncate">최근 글 예시 제목 2</div>
              <div class="text-secondary small text-truncate-2">짧은 미리보기 내용이 들어갑니다…</div>
            </a>
          </div>
        </div>
      </div>

      <!-- Tip box -->
      <div class="alert alert-info shadow-sm hover-lift mb-0">
        <div class="fw-bold mb-1"><i class="bi bi-lightbulb"></i> TIP</div>
        <div class="small">
          관리자 페이지에서 글을 작성한 뒤, 메인에서 목록을 확인해보세요.
        </div>
      </div>
    </aside>
  </div>
</main>

<footer class="border-top bg-white">
  <div class="container py-4 d-flex flex-column flex-md-row justify-content-between gap-2">
    <div class="text-secondary small">© {% now "Y" %} 나만의 블로그</div>
    <div class="text-secondary small">
      Made with Django + Bootstrap
    </div>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

```
지금 이게 내가 파이썬 장고로 진행하고있는 프로젝트야 내용파악해서 다른페이지를 추가했을때 비슷한형태로 