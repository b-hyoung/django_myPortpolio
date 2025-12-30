from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from django.db.models.signals import m2m_changed, pre_delete, post_delete
from django.dispatch import receiver
from taggit.models import Tag, TaggedItem

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    ip_address = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.title


# ------------------------------
# Tag cleanup: delete tags that are no longer used by any object
# ------------------------------

def _delete_orphan_tags(tag_ids):
    """Delete Tag records whose usage count is 0 (no TaggedItem rows left)."""
    if not tag_ids:
        return
    for tag_id in tag_ids:
        if not TaggedItem.objects.filter(tag_id=tag_id).exists():
            Tag.objects.filter(id=tag_id).delete()


@receiver(m2m_changed, sender=Note.tags.through)
def cleanup_tags_on_change(sender, instance, action, pk_set, **kwargs):
    # When tags are removed/cleared from a note, purge any tags that became unused.
    if action in ("post_remove", "post_clear"):
        _delete_orphan_tags(pk_set)


@receiver(pre_delete, sender=Note)
def cache_tag_ids_before_note_delete(sender, instance, **kwargs):
    # Cache tag ids before deleting the note (after delete, M2M rows are gone).
    instance._deleted_tag_ids = list(instance.tags.values_list("id", flat=True))


@receiver(post_delete, sender=Note)
def cleanup_tags_after_note_delete(sender, instance, **kwargs):
    _delete_orphan_tags(getattr(instance, "_deleted_tag_ids", []))
    