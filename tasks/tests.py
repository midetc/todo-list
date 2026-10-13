from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Tag, Task


class TaskTests(TestCase):
    def test_home_shows_open_tasks_before_done_and_newest_first(self):
        older = Task.objects.create(content="older open")
        newer = Task.objects.create(content="newer open")
        done = Task.objects.create(content="done task", done=True)
        now = timezone.now()
        Task.objects.filter(pk=older.pk).update(datetime=now - timedelta(days=2))
        Task.objects.filter(pk=newer.pk).update(datetime=now - timedelta(days=1))

        response = self.client.get(reverse("tasks:task-list"))

        self.assertEqual(response.status_code, 200)
        contents = [task.content for task in response.context["task_list"]]
        self.assertEqual(contents, ["newer open", "older open", "done task"])

    def test_home_shows_task_details(self):
        tag = Tag.objects.create(name="shop")
        task = Task.objects.create(
            content="Buy milk",
            deadline=timezone.now(),
        )
        task.tags.add(tag)

        response = self.client.get(reverse("tasks:task-list"))

        self.assertContains(response, "Buy milk")
        self.assertContains(response, "Not done")
        self.assertContains(response, "Created:")
        self.assertContains(response, "Deadline:")
        self.assertContains(response, "shop")
        self.assertContains(response, "Complete")

    def test_create_task_with_tag_and_deadline(self):
        tag = Tag.objects.create(name="shop")

        response = self.client.post(
            reverse("tasks:task-create"),
            {
                "content": "Buy milk",
                "deadline": "2026-10-20T18:30",
                "tags": [tag.pk],
            },
        )

        self.assertRedirects(response, reverse("tasks:task-list"))
        task = Task.objects.get()
        self.assertEqual(task.content, "Buy milk")
        self.assertFalse(task.done)
        self.assertIsNotNone(task.deadline)
        self.assertEqual(list(task.tags.all()), [tag])

    def test_update_task(self):
        task = Task.objects.create(content="Old")

        response = self.client.post(
            reverse("tasks:task-update", args=[task.pk]),
            {"content": "New"},
        )

        self.assertRedirects(response, reverse("tasks:task-list"))
        task.refresh_from_db()
        self.assertEqual(task.content, "New")

    def test_delete_task(self):
        task = Task.objects.create(content="Gone")

        response = self.client.post(reverse("tasks:task-delete", args=[task.pk]))

        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_toggle_switches_done_and_redirects_home(self):
        task = Task.objects.create(content="Toggle", done=False)
        url = reverse("tasks:task-toggle", args=[task.pk])

        self.assertEqual(self.client.get(url).status_code, 405)

        completed = self.client.post(url)
        self.assertRedirects(completed, reverse("tasks:task-list"))
        task.refresh_from_db()
        self.assertTrue(task.done)

        self.client.post(url)
        task.refresh_from_db()
        self.assertFalse(task.done)

        home = self.client.get(reverse("tasks:task-list"))
        self.assertContains(home, "Complete")


class TagTests(TestCase):
    def test_tag_pages_create_update_and_delete(self):
        created = self.client.post(reverse("tasks:tag-create"), {"name": "shop"})
        self.assertRedirects(created, reverse("tasks:tag-list"))
        tag = Tag.objects.get(name="shop")

        listed = self.client.get(reverse("tasks:tag-list"))
        self.assertContains(listed, "shop")
        self.assertContains(listed, reverse("tasks:tag-update", args=[tag.pk]))
        self.assertContains(listed, reverse("tasks:tag-delete", args=[tag.pk]))

        updated = self.client.post(
            reverse("tasks:tag-update", args=[tag.pk]),
            {"name": "grocery"},
        )
        self.assertRedirects(updated, reverse("tasks:tag-list"))
        tag.refresh_from_db()
        self.assertEqual(tag.name, "grocery")

        deleted = self.client.post(reverse("tasks:tag-delete", args=[tag.pk]))
        self.assertRedirects(deleted, reverse("tasks:tag-list"))
        self.assertFalse(Tag.objects.filter(pk=tag.pk).exists())

    def test_deleting_a_tag_keeps_the_task(self):
        tag = Tag.objects.create(name="shop")
        task = Task.objects.create(content="Buy milk")
        task.tags.add(tag)

        self.client.post(reverse("tasks:tag-delete", args=[tag.pk]))

        task.refresh_from_db()
        self.assertEqual(task.content, "Buy milk")
        self.assertEqual(task.tags.count(), 0)
