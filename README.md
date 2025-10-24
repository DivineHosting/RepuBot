# 🤖 RepuBot

RepuBot is a powerful **Discord reputation and vouch bot** inspired by bots like Prompt and Shiba.  
It allows members to vouch for each other, track reputation, and manage approvals with a clean and automated system.

---

## 🧩 Features

### 👤 Member Commands (Prefix: `+`)
| Command | Description |
|----------|-------------|
| `+vouch @user <reason>` | Submit a vouch request (requires admin approval) |
| `+rep @user` | Check a user's total approved vouches |
| `+p` | View your submitted vouches |
| `+leaderboard` | Show top users by total approved vouches |
| `+help` | Show all available commands |

### ⚙️ Admin Slash Commands
| Command | Description |
|----------|-------------|
| `/approve <vouch_id>` | Approve a pending vouch |
| `/deny <vouch_id> [reason]` | Deny a pending vouch |
| `/clearvouch @user` | Clear all vouches for a user |
| `/setlogchannel #channel` | Set the server’s vouch-log channel |

---

## 🧾 Data Storage (MongoDB)
Each vouch is stored securely in MongoDB:

```json
{
  "_id": ObjectId,
  "guild_id": 1234567890,
  "vouched_by": "UserID",
  "vouched_for": "UserID",
  "reason": "Vouch reason text",
  "status": "pending | approved | denied",
  "timestamp": "2025-10-23T12:00:00Z"
}

Settings (like vouch-log channel) are also stored per guild.


---

🧱 Folder Structure

RepuBot/
├── bot.py               # Main bot file
├── config.py            # Loads .env and settings
├── database.py          # MongoDB connection and queries
├── .env                 # Private credentials (DO NOT SHARE)
├── requirements.txt     # Dependencies
├── cogs/
│   ├── member.py        # +vouch, +rep, +p, +leaderboard
│   ├── admin.py         # /approve, /deny, /setlogchannel, etc.
│   ├── help.py          # +help command
│   └── utils.py         # Common embed formatting
└── README.md


---

⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/YOUR_GITHUB_USERNAME/RepuBot.git
cd RepuBot

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Configure Environment Variables

Create a file named .env in the project root:

DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
MONGO_URI=YOUR_MONGODB_URI

4️⃣ Start the Bot

python bot.py


---

🌐 Example Workflow

1. A user types:

+vouch @User123 Great trader!

→ RepuBot stores it as pending and sends it to the log channel.


2. An admin reviews and approves with:

/approve <vouch_id>

→ RepuBot marks it approved and updates reputation.


3. Users can check vouches with:

+rep @User123




---

🎨 Design

Embed Color: #3498db

Footer: RepuBot • Building Reputation

Log messages are neat, rich embeds sent to a per-server configured channel.



---

🛠️ Tech Stack

Python 3.12+

discord.py v2.4.0

MongoDB (pymongo)

dotenv (for security)



---

💡 Future Improvements

Web dashboard to view/manage vouches

Reputation-based level roles

Export vouch data as CSV

Auto-notify when users reach milestones



---

📜 License

This project is open-source and available for personal use under the MIT License.
Please credit RepuBot if you fork or modify it.


---
