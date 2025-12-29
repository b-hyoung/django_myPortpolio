import json
import requests
import markdown
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from projects.models import Project

# --- Tech Name Mapping ---
TECH_MAP = {
    '파이썬': 'python', 'python': 'python',
    '장고': 'django', 'django': 'django',
    '리액트': 'react', 'react': 'react',
    '도커': 'docker', 'docker': 'docker',
    '자바스크립트': 'javascript', 'javascript': 'javascript',
    '자바': 'java', 'java': 'java',
    'mysql': 'mysql',
    'postgresql': 'postgresql',
}

def ai_search_view(request):
    """
    Renders the main AI chat interface page.
    """
    return render(request, 'ai_search/ai_search.html', {'hide_layout_elements': True})

def chat_interaction(request):
    """
    Handles conversational AJAX requests, integrating session-based context memory,
    interactive project filtering, and LLM fallback.
    """
    if request.method == 'POST':
        try:
            history = request.session.get('chat_history', [])
            data = json.loads(request.body)
            user_message = data.get('message', '').lower().strip()
            ai_response = {}
            simplified_ai_text = ''

            # 1. Analyze user message for tech keywords using TECH_MAP
            detected_techs = list(set([TECH_MAP[key] for key in TECH_MAP if key in user_message]))
            
            last_ai_response_text = history[-1]['ai'] if history else ''
            is_project_context = '[프로젝트]' in last_ai_response_text

            # 3. Determine action
            # Get all distinct technologies from visible projects for dynamic suggestions
            available_techs_in_visible_projects = set()
            for project in Project.objects.filter(is_visible=True):
                for tech_raw in project.technologies.split(','):
                    tech_en = tech_raw.strip().lower()
                    if tech_en in TECH_MAP.values(): # Check if it's a known tech
                        available_techs_in_visible_projects.add(tech_en)

            dynamic_project_suggestions = []
            if '모든 프로젝트 보기' not in user_message: # Avoid adding if user explicitly asked for all
                dynamic_project_suggestions.append('모든 프로젝트 보기')
            
            # Map back to Korean for display
            for tech_en in sorted(list(available_techs_in_visible_projects)):
                # Find the Korean name if available, otherwise use English
                # Prioritize Korean key if it maps to the tech_en
                tech_display = next((k for k, v in TECH_MAP.items() if v == tech_en and k != v), tech_en)
                dynamic_project_suggestions.append(f"{tech_display.capitalize()} 프로젝트만 보기")


            # Priority 1: Follow-up filtering
            if detected_techs and is_project_context:
                tech_to_filter = detected_techs[0]
                projects = Project.objects.filter(is_visible=True, technologies__iregex=fr'\b{tech_to_filter}\b').order_by('-created_at')
                if projects.exists():
                    ai_response = {'type': 'html', 'content': render_to_string('ai_search/_project_cards.html', {'projects': projects})}
                    ai_response['suggestions'] = dynamic_project_suggestions
                    simplified_ai_text = f"[{tech_to_filter} 프로젝트 목록 표시]"
                else:
                    ai_response = {'type': 'text', 'content': f"'{tech_to_filter}' 기술을 포함하는 프로젝트를 찾을 수 없습니다."}
            
            # Priority 2: Initial project request (with optional filter)
            elif '프로젝트' in user_message:
                projects_query = Project.objects.filter(is_visible=True)
                if detected_techs:
                    tech_to_filter = detected_techs[0]
                    projects = projects_query.filter(technologies__iregex=fr'\b{tech_to_filter}\b').order_by('-created_at')
                    if projects.exists():
                        ai_response = {'type': 'html', 'content': render_to_string('ai_search/_project_cards.html', {'projects': projects})}
                        ai_response['suggestions'] = dynamic_project_suggestions
                        simplified_ai_text = f'[{tech_to_filter} 프로젝트 목록 표시]'
                    else:
                        ai_response = {'type': 'text', 'content': f"'{tech_to_filter}' 기술을 사용하는 프로젝트를 찾을 수 없습니다."}
                else:
                    projects = projects_query.order_by('-created_at')
                    if projects.exists():
                        ai_response = {'type': 'html', 'content': render_to_string('ai_search/_project_cards.html', {'projects': projects})}
                        ai_response['suggestions'] = dynamic_project_suggestions
                        simplified_ai_text = '[프로젝트 목록 표시]'
                    else:
                        ai_response = {'type': 'text', 'content': '현재 데이터베이스에 등록된 프로젝트가 없습니다.'}

            # Priority 3: Other keywords
            elif '기술' in user_message or '스택' in user_message:
                ai_response = {
                    'type': 'html',
                    'content': """
                    <p>포트폴리오의 주요 기술 스택은 다음과 같습니다. 💻</p>
                    <ul>
                        <li><strong>Python &amp; Django:</strong> 안정적인 백엔드 시스템을 구축합니다.</li>
                        <li><strong>JavaScript &amp; React:</strong> 동적이고 인터랙티브한 프론트엔드를 구현합니다.</li>
                        <li><strong>Docker:</strong> 개발 및 배포 환경의 일관성을 유지하고 운영 효율성을 높입니다.</li>
                        <li><strong>Databases:</strong> PostgreSQL, MySQL 등 관계형 데이터베이스를 다룹니다.</li>
                        <li><strong>Cloud:</strong> AWS, Google Cloud 등 클라우드 인프라 활용 경험이 있습니다.</li>
                    </ul>
                    """,
                    'suggestions': ['관련 프로젝트 보여줘']
                }
                simplified_ai_text = '[기술 스택 표시]'
            
            elif '소개' in user_message or '너' in user_message or '누구' in user_message or '뭘할수있' in user_message or '무엇을 할수있' in user_message:
                ai_response = {
                    'type': 'html',
                    'content': """
                    <p>저는 이 포트폴리오의 주인에 대해 알려주기 위해 만들어진 AI 어시스턴트입니다. 제가 할 수 있는 일은 다음과 같습니다:</p>
                    <ul>
                        <li><strong>프로젝트 정보 제공:</strong> "프로젝트 보여줘"라고 입력하시면 주인의 포트폴리오 프로젝트들을 상세히 보여드릴 수 있습니다.</li>
                        <li><strong>기술 스택 설명:</strong> "기술" 또는 "스택"에 대해 물어보시면 주인이 주로 사용하는 기술 스택을 알려드립니다.</li>
                        <li><strong>일반적인 대화:</strong> 포트폴리오와 관련하여 궁금한 점이 있으시다면 자유롭게 질문해주세요. 제가 아는 범위 내에서 성심껏 답변해 드립니다.</li>
                    </ul>
                    """
                }
                simplified_ai_text = '[기능 소개 표시]'
            
            elif '안녕' in user_message or 'hi' in user_message or 'hello' in user_message:
                ai_response = { 
                    'type': 'text', 
                    'content': '안녕하세요! 무엇을 도와드릴까요? "프로젝트 목록"이나 "기술 스택"에 대해 물어보시면 제가 아는 정보를 보여드릴게요.',
                    'suggestions': ['프로젝트 보여줘', '기술 스택 알려줘', '무엇을 할 수 있나요?']
                }

            # Priority 4: Fallback to LLM with context
            if not ai_response:
                formatted_history = "\n".join([f"User: {h['user']}\nAssistant: {h['ai']}" for h in history])
                system_prompt = "You are a helpful AI assistant for a personal portfolio website. Your owner is a developer. Please answer the user's questions based on the persona of an assistant who knows the developer well. **You must always answer in Korean.**"
                prompt_text = f"{system_prompt}\n\n{formatted_history}\n\nUser: {user_message}\n\nAssistant (in Korean): "
                
                try:
                    ollama_api_url = "http://localhost:11434/api/generate"
                    payload = {"model": "llama3:instruct", "prompt": prompt_text, "stream": False, "options": {"temperature": 0.7}}
                    response = requests.post(ollama_api_url, json=payload, timeout=300)
                    response.raise_for_status()
                    ollama_response_data = response.json()
                    ollama_text_response = ollama_response_data.get('response', 'Ollama에서 응답을 받지 못했습니다.')
                    ai_response = {'type': 'text', 'content': markdown.markdown(ollama_text_response)}
                except requests.exceptions.ConnectionError:
                    ai_response = {'type': 'text', 'content': 'Ollama 서버에 연결할 수 없습니다.'}
                except requests.exceptions.RequestException as e:
                    ai_response = {'type': 'text', 'content': f'Ollama API 호출 중 오류: {e}'}

            # 4. Save new exchange to session history
            if not simplified_ai_text:
                simplified_ai_text = ai_response.get('content', '')

            history.append({'user': user_message, 'ai': simplified_ai_text})
            request.session['chat_history'] = history[-4:]

            return JsonResponse({'response': ai_response})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
