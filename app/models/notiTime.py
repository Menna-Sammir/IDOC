from datetime import  timedelta


def calculate_time_ago(current_time, notification_time):
    time_difference = current_time - notification_time
    if time_difference < timedelta(minutes=1):
        return 'Just now'
    elif time_difference < timedelta(hours=1):
        minutes = time_difference.seconds // 60
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif time_difference < timedelta(days=1):
        hours = time_difference.seconds // 3600
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    else:
        days = time_difference.days
        return f'{days} day{"s" if days > 1 else ""} ago'