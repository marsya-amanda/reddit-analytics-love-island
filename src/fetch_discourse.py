import requests
import json
import time
import re
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

discussion_threads = {
    'Episode 1': 'https://www.reddit.com/r/LoveIslandAus/comments/1oh7qjr/season_7_episode_1_monday_27th_october_discussion/',
    'Episode 2': 'https://www.reddit.com/r/LoveIslandAus/comments/1oi2o1h/season_7_episode_2_tuesday_28th_october/',
    'Episode 3': 'https://www.reddit.com/r/LoveIslandAus/comments/1oixqgp/season_7_episode_3_wednesday_29th_october/',
    'Episode 4': 'https://www.reddit.com/r/LoveIslandAus/comments/1ojsw3h/season_7_episode_4_thursday_30th_october/',
    'Episode 5': 'https://www.reddit.com/r/LoveIslandAus/comments/1on54g0/season_7_episode_5_monday_3rd_november_discussion/',
    'Episode 6': 'https://www.reddit.com/r/LoveIslandAus/comments/1oo0t3m/season_7_episode_6_tuesday_4th_november/',
    'Episode 7': 'https://www.reddit.com/r/LoveIslandAus/comments/1oow4zt/season_7_episode_7_wednesday_5th_november/',
    'Episode 8': 'https://www.reddit.com/r/LoveIslandAus/comments/1ops685/season_7_episode_8_thursday_6th_november/',
    'Episode 9': 'https://www.reddit.com/r/LoveIslandAus/comments/1ot77p5/season_7_episode_9_monday_10th_november/',
    'Episode 10': 'https://www.reddit.com/r/LoveIslandAus/comments/1ou2t22/season_7_episode_10_tuesday_11th_november/',
    'Episode 11': 'https://www.reddit.com/r/LoveIslandAus/comments/1ouyeow/season_7_episode_11_wednesday_12th_november/',
    'Episode 12': 'https://www.reddit.com/r/LoveIslandAus/comments/1ovugzx/season_7_episode_12_thursday_13th_november/',
    'Episode 13': 'https://www.reddit.com/r/LoveIslandAus/comments/1oz2or4/season_7_episode_13_monday_17th_november/',
    'Episode 14': 'https://www.reddit.com/r/LoveIslandAus/comments/1ozy5xz/season_7_episode_14_tuesday_18th_november/',
    'Episode 15': 'https://www.reddit.com/r/LoveIslandAus/comments/1p0tnvk/season_7_episode_15_wednesday_19th_november/',
    'Episode 16': 'https://www.reddit.com/r/LoveIslandAus/comments/1p1pkd2/season_7_episode_16_thursday_20th_november/',
    'Episode 17': 'https://www.reddit.com/r/LoveIslandAus/comments/1p53ezh/season_7_episode_17_monday_24th_november/',
    'Episode 18': 'https://www.reddit.com/r/LoveIslandAus/comments/1p5yvxu/season_7_episode_18_tuesday_25th_november/',
    'Episode 19': 'https://www.reddit.com/r/LoveIslandAus/comments/1p6u4jb/season_7_episode_19_wednesday_26th_november/',
    'Episode 20': 'https://www.reddit.com/r/LoveIslandAus/comments/1p7ox2x/season_7_episode_20_thursday_27th_november/',
}


