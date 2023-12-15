from datetime import datetime, timezone, timedelta

def time_ago(value):
    if isinstance(value, datetime):
        created_at = value
    else:
        created_at = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    # Replace 'php' with your actual PHP timezone
    php_timezone = timezone(timedelta(hours=8))  # Replace with your PHP timezone offset

    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    created_at = created_at.replace(tzinfo=php_timezone).astimezone(timezone.utc)

    time_difference = now - created_at

    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f'{days} {"day" if days == 1 else "days"} ago'
    elif hours > 0:
        return f'{hours} {"hour" if hours == 1 else "hours"} ago'
    elif minutes > 0:
        return f'{minutes} {"minute" if minutes == 1 else "minutes"} ago'
    else:
        return f'{seconds} {"second" if seconds == 1 else "seconds"} ago'

def get_notification_text(notif):
    notif_type = notif.get('type', '')

    if notif_type == 'POST':
        return 'created a post'
    elif notif_type == 'LIKE':
        return 'liked your post'
    elif notif_type == 'SAVE':
        return 'saved your post'
    elif notif_type == 'COMMENT':
        return 'commented on your post'
    elif notif_type == 'FOLLOW':
        return 'followed you'
    else:
        return 'performed an action'