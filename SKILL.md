---
name: instagram
description: Interact with Instagram DMs — list chats, read/send messages, search users, download media, manage threads. Use when the user asks anything about Instagram direct messages, sending DMs, checking Instagram chats, or interacting with Instagram users.
argument-hint: [command] [args...]
allowed-tools: Bash(instagram *)
---

# Instagram DM CLI (Claude Code Skill)

This skill wraps the Instagram DM MCP server as a CLI tool for use with [Claude Code](https://claude.com/claude-code).

## Setup

1. Clone this repo and install:
   ```bash
   # with uv
   uv pip install .
   # or with pip
   pip install .
   ```
2. Set credentials as environment variables:
   ```bash
   export INSTAGRAM_USERNAME="your_username"
   export INSTAGRAM_PASSWORD="your_password"
   ```
3. Copy this `SKILL.md` to `skills/instagram/SKILL.md` (personal) or keep it in the repo root for project-level use.

## Usage

All commands output JSON. Use the `instagram` entrypoint:

```bash
instagram <command> [args...]
```

## Commands Reference

### Chats & Threads

```bash
# List recent DM threads (default 20)
instagram chats [-n AMOUNT] [--filter {flagged,unread}] [--message-limit N] [--full]

# Read messages from a thread
instagram messages THREAD_ID [-n AMOUNT]

# Search DM threads by keyword
instagram search-threads QUERY

# Get thread details
instagram thread-details THREAD_ID [-n AMOUNT]

# Get thread by participant user IDs
instagram thread-by-participants USER_ID [USER_ID ...]

# List pending (message request) chats
instagram pending [-n AMOUNT]
```

### Sending Messages

```bash
# Send text message
instagram send USERNAME "message text"

# Send photo
instagram send-photo USERNAME /path/to/photo.jpg

# Send video
instagram send-video USERNAME /path/to/video.mp4
```

### User Lookup

```bash
# Get user info (bio, followers, etc.)
instagram user-info USERNAME

# Get user ID from username
instagram user-id USERNAME

# Get username from user ID
instagram username USER_ID

# Search users
instagram search-users QUERY

# Check online status
instagram online USERNAME [USERNAME ...]
```

### Content

```bash
# Get user stories
instagram stories USERNAME

# Get user posts
instagram posts USERNAME [-n COUNT]

# Get user followers
instagram followers USERNAME [-n COUNT]

# Get user following
instagram following USERNAME [-n COUNT]

# Like/unlike a post
instagram like URL [--unlike]
```

### Media in DMs

```bash
# List messages with media in a thread
instagram media-messages THREAD_ID [--limit N]

# Download media from a DM message
instagram download-media THREAD_ID MESSAGE_ID [-o OUTPUT_DIR]

# Download shared post/reel from a DM message
instagram download-shared THREAD_ID MESSAGE_ID [-o OUTPUT_DIR]
```

### Thread Management

```bash
# Mark message as seen
instagram seen THREAD_ID MESSAGE_ID

# Delete a message
instagram delete THREAD_ID MESSAGE_ID

# Mute/unmute a conversation
instagram mute THREAD_ID [--unmute]
```

## Workflow Tips

- To find a thread, first run `chats` to get thread IDs, then `messages THREAD_ID` to read.
- To message someone new, use `send USERNAME "text"` directly — no need to find thread ID first.
- Thread IDs are long numeric strings like `340282366841710301244258460745246570457`.
- When presenting messages, format them nicely: show sender, timestamp, and content.
- For media messages, describe the type (photo/video/reel share) since raw media can't be displayed.
