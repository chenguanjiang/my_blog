import os
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from userprofile.models import Profile
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    help = "清理数据库中指向不存在文件的头像引用"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="仅统计与展示将被清理的记录，不实际修改数据库",
        )

    def handle(self, *args, **options):
        dry = options.get("dry_run", False)
        total = 0
        affected = 0

        qs = Profile.objects.all().only("id", "avatar")
        for p in qs.iterator():
            total += 1
            # 没有头像或为空字符串则跳过
            if not p.avatar or not p.avatar.name:
                continue
            rel_path = p.avatar.name
            # 使用存储层判断文件是否存在
            exists = default_storage.exists(rel_path)
            if not exists:
                affected += 1
                if dry:
                    self.stdout.write(f"[DRY] Profile#{p.id} 头像缺失: {rel_path}")
                else:
                    # 清空引用。由于字段非 null，可设为空字符串
                    p.avatar = ""
                    p.save(update_fields=["avatar"])
                    self.stdout.write(f"[FIXED] Profile#{p.id} 头像已清空: {rel_path}")

        summary = f"扫描完成，共 {total} 条，缺失头像 {affected} 条"
        if dry:
            summary += "（未执行修改）"
        self.stdout.write(summary)
