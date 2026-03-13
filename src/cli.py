#!/usr/bin/env python3
"""CLI interface for Instagram DM tools — mirrors MCP server functionality."""

import argparse
import json
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def login(args):
    """Login and initialize the shared client."""
    from src.mcp_server import client, create_client
    import src.mcp_server as mcp_server

    username = getattr(args, "username", None) or os.getenv("INSTAGRAM_USERNAME")
    password = getattr(args, "password", None) or os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("Error: credentials required. Set INSTAGRAM_USERNAME/INSTAGRAM_PASSWORD env vars or use --username/--password.", file=sys.stderr)
        sys.exit(1)

    session_file = Path(f"{username}_session.json")

    try:
        if session_file.exists():
            client.load_settings(session_file)
        client.login(username, password)
        client.dump_settings(session_file)
    except Exception:
        if session_file.exists():
            session_file.unlink()
            mcp_server.client = create_client()
            mcp_server.client.login(username, password)
            mcp_server.client.dump_settings(session_file)
        else:
            raise


def output(result):
    """Pretty-print a result dict."""
    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))


def cmd_chats(args):
    from src.mcp_server import list_chats
    output(list_chats(
        amount=args.amount,
        selected_filter=args.filter,
        thread_message_limit=args.message_limit,
        full=args.full,
    ))


def cmd_messages(args):
    from src.mcp_server import list_messages
    output(list_messages(thread_id=args.thread_id, amount=args.amount))


def cmd_send(args):
    from src.mcp_server import send_message
    output(send_message(username=args.to, message=args.message))


def cmd_send_photo(args):
    from src.mcp_server import send_photo_message
    output(send_photo_message(username=args.to, photo_path=args.photo))


def cmd_send_video(args):
    from src.mcp_server import send_video_message
    output(send_video_message(username=args.to, video_path=args.video))


def cmd_seen(args):
    from src.mcp_server import mark_message_seen
    output(mark_message_seen(thread_id=args.thread_id, message_id=args.message_id))


def cmd_pending(args):
    from src.mcp_server import list_pending_chats
    output(list_pending_chats(amount=args.amount))


def cmd_search_threads(args):
    from src.mcp_server import search_threads
    output(search_threads(query=args.query))


def cmd_thread_by_participants(args):
    from src.mcp_server import get_thread_by_participants
    output(get_thread_by_participants(user_ids=args.user_ids))


def cmd_thread_details(args):
    from src.mcp_server import get_thread_details
    output(get_thread_details(thread_id=args.thread_id, amount=args.amount))


def cmd_user_id(args):
    from src.mcp_server import get_user_id_from_username
    output(get_user_id_from_username(username=args.username_lookup))


def cmd_username(args):
    from src.mcp_server import get_username_from_user_id
    output(get_username_from_user_id(user_id=args.user_id))


def cmd_user_info(args):
    from src.mcp_server import get_user_info
    output(get_user_info(username=args.username_lookup))


def cmd_online(args):
    from src.mcp_server import check_user_online_status
    output(check_user_online_status(usernames=args.usernames))


def cmd_search_users(args):
    from src.mcp_server import search_users
    output(search_users(query=args.query))


def cmd_stories(args):
    from src.mcp_server import get_user_stories
    output(get_user_stories(username=args.username_lookup))


def cmd_like(args):
    from src.mcp_server import like_media
    output(like_media(media_url=args.url, like=not args.unlike))


def cmd_followers(args):
    from src.mcp_server import get_user_followers
    output(get_user_followers(username=args.username_lookup, count=args.count))


def cmd_following(args):
    from src.mcp_server import get_user_following
    output(get_user_following(username=args.username_lookup, count=args.count))


def cmd_posts(args):
    from src.mcp_server import get_user_posts
    output(get_user_posts(username=args.username_lookup, count=args.count))


def cmd_media_messages(args):
    from src.mcp_server import list_media_messages
    output(list_media_messages(thread_id=args.thread_id, limit=args.limit))


def cmd_download_media(args):
    from src.mcp_server import download_media_from_message
    output(download_media_from_message(
        message_id=args.message_id,
        thread_id=args.thread_id,
        download_path=args.output,
    ))


def cmd_download_shared(args):
    from src.mcp_server import download_shared_post_from_message
    output(download_shared_post_from_message(
        message_id=args.message_id,
        thread_id=args.thread_id,
        download_path=args.output,
    ))


def cmd_delete(args):
    from src.mcp_server import delete_message
    output(delete_message(thread_id=args.thread_id, message_id=args.message_id))


def cmd_mute(args):
    from src.mcp_server import mute_conversation
    output(mute_conversation(thread_id=args.thread_id, mute=not args.unmute))


