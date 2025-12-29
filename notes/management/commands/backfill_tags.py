import requests
import json
from django.core.management.base import BaseCommand
from notes.models import Note

class Command(BaseCommand):
    help = 'Backfills tags for existing notes that do not have any.'

    def handle(self, *args, **options):
        notes_without_tags = Note.objects.filter(tags__isnull=True)
        if not notes_without_tags.exists():
            self.stdout.write(self.style.SUCCESS('All notes already have tags. Nothing to do.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {notes_without_tags.count()} notes without tags. Starting backfill...'))

        for note in notes_without_tags:
            self.stdout.write(f'Processing note: "{note.title}"')
            if not note.content:
                self.stdout.write(self.style.WARNING('  - Skipping note as it has no content.'))
                continue

            try:
                # --- Prepare the prompt for Ollama ---
                prompt = (
                    f"다음 텍스트에서 가장 중요한 핵심 키워드 2개를 쉼표(,)로 구분하여 추출해 주세요. "
                    f"다른 설명 없이 키워드만 응답해야 합니다. 예: 파이썬,장고\n\n"
                    f"텍스트: {note.content}"
                )

                # --- Ollama API Call ---
                ollama_api_url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "llama3:instruct",
                    "prompt": prompt,
                    "stream": False
                }
                
                response = requests.post(ollama_api_url, json=payload, timeout=60)
                response.raise_for_status()
                
                ollama_response = response.json()
                raw_keywords = ollama_response.get('response', '').strip()
                
                if raw_keywords:
                    keyword_list = [tag.strip() for tag in raw_keywords.split(',') if tag.strip()]
                    note.tags.add(*keyword_list)
                    self.stdout.write(self.style.SUCCESS(f'  - Successfully added tags: {", ".join(keyword_list)}'))
                else:
                    self.stdout.write(self.style.WARNING('  - AI did not return any keywords.'))

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'  - Could not connect to Ollama. Error: {e}'))
                self.stdout.write(self.style.WARNING('  - Aborting backfill. Please ensure Ollama is running and accessible.'))
                break # Stop the process if Ollama isn't running
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  - An unexpected error occurred: {e}'))

        self.stdout.write(self.style.SUCCESS('Backfill process complete.'))
