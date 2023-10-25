import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

import random
import json

with open('conf.json') as config_file:
    config = json.load(config_file)


async def action(s, users):
    base_url = config['base_url']
    posts_id: list[str] = []
    try:
        async with s.post(f'{base_url}/signup', json={'name': f'bot{users}', 'password': 'pass'}) as r:
            if r.status != 200:
                print(f'Signup - {await r.json()}')

        async with s.post(f'{base_url}/login', json={'login': f'bot{users}', 'password': 'pass'}) as r:
            if r.status != 200:
                r.raise_for_status()
            token = await r.json()

        for _ in range(config['max_posts_per_user']):
            async with s.post(f'{base_url}/posts', json={'content': f'Some text {users}'},
                              headers={'Authorization': f'Bearer {token["access"]}'}) as r:
                if r.status != 200:
                    r.raise_for_status()
                post = await r.json()
                posts_id.append(post['id'])
                print(f'Post - {post}')

        for _ in range(config['max_likes_per_user']):
            async with s.post(f'{base_url}/posts/like', json={'post_id': random.choice(posts_id)},
                              headers={'Authorization': f'Bearer {token["access"]}'}) as r:
                print(f'Like - {await r.json()}')

        return {f'Bot {users}': 'finished'}
    except ClientConnectorError:
        return {f'Bot {users}': 'error connection'}


async def action_all(s, users):
    tasks = []
    for user in users:
        task = asyncio.create_task(action(s, user))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


async def main():
    users = range(1, config['number_of_users'] + 1)
    async with aiohttp.ClientSession() as session:
        print(await action_all(session, users))


if __name__ == '__main__':
    if not(isinstance(config['number_of_users'], int)) or not(isinstance(config['max_posts_per_user'], int)) or \
            not(isinstance(config['max_likes_per_user'], int)):
        print("Please, check data type from config file for validity (must be int type)")
        exit(1)
    asyncio.run(main())