def build_parser():
    p = argparse.ArgumentParser(prog="instagram", description="Instagram DM CLI")
    p.add_argument("--username", help="Instagram username")
    p.add_argument("--password", help="Instagram password")

    sub = p.add_subparsers(dest="command", required=True)

    # chats
    s = sub.add_parser("chats", help="List DM threads")
    s.add_argument("-n", "--amount", type=int, default=20)
    s.add_argument("--filter", default="", choices=["", "flagged", "unread"])
    s.add_argument("--message-limit", type=int, default=None)
    s.add_argument("--full", action="store_true")
    s.set_defaults(func=cmd_chats)

    # messages
    s = sub.add_parser("messages", help="List messages in a thread")
    s.add_argument("thread_id")
    s.add_argument("-n", "--amount", type=int, default=20)
    s.set_defaults(func=cmd_messages)

    # send
    s = sub.add_parser("send", help="Send a text message")
    s.add_argument("to", help="Recipient username")
    s.add_argument("message")
    s.set_defaults(func=cmd_send)

    # send-photo
    s = sub.add_parser("send-photo", help="Send a photo")
    s.add_argument("to", help="Recipient username")
    s.add_argument("photo", help="Path to photo file")
    s.set_defaults(func=cmd_send_photo)

    # send-video
    s = sub.add_parser("send-video", help="Send a video")
    s.add_argument("to", help="Recipient username")
    s.add_argument("video", help="Path to video file")
    s.set_defaults(func=cmd_send_video)

    # seen
    s = sub.add_parser("seen", help="Mark message as seen")
    s.add_argument("thread_id")
    s.add_argument("message_id")
    s.set_defaults(func=cmd_seen)

    # pending
    s = sub.add_parser("pending", help="List pending chats")
    s.add_argument("-n", "--amount", type=int, default=20)
    s.set_defaults(func=cmd_pending)

    # search-threads
    s = sub.add_parser("search-threads", help="Search DM threads")
    s.add_argument("query")
    s.set_defaults(func=cmd_search_threads)

    # thread-by-participants
    s = sub.add_parser("thread-by-participants", help="Get thread by user IDs")
    s.add_argument("user_ids", type=int, nargs="+")
    s.set_defaults(func=cmd_thread_by_participants)

    # thread-details
    s = sub.add_parser("thread-details", help="Get thread details")
    s.add_argument("thread_id")
    s.add_argument("-n", "--amount", type=int, default=20)
    s.set_defaults(func=cmd_thread_details)

    # user-id
    s = sub.add_parser("user-id", help="Get user ID from username")
    s.add_argument("username_lookup")
    s.set_defaults(func=cmd_user_id)

    # username
    s = sub.add_parser("username", help="Get username from user ID")
    s.add_argument("user_id")
    s.set_defaults(func=cmd_username)

    # user-info
    s = sub.add_parser("user-info", help="Get user info")
    s.add_argument("username_lookup")
    s.set_defaults(func=cmd_user_info)

    # online
    s = sub.add_parser("online", help="Check online status")
    s.add_argument("usernames", nargs="+")
    s.set_defaults(func=cmd_online)

    # search-users
    s = sub.add_parser("search-users", help="Search users")
    s.add_argument("query")
    s.set_defaults(func=cmd_search_users)

    # stories
    s = sub.add_parser("stories", help="Get user stories")
    s.add_argument("username_lookup")
    s.set_defaults(func=cmd_stories)

    # like
    s = sub.add_parser("like", help="Like/unlike a post")
    s.add_argument("url", help="Post URL")
    s.add_argument("--unlike", action="store_true")
    s.set_defaults(func=cmd_like)

    # followers
    s = sub.add_parser("followers", help="Get user followers")
    s.add_argument("username_lookup")
    s.add_argument("-n", "--count", type=int, default=20)
    s.set_defaults(func=cmd_followers)

    # following
    s = sub.add_parser("following", help="Get user following")
    s.add_argument("username_lookup")
    s.add_argument("-n", "--count", type=int, default=20)
    s.set_defaults(func=cmd_following)

    # posts
    s = sub.add_parser("posts", help="Get user posts")
    s.add_argument("username_lookup")
    s.add_argument("-n", "--count", type=int, default=12)
    s.set_defaults(func=cmd_posts)

    # media-messages
    s = sub.add_parser("media-messages", help="List media messages in thread")
    s.add_argument("thread_id")
    s.add_argument("--limit", type=int, default=100)
    s.set_defaults(func=cmd_media_messages)

    # download-media
    s = sub.add_parser("download-media", help="Download media from DM message")
    s.add_argument("thread_id")
    s.add_argument("message_id")
    s.add_argument("-o", "--output", default="./downloads")
    s.set_defaults(func=cmd_download_media)

    # download-shared
    s = sub.add_parser("download-shared", help="Download shared post/reel from DM")
    s.add_argument("thread_id")
    s.add_argument("message_id")
    s.add_argument("-o", "--output", default="./downloads")
    s.set_defaults(func=cmd_download_shared)

    # delete
    s = sub.add_parser("delete", help="Delete a message")
    s.add_argument("thread_id")
    s.add_argument("message_id")
    s.set_defaults(func=cmd_delete)

    # mute
    s = sub.add_parser("mute", help="Mute/unmute a conversation")
    s.add_argument("thread_id")
    s.add_argument("--unmute", action="store_true")
    s.set_defaults(func=cmd_mute)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    login(args)
    args.func(args)


if __name__ == "__main__":
    main()
