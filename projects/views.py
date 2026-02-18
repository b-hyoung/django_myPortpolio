from django.shortcuts import render, get_object_or_404
from .models import Project


PROJECT_DETAIL_META = {
    "Eternal Return 전적 검색 서비스 최적화": {
        "view_mode": "impact",
        "one_liner": "반복 조회 구간 캐싱 구조 도입을 통한 성능 및 안정성 개선 프로젝트.",
        "period": "2025.07 - 2025.08",
        "role": "백엔드 개발",
        "contribution": "100%",
        "my_role_points": [
            "전적 조회 API 및 캐시 적용 구간 직접 구현",
            "Redis 키 전략 및 만료 정책 설계",
            "Nginx/Docker 배포 구성 및 운영 점검",
        ],
        "triple_title": "문제 / 해결 / 결과",
        "triple_sections": [
            {
                "label": "문제",
                "points": [
                    "반복 전적 조회 요청 집중으로 인한 DB I/O 부하 누적",
                    "피크 시간대 API 응답 지연",
                ],
            },
            {
                "label": "해결",
                "points": [
                    "Redis 인메모리 캐시 계층 도입",
                    "Nginx Reverse Proxy 및 Docker 배포 표준화",
                    "외부 API 변경 대응용 파싱 모듈 분리",
                ],
            },
            {
                "label": "결과",
                "points": [
                    "API 응답 시간 약 20% 단축",
                    "DB 부하 완화 및 운영 안정성 개선",
                ],
            },
        ],
        "kpi_title": "성과 지표",
        "metrics": [
            {"label": "응답 시간", "value": "-20%", "note": "반복 조회 구간 기준"},
            {"label": "운영 안정성", "value": "개선", "note": "트래픽 분산 구성 적용"},
        ],
    },
    "KUMAMID (한국영상대 졸업작품전 웹사이트)": {
        "view_mode": "impact",
        "one_liner": "렌더링 전략 전환과 콘텐츠 구조 개선을 통한 초기 로딩 성능 최적화 프로젝트.",
        "period": "2025.05 - 2025.07",
        "role": "프론트엔드 개발 (2인 팀)",
        "contribution": "50%",
        "my_role_points": [
            "프론트엔드 구조 설계 및 핵심 화면 구현 담당",
            "초기 렌더링 구조 CSR -> SSR 전환 작업 수행",
            "이미지 로딩 전략 및 반응형 UI 최적화 적용",
        ],
        "writeup_link": "https://kimbob-world.tistory.com/33",
        "triple_title": "문제 / 해결 / 결과",
        "triple_sections": [
            {
                "label": "문제",
                "points": [
                    "CSR 중심 구조로 인한 초기 렌더링 지연",
                    "정적 하드코딩 기반 콘텐츠 운영 비효율",
                ],
            },
            {
                "label": "해결",
                "points": [
                    "초기 레이아웃 SSR 중심 구조 전환",
                    "썸네일 우선 이미지 로딩 전략 적용",
                    "JSON/DB 기반 자동 렌더링 구조 리팩토링",
                ],
            },
            {
                "label": "결과",
                "points": [
                    "LCP 3초대에서 1초 내외로 단축",
                    "콘텐츠 추가·수정 시 운영 효율 개선",
                ],
            },
        ],
        "kpi_title": "성과 지표",
        "metrics": [
            {"label": "LCP", "value": "-66%", "note": "3초대 -> 1초 내외"},
            {"label": "운영 효율", "value": "개선", "note": "데이터 기반 렌더링 전환"},
        ],
    },
    "개인 포트폴리오 및 블로그 서비스": {
        "view_mode": "service",
        "one_liner": "콘텐츠 기록, 프로젝트 소개, AI 질의 기능을 통합한 개인 브랜딩형 서비스.",
        "period": "2025.12 - 2026.02",
        "role": "풀스택 개발",
        "contribution": "100%",
        "my_role_points": [
            "서비스 기획, 백엔드, 프론트엔드, 배포 전 과정을 단독 수행",
            "프로젝트/블로그/AI 검색 기능 통합 아키텍처 구성",
            "운영 링크 관리 및 콘텐츠 구조 설계",
        ],
        "triple_title": "서비스 구조",
        "triple_sections": [
            {
                "label": "서비스 개요",
                "points": [
                    "개인 포트폴리오와 기술 블로그를 단일 서비스로 통합",
                    "프로젝트 중심 정보 구조와 글 중심 기록 구조 병행",
                ],
            },
            {
                "label": "핵심 기능",
                "points": [
                    "프로젝트 리스트/상세 및 기술 스택 시각화",
                    "블로그·노트 기반 지식 기록 및 검색",
                    "AI Search 기반 포트폴리오 질의응답",
                ],
            },
            {
                "label": "사용자 가치",
                "points": [
                    "개발 경험과 결과물을 한 화면 흐름으로 파악 가능",
                    "채용·협업 상황에서 정보 전달 속도 향상",
                ],
            },
        ],
        "kpi_title": "서비스 포지션",
        "metrics": [
            {"label": "대상 사용자", "value": "채용/협업 관계자", "note": "개발 역량 검토 목적"},
            {"label": "서비스 유형", "value": "브랜딩/기록형", "note": "포트폴리오 + 블로그 + AI"},
        ],
    },
    "Travel-JC (전주 외국인 안내 키오스크)": {
        "view_mode": "service",
        "one_liner": "외국인 사용자의 지역 정보 접근성을 개선하기 위한 키오스크형 안내 서비스.",
        "period": "2026.01 - 2026.02",
        "role": "서비스 개발",
        "contribution": "100%",
        "my_role_points": [
            "키오스크 UI 흐름 및 데이터 조회 구조 직접 구현",
            "장소 데이터 모델 정리 및 SQLite 연동 처리",
            "GUI(Python)와 Django 서비스 구조 연결 설계",
        ],
        "triple_title": "서비스 구조",
        "triple_sections": [
            {
                "label": "서비스 개요",
                "points": [
                    "전주 지역 장소 정보를 다국어로 제공하는 안내형 서비스",
                    "키오스크 UX 기반 탐색 흐름 설계",
                ],
            },
            {
                "label": "핵심 기능",
                "points": [
                    "장소 목록/상세 조회와 이미지 기반 정보 탐색",
                    "SQLite 기반 장소 데이터 조회 및 카테고리 구성",
                    "GUI(Python)와 Django 백엔드 혼합 구조",
                ],
            },
            {
                "label": "사용자 가치",
                "points": [
                    "언어 장벽 상황에서 지역 정보 접근성 향상",
                    "현장 안내 시나리오에 맞는 빠른 정보 탐색 제공",
                ],
            },
        ],
        "kpi_title": "서비스 포지션",
        "metrics": [
            {"label": "대상 사용자", "value": "전주 방문 외국인", "note": "현장 안내/탐색 목적"},
            {"label": "서비스 형태", "value": "키오스크형 안내", "note": "GUI + 데이터 조회 구조"},
        ],
    },
    "kkeua (끝말잇기 아이템전)": {
        "view_mode": "service",
        "one_liner": "실시간 멀티플레이와 아이템 규칙을 결합한 단어 게임 서비스.",
        "period": "2025.03 - 2025.04",
        "role": "프론트엔드 개발 (팀 프로젝트)",
        "contribution": "프론트엔드 담당",
        "my_role_points": [
            "React 기반 게임 화면 및 사용자 인터랙션 구현",
            "실시간 상태 반영 UI와 게임 흐름 화면 구성",
            "반응형 레이아웃 및 UX 동선 정리",
        ],
        "triple_title": "서비스 구조",
        "triple_sections": [
            {
                "label": "서비스 개요",
                "points": [
                    "아이템 요소가 포함된 실시간 끝말잇기 게임",
                    "멀티플레이 기반 세션 참여형 서비스",
                ],
            },
            {
                "label": "핵심 기능",
                "points": [
                    "WebSocket 기반 실시간 게임 인터페이스",
                    "로비/게임 플로우 분리 구조",
                    "React + TailwindCSS 기반 반응형 UI",
                ],
            },
            {
                "label": "사용자 가치",
                "points": [
                    "단순 단어 게임 대비 상호작용 요소 강화",
                    "실시간 참여 경험 중심의 몰입도 향상",
                ],
            },
        ],
        "kpi_title": "서비스 포지션",
        "metrics": [
            {"label": "대상 사용자", "value": "실시간 게임 이용자", "note": "캐주얼 멀티플레이 목적"},
            {"label": "서비스 형태", "value": "실시간 단어 게임", "note": "아이템 기반 규칙 확장"},
        ],
    },
    "Ai_serbot-project (AI 로봇 원격 제어)": {
        "view_mode": "service",
        "one_liner": "재난 탐사 시나리오용 로봇 제어와 현장 모니터링을 통합한 관제 서비스.",
        "period": "2025.12 - 2025.12",
        "role": "서비스 개발",
        "contribution": "팀 프로젝트",
        "my_role_points": [
            "관제 시나리오 기준 화면 흐름 및 기능 요구 정리",
            "원격 제어/모니터링 기능 연계 구간 개발 참여",
            "실행 절차 문서화 및 운영 테스트 지원",
        ],
        "triple_title": "서비스 구조",
        "triple_sections": [
            {
                "label": "서비스 개요",
                "points": [
                    "재난 현장 선진입 로봇을 원격 제어하는 통합 관제 시스템",
                    "데스크톱 기반 제어/모니터링 환경 구성",
                ],
            },
            {
                "label": "핵심 기능",
                "points": [
                    "TCP 소켓 기반 원격 제어 흐름",
                    "센서 데이터·영상 정보 실시간 모니터링",
                    "운용 기록 기반 사후 분석 구조",
                ],
            },
            {
                "label": "사용자 가치",
                "points": [
                    "위험 구간 선탐사 지원을 통한 현장 안전성 보조",
                    "관제 인력의 상황 인지 속도 향상",
                ],
            },
        ],
        "kpi_title": "서비스 포지션",
        "metrics": [
            {"label": "대상 사용자", "value": "재난 대응 관제 인력", "note": "원격 제어/상황 판단 목적"},
            {"label": "서비스 형태", "value": "통합 관제형", "note": "제어 + 모니터링 + 기록"},
        ],
    },
}


