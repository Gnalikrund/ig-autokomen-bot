from instagrapi import Client
from datetime import datetime, timezone
import random
import time

def login():
    cl = Client()
    username = input("Masukkan username IG: ")
    password = input("Masukkan password IG: ")
    cl.login(username, password)
    return cl

def load_targets(file_path="target.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_comments(file_path="komentar.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def handle_post_timing(post_time):
    now = datetime.now(timezone.utc)
    age = (now - post_time).total_seconds()

    if age < 30:
        wait_time = 30 - age
        print(f"Post baru (umur {int(age)}s), tunggu {int(wait_time)} detik...")
        time.sleep(wait_time)
        return True
    elif age > 80:
        print(f"Lewati post (umur {int(age)}s) - lebih dari 80 detik")
        return False
    else:
        return True

def main():
    cl = login()
    targets = load_targets()
    comments = load_comments()
    max_posts = 15

    for username in targets:
        try:
            user_id = cl.user_id_from_username(username)
            medias = cl.user_medias(user_id, 20)
            count = 0

            for media in medias:
                if count >= max_posts:
                    break

                if not handle_post_timing(media.taken_at):
                    continue

                komentar_gabungan = "\n".join(random.sample(comments, 2))
                cl.media_comment(media.id, komentar_gabungan)
                print(f"Komentar terkirim ke @{username}: {komentar_gabungan}")
                count += 1

        except Exception as e:
            print(f"Gagal untuk @{username}: {e}")

    print("Selesai semua target.")

if _name_ == "_main_":
    main()