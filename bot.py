import logging
import random
import tomllib
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

import faker
import httpx

fake = faker.Faker()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
host = "http://127.0.0.1:8000"


def get_config(conf_name: str = "bot-conf.toml") -> dict[str, int]:
    logger.info("Loading config")
    with open(conf_name, mode="rb") as fp:
        config = tomllib.load(fp)
        return config["bot"]


def create_user_with_posts(client: httpx.Client, max_posts_per_user: int) -> tuple[str, list[dict]]:
    user_data = {
        "email": fake.email(),
        "password": fake.password(),
        "nickname": fake.name(),
    }
    logger.info(f"Creating user with email {user_data['email']}")
    client.post("/api/auth/register", json=user_data)
    user_data = {
        "username": user_data["email"],
        "password": user_data["password"],
    }
    logger.info(f"Logging in user with email {user_data['username']}")
    response = client.post("/api/auth/jwt/login", data=user_data)
    token = response.json()["access_token"]
    created_posts = []
    posts_to_create = random.randint(1, max_posts_per_user)
    for _ in range(posts_to_create):
        post_data = {
            "title": fake.sentence(),
            "content": fake.text(),
        }
        logger.info(f"User {user_data['username']} creating post with title {post_data['title'][:15]}")
        response = client.post(
            "/api/post",
            json=post_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        created_posts.append(response.json())
    return token, created_posts


def like_posts(client: httpx.Client, token: str, all_posts: list[dict], max_likes_per_user: int) -> None:
    posts_to_like = random.randint(1, max_likes_per_user)
    all_posts = deepcopy(all_posts)
    for _ in range(posts_to_like):
        post = random.choice(all_posts)
        logger.info(f"User liking post with title {post['id']}")
        client.patch(
            f"/api/post/like/{post['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        all_posts.remove(post)


def main() -> None:
    config = get_config()
    number_of_users = config.get("number_of_users", 5)
    max_posts_per_user = config.get("max_posts_per_user", 10)
    max_likes_per_user = config.get("max_likes_per_user", 5)
    tokens = []
    all_posts = []
    with httpx.Client(base_url=host) as client:
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [
                executor.submit(create_user_with_posts, client, max_posts_per_user) for _ in range(number_of_users)
            ]
            for future in futures:
                token, created_posts = future.result()
                tokens.append(token)
                all_posts.extend(created_posts)
            futures = [executor.submit(like_posts, client, token, all_posts, max_likes_per_user) for token in tokens]
            for future in futures:
                future.result()


if __name__ == "__main__":
    main()
