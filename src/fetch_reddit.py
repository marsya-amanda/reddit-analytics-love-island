import requests
import json
import time
from datetime import datetime

def scrape_reddit_episodes(start_date="2025-10-27", output_file="reddit_episodes.json"):
    """
    Scrapes r/LoveIslandAus for posts containing 'episode' keyword.
    
    Args:
        start_date: Start date in YYYY-MM-DD format (default: 2025-10-27)
        output_file: Output JSON file path
    
    Returns:
        dict: Dictionary containing scraped posts and metadata
    """
    subreddit = "LoveIslandAus"
    keyword = "episode"
    
    # Convert start date to Unix timestamp
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    start_timestamp = int(start_datetime.timestamp())
    current_timestamp = int(time.time())
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_posts = []
    after = None  # For pagination
    
    print(f"Scraping r/{subreddit} for posts containing '{keyword}'...")
    print(f"Date range: {start_date} to now")
    
    while True:
        # Reddit search URL - sorted by new (most recent first) https://www.reddit.com/r/LoveIslandAus/search/?q=episode&type=posts&sort=new&cId=21f8c4a1-2283-4312-b2ca-c8e3948f96bc&iId=44175f6d-521e-48d0-abef-a800e05bfc22
        if after:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&type=posts&sort=new&restrict_sr=1&limit=100&after={after}"
        else:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&type=posts&sort=new&restrict_sr=1&limit=100"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = data.get('data', {}).get('children', [])
            
            if not posts:
                break
            
            batch_filtered = []
            for post in posts:
                post_data = post.get('data', {})
                created_utc = post_data.get('created_utc', 0)
                
                # Filter by date range
                if start_timestamp <= created_utc <= current_timestamp:
                    post_info = {
                        'id': post_data.get('id'),
                        'title': post_data.get('title'),
                        'author': post_data.get('author'),
                        'created_utc': created_utc,
                        'created_date': datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'url': post_data.get('url'),
                        'permalink': f"https://www.reddit.com{post_data.get('permalink', '')}",
                        'selftext': post_data.get('selftext', '')[:500]  # First 500 chars
                    }
                    batch_filtered.append(post_info)
                elif created_utc < start_timestamp:
                    # If we've gone past the start date, we can stop
                    # (since results are sorted by new, most recent first)
                    break
            
            all_posts.extend(batch_filtered)
            
            # Check if we've gone past the start date
            oldest_in_batch = min([p.get('data', {}).get('created_utc', 0) for p in posts], default=0)
            if oldest_in_batch < start_timestamp:
                break
            
            # Get pagination token
            after = data.get('data', {}).get('after')
            if not after:
                break
            
            # Be respectful with rate limiting
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            break
    
    # Sort by most recent (created_utc descending)
    all_posts.sort(key=lambda x: x['created_utc'], reverse=True)
    
    # Save to JSON
    output = {
        'subreddit': subreddit,
        'keyword': keyword,
        'date_range': {
            'start': start_date,
            'end': datetime.now().strftime('%Y-%m-%d')
        },
        'total_posts': len(all_posts),
        'posts': all_posts
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nScraping complete!")
    print(f"Found {len(all_posts)} posts")
    print(f"Results saved to {output_file}")
    
    return output


def scrape_reddit() -> list[dict]:
    """
    Legacy function for backward compatibility.
    Now calls scrape_reddit_episodes and returns the posts list.
    """
    results = scrape_reddit_episodes()
    return results.get('posts', [])


if __name__ == "__main__":
    # Scrape from October 27, 2025 to now
    results = scrape_reddit_episodes(start_date="2025-10-27", output_file="../data/reddit_episodes.json")