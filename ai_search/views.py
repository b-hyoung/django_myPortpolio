import json
import os
import markdown
from openai import OpenAI, AuthenticationError
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
    Handles conversational AJAX requests using an OpenAI RAG pattern.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').lower().strip()
        history = request.session.get('chat_history', [])
        ai_response = {}
        
        # --- Priority 1: Project-related queries ---
        if '프로젝트' in user_message or '포트폴리오' in user_message or '뭐했어' in user_message or '뭐 했어' in user_message:
            projects_query = Project.objects.filter(is_visible=True).order_by('-created_at')
            
            # Optional: re-introduce tech filtering if needed. For now, show all projects.
            # detected_techs = list(set([TECH_MAP[key] for key in TECH_MAP if key in user_message]))
            # if detected_techs:
            #    tech_to_filter = detected_techs[0]
            #    projects_query = projects_query.filter(technologies__iregex=fr'\b{tech_to_filter}\b')

            projects_to_display = projects_query[:4] # Display up to 4 projects
            
            if projects_to_display.exists():
                rendered_html = render_to_string('ai_search/_project_cards.html', {'projects': projects_to_display})
                ai_response = {'type': 'html', 'content': rendered_html}
            else:
                ai_response = {'type': 'text', 'content': '현재 등록된 프로젝트가 없습니다.'}
        
        # If ai_response is already set by project logic, skip OpenAI call
        if ai_response:
            # --- Save history (for predefined responses) ---
            simplified_ai_text = ai_response.get('content', '') # Use actual HTML or text
            history.append({'user': user_message, 'ai': simplified_ai_text})
            request.session['chat_history'] = history[-4:] # Keep last 4 exchanges
            return JsonResponse({'response': ai_response})

        # --- RAG: Retrieve Context from Database (if no specific rule matched) ---
        projects = Project.objects.filter(is_visible=True)
        project_context = "\n\n".join([
            f"Project Title: {p.title}\n"
            f"Description: {p.description}\n"
            f"Technologies: {p.technologies}"
            for p in projects
        ])

        # --- Initialize OpenAI Client ---
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return JsonResponse({
                'response': {'type': 'text', 'content': '관리자에게 문의하세요: OPENAI_API_KEY가 설정되지 않았습니다.'}
            })
        client = OpenAI(api_key=api_key)

        # --- Prepare messages for OpenAI API ---
        # We create a simplified history for the prompt
        formatted_history = []
        for h in history:
            formatted_history.append({"role": "user", "content": h['user']})
            # We assume the 'ai' part in history is simplified text
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

        # --- Call OpenAI API ---
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
            )
            ai_text_response = completion.choices[0].message.content
            ai_response = {'type': 'html', 'content': markdown.markdown(ai_text_response)}

        except AuthenticationError:
            ai_response = {'type': 'text', 'content': "OpenAI API 키가 유효하지 않습니다. 관리자에게 문의하세요."}
        except Exception as e:
            ai_response = {'type': 'text', 'content': f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}"}
        
        # --- Save history ---
        history.append({'user': user_message, 'ai': ai_text_response}) # Save the raw text response for future context
        request.session['chat_history'] = history[-4:] # Keep last 4 exchanges

        return JsonResponse({'response': ai_response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

