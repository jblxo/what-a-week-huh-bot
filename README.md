### "What a week, huh? Captain, it's Wednesday"

This is a simple Telegram Python-based meme bot that primarily sends the _"what a week, huh?"_ meme to your Telegram room **every Wednesday** (default at 11:11 in the Europe/Berlin timezone), and also sends a **wake-up video on the first day of each month** (default at 07:00 in the same timezone).

The bot uses threading and job scheduling within the script, so no cron job setup is required.

The repository is dockerized, and the only required runtime environment is the `TELEGRAM_BOT_TOKEN`.

### Environment variables

- `TELEGRAM_BOT_TOKEN` (required): Telegram bot token.
- `SCHEDULE_TZ` (optional, default: `Europe/Berlin`): Timezone used for all scheduled jobs.
- `WEDNESDAY_PHOTO_TIME` (optional, default: `11:11`): Time of day to send the Wednesday photo.
- `FIRST_OF_MONTH_VIDEO_TIME` (optional, default: `07:00`): Time of day to send the first-of-month video.

Example configuration:

```bash
export TELEGRAM_BOT_TOKEN="<your-token>"
export SCHEDULE_TZ="Europe/Prague"
export WEDNESDAY_PHOTO_TIME="11:11"
export FIRST_OF_MONTH_VIDEO_TIME="07:00"
```
