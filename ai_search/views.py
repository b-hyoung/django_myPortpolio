import json
import os
import markdown
from openai import OpenAI, AuthenticationError
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from projects.models import Project
from django_ratelimit.decorators import ratelimit
import logging
import traceback # Import traceback

logger = logging.getLogger(__name__)


# --- Tech Name Mapping ---
TECH_MAP = {
    '파이썬': 'python', 'python': 'python',
    '장고': 'django', 'django': 'django',
    '리액트': 'react', 'react': 'react',
    '도커': 'docker', 'docker': 'docker',
    '자바스크립트': 'javascript', 'javascript': 'javascript',
    '자바': 'java', 'java': 'java',
    'mysql': 'mysql', 'sql': 'mysql', '마이에스큐엘': 'mysql',
    'postgresql': 'postgresql', '포스트그레스큐엘': 'postgresql',
    'aws': 'aws', '아마존 웹 서비스': 'aws',
    '넥스트js': 'nextjs', 'nextjs': 'nextjs', 'next.js': 'nextjs',
    '파이어베이스': 'firebase', 'firebase': 'firebase',
    '테일윈드css': 'tailwindcss', 'tailwindcss': 'tailwindcss', 'tailwind': 'tailwindcss',
    '소켓': 'socket', 'socket': 'socket',
    '올라마': 'ollama', 'ollama': 'ollama', 'llama3.1': 'ollama', 'llama': 'ollama',
    '스프링 부트': 'spring boot', 'spring boot': 'spring boot',
    '깃': 'git', 'git': 'git', 'github': 'git', '깃허브': 'git',
}

def ai_search_view(request):
    """
    Renders the main AI chat interface page.
    """
    return render(request, 'ai_search/ai_search.html', {'hide_layout_elements': True})

@ratelimit(key='ip', rate='10/m', block=True)
def chat_interaction(request):
    """
    Handles conversational AJAX requests using an OpenAI RAG pattern.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try: # Outer try-except to catch any unexpected error during initial processing
        data = json.loads(request.body)
        user_message = data.get('message', '').lower().strip()
        history = request.session.get('chat_history', [])
        ai_response = {}
        
        # --- Priority 1: Project-related queries ---
        if '프로젝트' in user_message or '포트폴리오' in user_message or '뭐했어' in user_message or '뭐 했어' in user_message:
            projects_query = Project.objects.filter(is_visible=True).order_by('-created_at')
            
            # Re-introduce tech filtering
            detected_techs = list(set([TECH_MAP[key] for key in TECH_MAP if key in user_message if key in TECH_MAP]))
            if detected_techs:
                tech_to_filter = detected_techs[0]
                projects_query = projects_query.filter(technologies__iregex=fr'\b{tech_to_filter}\b')

            projects_to_display = projects_query[:4] # Display up to 4 projects
            
            if projects_to_display.exists():
                rendered_html = render_to_string('ai_search/_project_cards.html', {'projects': projects_to_display})
                ai_response = {'type': 'html', 'content': rendered_html}
            else:
                ai_response = {'type': 'text', 'content': '현재 등록된 프로젝트가 없습니다.'}
        
        # If ai_response is already set by project logic, skip OpenAI call
        if ai_response:
            # For predefined responses, save a simplified text to history, NOT the raw HTML
            history_ai_content = "프로젝트 목록을 표시했습니다." if ai_response.get('type') == 'html' else ai_response.get('content', '')
            history.append({'user': user_message, 'ai': history_ai_content})
            request.session['chat_history'] = history[-4:] # Keep last 4 exchanges
            return JsonResponse({'response': ai_response})

        # --- RAG: Retrieve Context from Database (if no specific rule matched) ---
        # TEMPORARY TEST: Force a very short context to check if code changes are being deployed.
        project_context = "This is a temporary deployment test."


        # --- Dynamic AI Service Selection ---
        # 환경 변수 'AI_SERVICE_PROVIDER' 값에 따라 사용할 AI 서비스를 선택합니다.
        # 'openai' 또는 'local'을 값으로 가집니다. 기본값은 'openai' 입니다.
        ai_provider = os.environ.get("AI_SERVICE_PROVIDER", "openai").lower()

        # --- Prepare messages for AI API (Common for both services) ---
        formatted_history = []
        for h in history:
            formatted_history.append({"role": "user", "content": h['user']})
            formatted_history.append({"role": "assistant", "content": h['ai']})

        system_prompt = (
            "You are a helpful AI assistant for a personal portfolio website. Your owner is a developer. "
            "Please answer the user's questions based on the persona of an assistant who knows the developer well. "
            "Use the provided project context to answer questions about projects accurately. "
            "**You must always answer in Korean.**"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"## 포트폴리오 프로젝트 정보:\n{project_context}"}
        ]
        messages.extend(formatted_history)
        messages.append({"role": "user", "content": user_message})

        # --- Call AI Service based on provider ---
        try:
            if ai_provider == 'local':
                # --- Use Local AI (Ollama) ---
                ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
                # 사용자가 지정한 모델 'llama3:instruct'를 기본값으로 설정합니다.
                ollama_model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3:instruct")

                client = OpenAI(
                    base_url=ollama_base_url,
                    api_key='ollama', # Ollama는 api_key가 필요 없습니다.
                )
                
                logger.info(f"Connecting to Local AI: {ollama_base_url} with model {ollama_model_name}")
                
                completion = client.chat.completions.create(
                    model=ollama_model_name,
                    messages=messages,
                    temperature=0.7,
                )
            else: # Default to OpenAI
                # --- Use OpenAI ---
                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    logger.error("OPENAI_API_KEY is not set for the 'openai' provider.")
                    return JsonResponse({
                        'response': {'type': 'text', 'content': '관리자에게 문의하세요: OPENAI_API_KEY가 설정되지 않았습니다.'}
                    })
                
                client = OpenAI(api_key=api_key)
                
                logger.info("Connecting to OpenAI API with model gpt-3.5-turbo")
                
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                )

            # --- Process and Save Response (Common for both services) ---
            ai_text_response = completion.choices[0].message.content
            ai_response = {'type': 'html', 'content': markdown.markdown(ai_text_response)}
            
            history.append({'user': user_message, 'ai': ai_text_response}) 
            request.session['chat_history'] = history[-4:] 

        except AuthenticationError as e:
            logger.error(f"AI Service AuthenticationError for provider '{ai_provider}': {e}")
            ai_response = {'type': 'text', 'content': f"AI 서비스 인증 오류가 발생했습니다. ('{ai_provider}'). 관리자에게 문의하세요."}
        except Exception as e:
            logger.error(f"Error during AI call for provider '{ai_provider}': {e}", exc_info=True)
            ai_response = {'type': 'text', 'content': f"AI 모델 호출 중 오류가 발생했습니다. ('{ai_provider}'). 서버 로그를 확인하세요."}
        
        return JsonResponse({'response': ai_response})

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError in chat_interaction: {e}", exc_info=True)
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400) # Bad Request
    except Exception as e:
        logger.error(f"Unhandled exception in chat_interaction: {e}", exc_info=True)
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

