from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Q # Q 임포트
from .models import Note
from .forms import NoteForm
from taggit.models import Tag # Import Tag model
import random # random 모듈 추가

def index(request, tag_name=None):
    notes = Note.objects.all().order_by("-created_at") # 기본 쿼리셋

    query = request.GET.get('q') # 'q' 파라미터에서 검색어 가져오기
    tag_param = request.GET.get('tag') # 'tag' 파라미터에서 태그 이름 가져오기

    # URL 경로로 tag_name이 제공된 경우 (예: /notes/tag/python/)
    # 또는 검색 폼의 'q' 파라미터가 비어 있고 URL 경로에 tag_name이 있는 경우
    if tag_name and not query and not tag_param: # tag_param도 고려
        query = tag_name # URL 경로의 태그 이름을 검색 쿼리로 사용
    elif tag_param and not query: # 'q'가 없고 'tag' 파라미터가 있는 경우
        query = tag_param # 'tag' 파라미터를 검색 쿼리로 사용

    if query:
        # 제목 또는 태그 이름으로 검색
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct() # 중복 노트 제거
    
    form = NoteForm()
    all_tags = Tag.objects.annotate(num_times=Count('note')).all()

    # 각 노트에 결정론적 무작위 스타일 적용
    colors = ['#fff9c4', '#c4e6ff', '#d6ffc4', '#ffd6ed'] # Post-it 색상
    for note in notes:
        # 노트 ID를 시드로 사용하여 결정론적 무작위성 확보
        random.seed(note.id)
        note.random_color = random.choice(colors)
        note.random_rotation = (random.random() * 6) - 3 # -3 to +3 deg
        note.random_offset_x = (random.random() * 14) - 7 # -7 to +7 px
        note.random_offset_y = (random.random() * 14) - 7 # -7 to +7 px
    
    context = {
        'notes': notes,
        'tag_name': query, # 이제 tag_name은 검색 쿼리와 동일
        'form': form,
        'all_tags': all_tags,
    }
    return render(request, 'notes/index.html', context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    context = {
        'note': note,
    }
    return render(request, 'notes/note_detail.html', {'note': note})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_note(request):
    if request.method == 'POST':
        ip_address = get_client_ip(request)
        note_count = Note.objects.filter(ip_address=ip_address).count()

        if note_count >= 3:
            return JsonResponse({'status': 'error', 'message': 'IP당 3개의 노트만 생성할 수 있습니다.'}, status=403)

        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.ip_address = ip_address
            note.save()
            form.save_m2m() # Save ManyToMany relations for tags
            return JsonResponse({'status': 'success', 'message': '노트가 성공적으로 저장되었습니다.'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    # GET request: Render the create note page
    form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})


from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

def note_content_api(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    data = {
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.strftime('%Y.%m.%d'),
        # Add other fields as needed
    }
    return JsonResponse(data)

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_all_notes(request):
    if request.method == 'POST':
        if 'delete_all' in request.POST:
            try:
                Note.objects.all().delete()
                messages.success(request, '모든 노트가 성공적으로 삭제되었습니다.')
            except Exception as e:
                messages.error(request, f'노트 삭제 중 오류가 발생했습니다: {e}')
            return redirect('notes:admin_delete_all')

        elif 'delete_selected' in request.POST:
            note_ids = request.POST.getlist('note_ids')
            if not note_ids:
                messages.error(request, '삭제할 노트를 선택해주세요.')
                return redirect('notes:admin_delete_all')
            try:
                Note.objects.filter(id__in=note_ids).delete()
                messages.success(request, f'{len(note_ids)}개의 노트가 성공적으로 삭제되었습니다.')
            except Exception as e:
                messages.error(request, f'노트 삭제 중 오류가
 발생했습니다: {e}')
            return redirect('notes:admin_delete_all')
            
        else:
            messages.error(request, '잘못된 요청입니다.')
            return redirect('notes:admin_delete_all')

    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'notes/admin_delete_all.html', {'notes': notes})