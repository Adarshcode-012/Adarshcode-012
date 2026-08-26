from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'leetcode.json'
USERNAME = 'Adarsh_jai12'
ENDPOINT = 'https://leetcode.com/graphql'
QUERY = '''
query userProfileCalendar($username: String!, $year: Int) {
  matchedUser(username: $username) {
    username
    profile { realName ranking }
    submitStatsGlobal {
      acSubmissionNum { difficulty count submissions }
      totalSubmissionNum { difficulty count submissions }
    }
    userCalendar(year: $year) {
      activeYears
      streak
      totalActiveDays
      dccBadges { timestamp badge { name icon } }
      submissionCalendar
    }
  }
}
'''

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (compatible; Adarshcode-012 profile generator)',
    'Referer': 'https://leetcode.com/',
}

def fetch(year=None):
    r = requests.post(ENDPOINT, json={
        'query': QUERY,
        'variables': {'username': USERNAME, 'year': year},
        'operationName': 'userProfileCalendar',
    }, headers=headers, timeout=30)
    r.raise_for_status()
    payload = r.json()
    if payload.get('errors'):
        raise RuntimeError(payload['errors'])
    user = payload.get('data', {}).get('matchedUser')
    if not user:
        raise RuntimeError(f'LeetCode user not found: {USERNAME}')
    return user

# Fetch the rolling calendar without hard-coding a year; LeetCode's calendar
# endpoint returns the active contribution window when year is omitted.
user = fetch()
calendar = user['userCalendar']
raw = json.loads(calendar.get('submissionCalendar') or '{}')
now = datetime.now(timezone.utc)
cutoff = now - timedelta(days=365)

days = []
for ts, count in raw.items():
    dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
    if dt >= cutoff:
        days.append({'date': dt.date().isoformat(), 'count': int(count)})
days.sort(key=lambda x: x['date'])

stats = {'easy': 0, 'medium': 0, 'hard': 0, 'total_solved': 0}
for item in user.get('submitStatsGlobal', {}).get('acSubmissionNum', []):
    d = item['difficulty'].lower()
    if d in stats:
        stats[d] = int(item['count'])
stats['total_solved'] = stats['easy'] + stats['medium'] + stats['hard']

# Total submissions in the same rolling window.
total_submissions = sum(d['count'] for d in days)

result = {
    'username': user.get('username', USERNAME),
    'real_name': (user.get('profile') or {}).get('realName', 'Adarsh Jaiswal'),
    'ranking': (user.get('profile') or {}).get('ranking'),
    'fetched_at': now.isoformat(),
    'window_days': 365,
    'stats': {
        **stats,
        'submissions': total_submissions,
        'active_days': calendar.get('totalActiveDays', len(days)),
        'streak': calendar.get('streak', 0),
    },
    'days': days,
}
OUT.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(f'Wrote {OUT}: {len(days)} active dates, {total_submissions} submissions')