TECH_PURPOSES = {
    "python": "핵심 비즈니스 로직 구현",
    "django": "웹 백엔드 및 API 계층 구성",
    "redis": "반복 조회 구간 캐싱 최적화",
    "docker": "배포 환경 표준화",
    "nginx": "Reverse Proxy 및 요청 분산",
    "next.js": "SSR 기반 초기 렌더링 최적화",
    "nextjs": "SSR 기반 초기 렌더링 최적화",
    "typescript": "정적 타입 기반 안정성 확보",
    "firebase": "백엔드 서비스 및 데이터 연동",
    "tailwindcss": "반응형 UI 구현",
    "react": "컴포넌트 중심 UI 구성",
    "mysql": "관계형 데이터 저장",
    "aws": "인프라 운영 및 리소스 관리",
    "zustand": "인증 상태 중앙 관리",
    "java": "서비스 로직 구현",
    "sqlite": "경량 데이터 저장",
    "bootstrap": "반응형 UI 구성",
    "socket": "실시간 이벤트 처리",
    "sensor": "현장 데이터 수집 요소",
    "monitoring": "상태 관찰 및 시각화",
    "ai": "지능형 처리 기능 구성",
}


def _split_technologies(raw):
    if not isinstance(raw, str):
        return []
    normalized = raw.replace("\r\n", "\n").replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def project_list(request):
    projects = Project.objects.order_by("-created_at")
    view_mode = request.GET.get("view", "cards")
    if view_mode not in {"cards", "rows", "bento", "case"}:
        view_mode = "cards"
    return render(
        request,
        "projects/project_list.html",
        {"projects": projects, "view_mode": view_mode, "project_meta": PROJECT_DETAIL_META},
    )


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    profile = PROJECT_DETAIL_META.get(
        project.title,
        {
            "view_mode": "service",
            "one_liner": "프로젝트 핵심 내용을 구조화하여 정리한 상세 페이지.",
            "period": "-",
            "role": "-",
            "contribution": "-",
            "my_role_points": [],
            "writeup_link": "",
            "triple_title": "서비스 구조",
            "triple_sections": [
                {"label": "서비스 개요", "points": project.description.splitlines() or ["설명 추가 예정"]},
                {"label": "핵심 기능", "points": ["기능 정보 추가 예정"]},
                {"label": "사용자 가치", "points": ["가치 정보 추가 예정"]},
            ],
            "kpi_title": "서비스 포지션",
            "metrics": [],
        },
    )

    stack_items = []
    for tech in _split_technologies(project.technologies):
        purpose = TECH_PURPOSES.get(tech.lower(), "적용 목적 정리 예정.")
        stack_items.append({"name": tech, "purpose": purpose})

    context = {
        "project": project,
        "profile": profile,
        "stack_items": stack_items,
        "hide_layout_elements": True,
    }
    return render(request, "projects/project_detail.html", context)
