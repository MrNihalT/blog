import csv
import uuid
import wget
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Author, Post, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Deleting existing data...")

        Category.objects.all().delete()
        Post.objects.all().delete()
        Author.objects.all().delete()

        file_path = settings.BASE_DIR / "new_postss.csv"
        with open(file_path, encoding='utf-8') as file:
            csv_reader = csv.reader(file)

            next(csv_reader)

            for row in csv_reader:
                author_name = row[1].split(",")[0]
                content = row[2]
                date = row[3]
                tags = row[5]
                title = row[6]  # Fixed: title should be row[6]
                image = "https://picsum.photos/1500/1000"

                file_name = f"{uuid.uuid4()}.jpg"
                image_path = f'{settings.BASE_DIR}/media/posts/{file_name}'
                try:
                    image_filename = wget.download(image, image_path)
                    uploaded_file_url = f'posts/{file_name}'
                except:
                    uploaded_file_url = "posts/Screenshot_7.png"

                if Author.objects.filter(name=author_name).exists():
                    author = Author.objects.get(name=author_name)
                else:
                    user = User.objects.create_user(
                        username=uuid.uuid4(),
                        password="password",
                        first_name=author_name,
                    )

                    author = Author.objects.create(name=author_name, user=user)

                post = Post.objects.create(
                    title=title,
                    description=content,
                    short_description=content[:50],
                    time_to_read="5 min",
                    featured_image=uploaded_file_url,
                    author=author,
                    published_date=date,
                )

                tags_list = tags.split(",")
                for tag in tags_list:
                    if tag.strip():
                        item, created = Category.objects.get_or_create(title=tag)
                        post.categories.add(item)

        print("Process completed")