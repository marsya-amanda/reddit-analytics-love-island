import json
import csv
import re
from datetime import datetime
from pathlib import Path

def parse_episodes_csv(episodes_csv_path):
    """Load episodes.csv and return a list of episodes with their air dates."""
    episodes = []
    with open(episodes_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            episode_num = int(row['episode_number'])
            # Parse date from format "27 October, 2025"
            air_date_str = row['air_date'].strip().strip('"')
            air_date = datetime.strptime(air_date_str, "%d %B, %Y")
            episodes.append({
                'episode_number': episode_num,
                'air_date': air_date,
                'air_date_timestamp': int(air_date.timestamp())
            })
    return sorted(episodes, key=lambda x: x['episode_number'])

def extract_episode_number_from_title(title):
    """Extract episode number from title if it contains 'Episode {X}' pattern."""
    # Look for patterns like "Episode 5", "episode 5", "Episode5", etc.
    patterns = [
        r'[Ee]pisode\s+(\d+)',
        r'[Ee]p\s+(\d+)',
        r'[Ee]pisode\s*(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    return None

def assign_post_to_episode(post, episodes, ambiguous_ranges):
    """Assign a post to an episode based on its timestamp and title."""
    post_timestamp = post['created_utc']
    post_date = datetime.fromtimestamp(post_timestamp).date()
    
    # Find which episode range the post falls into
    for i in range(len(episodes)):
        current_ep = episodes[i]
        current_ep_date = current_ep['air_date'].date()
        
        # Check if post is on the same day as current episode
        if post_date == current_ep_date:
            return current_ep['episode_number']
        
        # Check if post is between current and next episode (if next exists)
        if i < len(episodes) - 1:
            next_ep = episodes[i + 1]
            next_ep_date = next_ep['air_date'].date()
            
            # Post is after current episode date but before next episode date
            if current_ep_date < post_date < next_ep_date:
                # Check if this is an ambiguous range (4-5, 8-9, 12-13, 16-17)
                if (current_ep['episode_number'], next_ep['episode_number']) in ambiguous_ranges:
                    # Try to extract episode number from title
                    title_episode = extract_episode_number_from_title(post['title'])
                    
                    if title_episode is not None:
                        # Check if the extracted episode number matches current or next
                        if title_episode == current_ep['episode_number']:
                            return current_ep['episode_number']
                        elif title_episode == next_ep['episode_number']:
                            return next_ep['episode_number']
                        # If it matches neither, default to current (most recent aired)
                        else:
                            return current_ep['episode_number']
                    else:
                        # No episode number in title, assign to current (most recent aired)
                        return current_ep['episode_number']
                else:
                    # Not an ambiguous range, assign to current episode
                    return current_ep['episode_number']
    
    # If post is on or after the last episode date, assign to last episode
    if post_date >= episodes[-1]['air_date'].date():
        return episodes[-1]['episode_number']
    
    # If post is before the first episode, assign to first episode
    if post_date < episodes[0]['air_date'].date():
        return episodes[0]['episode_number']
    
    # Fallback (shouldn't reach here)
    return episodes[0]['episode_number']

def parse_reddit_episodes(episodes_csv_path, reddit_json_path, output_dir='data'):
    """
    Parse reddit_episodes.json and divide posts into episode-specific CSV files.
    
    Args:
        episodes_csv_path: Path to episodes.csv
        reddit_json_path: Path to reddit_episodes.json
        output_dir: Directory to save output CSV files
    """
    # Load episodes
    episodes = parse_episodes_csv(episodes_csv_path)
    print(f"Loaded {len(episodes)} episodes")
    
    # Define ambiguous ranges (episodes between which we need to check titles)
    ambiguous_ranges = [
        (4, 5),
        (8, 9),
        (12, 13),
        (16, 17)
    ]
    
    # Load Reddit posts
    with open(reddit_json_path, 'r', encoding='utf-8') as f:
        reddit_data = json.load(f)
    
    posts = reddit_data.get('posts', [])
    print(f"Loaded {len(posts)} Reddit posts")
    
    # Group posts by episode
    episode_posts = {}
    for episode in episodes:
        episode_posts[episode['episode_number']] = []
    
    # Assign each post to an episode
    for post in posts:
        episode_num = assign_post_to_episode(post, episodes, ambiguous_ranges)
        episode_posts[episode_num].append(post)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Write CSV files for each episode
    csv_fieldnames = ['id', 'title', 'author', 'created_utc', 'created_date', 
                      'score', 'num_comments', 'url', 'permalink', 'selftext']
    
    for episode_num, posts_list in episode_posts.items():
        if posts_list:  # Only create file if there are posts
            csv_filename = output_path / f"reddit_episode_{episode_num}.csv"
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_fieldnames)
                writer.writeheader()
                for post in posts_list:
                    writer.writerow(post)
            
            print(f"Created {csv_filename} with {len(posts_list)} posts")
        else:
            print(f"No posts for episode {episode_num}, skipping CSV creation")

if __name__ == "__main__":
    # Paths
    episodes_csv = "../data/episodes.csv"
    reddit_json = "../data/reddit_episodes.json"
    output_directory = "../data"
    
    parse_reddit_episodes(episodes_csv, reddit_json, output_directory)

