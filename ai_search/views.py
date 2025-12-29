import json
import requests
import markdown
from django.shortcuts import render
from django.contrib import messages


# Agent's tools for web search and fetching (simulated by Python comments for local execution)
# from core.agent_tools import google_web_search, web_fetch 

def ai_search_view(request):
    query = None
    ai_result = None

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if not query:
            messages.error(request, '검색어를 입력해 주세요.')
            return render(request, 'ai_search/ai_search.html', {'query': query})

        try:
            # --- Step 1: Simulate Agent's Google Web Search ---
            # In a real environment, this would be a tool call to google_web_search
            # For local execution, you might replace this with a direct call to a search API
            
            # Simulated search results (as if from google_web_search)
            
            # Placeholder for actual search results. For the agent's workflow,
            # this would be replaced by actual web search and processing.
            simulated_search_results = [
                {"title": "Sample Article 1", "link": "https://example.com/article1"},
                {"title": "Sample Article 2", "link": "https://example.com/article2"},
                # Add more simulated results here as needed for local testing
            ]

            if not simulated_search_results:
                messages.warning(request, f"'{query}'에 대한 검색 결과를 찾을 수 없습니다.")
                return render(request, 'ai_search/ai_search.html', {'query': query})

            # --- Step 2: Simulate Agent's Web Fetch ---
            # In a real environment, this would be parallel web_fetch calls.
            # For local execution, you might implement web scraping or specific API calls.
            
            fetched_contents = []
            for item in simulated_search_results[:2]: # Fetch content for top 2 articles
                # Placeholder for actual content fetching.
                # In a real local setup, you'd use requests.get() and parse the HTML/text.
                fetched_contents.append(f"Content from {item['link']}: This is some sample content about {query} from {item['title']}.")

            if not fetched_contents:
                messages.warning(request, "가져올 수 있는 웹 콘텐츠가 없습니다.")
                return render(request, 'ai_search/ai_search.html', {'query': query})

            # --- Step 3: Prepare Prompt for Ollama ---
            combined_content = "\n\n".join(fetched_contents)
            ollama_prompt = f"""다음 웹 콘텐츠를 분석하고, '{query}'에 대한 정보를 한국어로 요약 정리해 주세요.
불필요한 내용은 제거하고, 핵심 정보 위주로 상세하게 설명해 주세요.
응답은 오직 한국어로만 작성해야 합니다. 추가 설명이나 인사말 없이 바로 요약 내용부터 시작하세요.

--- 사용자 질의: {query} ---

--- 웹 콘텐츠: ---
{combined_content}

--- 요약 정리 (한국어): ---
"""

            # --- Step 4: Ollama API Call (Placeholder - User must uncomment and configure for local Ollama) ---
            # IMPORTANT: This part assumes Ollama is running locally on http://localhost:11434
            # and that 'llama3:instruct' model is available.
            # If you are running this code, UNCOMMENT the 'requests' import at the top
            # and the following 'ollama_api_url' and 'payload' sections.
            # You might also need to install the 'requests' library: pip install requests
            
            ollama_api_url = "http://localhost:11434/api/generate"
            payload = {
                "model": "llama3:instruct",
                "prompt": ollama_prompt,
                "stream": False, # Set to True for streaming responses
                "options": {
                    "temperature": 0.7,
                }
            }

            
            # --- Actual Ollama API call would go here (uncomment for local testing) ---
            response = requests.post(ollama_api_url, json=payload, timeout=300)
            response.raise_for_status()
            ollama_response_data = response.json()
            ai_result_md = ollama_response_data.get('response', 'Ollama에서 응답을 받지 못했습니다.')
            ai_result = markdown.markdown(ai_result_md) if ai_result_md else ''

            # --- SIMULATED AI Response (for agent's workflow / if Ollama call is commented out) ---
            # The agent (me) will perform the summarization and translation based on the prompt.
            # User will see this simulated response if Ollama call is not uncommented.
            
            # ai_result = f"'{query}'에 대한 AI 요약 결과입니다. (이 메시지는 Ollama 연결 없이 생성된 시뮬레이션 결과입니다.)\n\n" \
            #             f"이곳에는 '{query}'에 대한 웹 검색 결과를 바탕으로 AI가 요약하고 한국어로 정리한 내용이 들어갑니다. " \
            #             f"주요 정보와 핵심 개념 위주로 설명되며, 예를 들어 '웹 개발 트렌드'에 대한 검색이라면, " \
            #             f"새로운 프레임워크, AI/ML 통합, 보안 동향 등에 대한 상세한 분석이 포함될 수 있습니다."
            # messages.success(request, 'AI 검색이 완료되었습니다!')
            # This part is already uncommented now, so the simulated response is not active.
            # No changes needed here. The user must have uncommented the Ollama part.
            messages.success(request, 'AI 검색이 완료되었습니다!')

        except requests.exceptions.ConnectionError:
            messages.error(request, 'Ollama 서버에 연결할 수 없습니다. Ollama가 실행 중인지 확인하고, `llama3:instruct` 모델이 다운로드되었는지 확인하세요.')
            ai_result = "Ollama 서버 연결 실패. Ollama가 실행 중이고 모델이 준비되었는지 확인해 주세요."
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Ollama API 호출 중 오류가 발생했습니다: {e}')
            ai_result = f"Ollama API 오류: {e}"
        except Exception as e:
            messages.error(request, f'예상치 못한 오류가 발생했습니다: {e}')
            ai_result = f"오류 발생: {e}"

    return render(request, 'ai_search/ai_search.html', {'query': query, 'result': ai_result})