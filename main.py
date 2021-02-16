from dynamodb import get_all_users

def main():
    users = get_all_users()
    if users:
        for user in users:
            print(user['info']['first_name'])


if __name__ == '__main__':
    main()
