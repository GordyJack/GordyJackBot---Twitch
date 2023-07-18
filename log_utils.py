import os
from datetime import datetime


def get_top_chatter(log_file, exclude_chatters):
    top_chatter = None
    with open(log_file, 'r') as f:
        found_top_chatters = False
        for line in f:
            if line.startswith('Top Chatters:'):
                found_top_chatters = True
            elif found_top_chatters and line.startswith('---'):
                chatter = line.strip().split(':')[0][3:]
                if exclude_chatters is None or chatter not in exclude_chatters:
                    top_chatter = chatter
                    break
    return top_chatter


def get_most_recent(log_directory='logs/chat'):
    log_files = os.listdir(log_directory)
    if not log_files:
        print("No log files found.")
        return

    log_files.sort()
    return os.path.join(log_directory, log_files[-1])


def save_chat_log(log_messages):
    now = datetime.now()
    current_date_time = now.strftime("%d%b%Y_%H%M%S")
    current_long_date = now.strftime("%A, the %d of %B")
    current_long_time = now.strftime("%I:%M:%S %p")
    filename = f"logs/chat/Stream Chat --- {current_date_time}.txt"

    full_log = ''
    authors_counts = {}
    command_count = 0
    response_count = 0

    for message in log_messages:
        full_log += f"{message}\n"

        message_split = message.split(' ')

        author = message_split[1].replace(':', '')
        authors_counts.setdefault(author, 0)
        authors_counts[author] += 1

        content = message_split[2]

        if content.startswith('!'):
            command_count += 1
        if author == "GordyJackBot":
            response_count += 1

    all_chatters = {k: authors_counts[k] for k in sorted(authors_counts)}
    top_chatters = {k: v for k, v in sorted(authors_counts.items(), key=lambda item: item[1], reverse=True)}

    line_separator = '======================================================================='
    with open(filename, "w") as f:
        f.write(line_separator + "\n")
        f.write(f"Twitch chat log for the stream on {current_long_date} ending at {current_long_time}\n")
        f.write(line_separator + "\n")
        f.write(f"Total Messages: {len(log_messages)}\n")
        f.write(f"---Chats: {len(log_messages) - command_count}\n")
        f.write(f"---Commands: {command_count}\n")
        f.write(f"---Responses: {response_count}\n")
        f.write(f"Total Chatters: {len(authors_counts.keys())}\n")
        for author, count in all_chatters.items():
            f.write(f"---{author}: {count}\n")
        f.write(f"Top Chatters:\n")
        for author, count in top_chatters.items():
            f.write(f"---{author}: {count}\n")
        f.write(line_separator + "\n")
        f.write(full_log)

    print(f"Chat log saved to {filename}")