def fetch_comments_from_reddit_json(url, max_comments=100):
    """
    Fetch comments using Reddit's JSON API (more reliable than HTML scraping).
    Returns list of comments sorted by score (top comments first).
    """
    # Use Reddit's JSON API
    json_url = url.rstrip('/') + '.json'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(json_url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        comments = []
        
        # Reddit JSON structure: [0] is the post, [1] is comments
        if len(data) >= 2 and 'data' in data[1]:
            comments_data = data[1]['data']['children']
            
            def extract_comments(children, depth=0):
                """Recursively extract comments from nested structure"""
                extracted = []
                for item in children:
                    if item.get('kind') == 't1':  # t1 = comment
                        comment_data = item.get('data', {})
                        comment = {
                            'id': comment_data.get('id'),
                            'author': comment_data.get('author'),
                            'body': comment_data.get('body', ''),
                            'score': comment_data.get('score', 0),
                            'created_utc': comment_data.get('created_utc'),
                            'permalink': f"https://www.reddit.com{comment_data.get('permalink', '')}",
                            'depth': depth
                        }
                        extracted.append(comment)
                        
                        # Recursively get replies
                        if comment_data.get('replies') and isinstance(comment_data['replies'], dict):
                            if 'data' in comment_data['replies']:
                                extracted.extend(extract_comments(
                                    comment_data['replies']['data']['children'], 
                                    depth + 1
                                ))
                return extracted
            
            all_comments = extract_comments(comments_data)
            
            # Sort by score (highest first) and take top N
            all_comments.sort(key=lambda x: x['score'], reverse=True)
            comments = all_comments[:max_comments]
        
        return comments
        
    except Exception as e:
        print(f"Error fetching JSON: {e}")
        return []


def fetch_comments_with_beautifulsoup(url, max_comments=100):
    """
    Fetch comments using BeautifulSoup (for old.reddit.com which is more scrapeable).
    Falls back to JSON API if BeautifulSoup approach fails.
    """
    # Convert to old.reddit.com for easier scraping
    old_reddit_url = url.replace('www.reddit.com', 'old.reddit.com')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(old_reddit_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comments = []
        
        # Find comment entries (old Reddit structure)
        comment_entries = soup.find_all('div', class_='comment')
        
        for entry in comment_entries[:max_comments]:
            try:
                # Extract comment text
                comment_body = entry.find('div', class_='usertext-body')
                body_text = comment_body.get_text(strip=True) if comment_body else ''
                
                # Extract author
                author_tag = entry.find('a', class_='author')
                author = author_tag.get_text(strip=True) if author_tag else '[deleted]'
                
                # Extract score
                score_tag = entry.find('span', class_='score')
                score_text = score_tag.get_text(strip=True) if score_tag else '0'
                # Parse score (handles "123 points" or just "123")
                score = 0
                if score_text and score_text != '•':
                    score_match = re.search(r'(\d+)', score_text.replace(',', ''))
                    if score_match:
                        score = int(score_match.group(1))
                
                # Extract permalink
                permalink_tag = entry.find('a', class_='bylink')
                permalink = permalink_tag.get('href', '') if permalink_tag else ''
                if permalink and not permalink.startswith('http'):
                    permalink = f"https://old.reddit.com{permalink}"
                
                comment = {
                    'id': entry.get('data-fullname', '').replace('t1_', ''),
                    'author': author,
                    'body': body_text,
                    'score': score,
                    'created_utc': None,  # Hard to extract from HTML
                    'permalink': permalink,
                    'depth': 0  # Would need to calculate from nesting
                }
                
                if body_text:  # Only add if comment has text
                    comments.append(comment)
                    
            except Exception as e:
                print(f"Error parsing comment: {e}")
                continue
        
        # Sort by score and take top N
        comments.sort(key=lambda x: x['score'], reverse=True)
        return comments[:max_comments]
        
    except Exception as e:
        print(f"BeautifulSoup scraping failed: {e}")
        print("Falling back to JSON API...")
        return fetch_comments_from_reddit_json(url, max_comments)


def fetch_all_episode_comments(output_dir='../data/comments', max_comments=100):
    """
    Fetch top comments from all discussion threads and save to JSON files.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for episode_name, url in discussion_threads.items():
        # Extract episode number
        episode_num = int(re.search(r'Episode (\d+)', episode_name).group(1))
        
        print(f"Fetching comments for {episode_name}...")
        
        # Try BeautifulSoup first, fallback to JSON API
        comments = fetch_comments_with_beautifulsoup(url, max_comments)
        
        if not comments:
            # If BeautifulSoup fails, use JSON API directly
            comments = fetch_comments_from_reddit_json(url, max_comments)
        
        # Prepare output data
        output_data = {
            'episode': episode_name,
            'episode_number': episode_num,
            'url': url,
            'fetched_at': datetime.now().isoformat(),
            'total_comments_fetched': len(comments),
            'comments': comments
        }
        
        # Save to JSON file
        output_file = output_path / f"comments_episode_{episode_num}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Saved {len(comments)} comments to {output_file}")
        
        # Be respectful with rate limiting
        time.sleep(2)
    
    print("\n✓ All episodes processed!")


if __name__ == "__main__":
    fetch_all_episode_comments(max_comments=100)
