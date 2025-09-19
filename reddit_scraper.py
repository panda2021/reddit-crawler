#!/usr/bin/env python3
"""
Reddit Thread Scraper using PRAW
A Python script to scrape Reddit threads and their comments.
"""

import praw
import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
import argparse


class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize the Reddit scraper with credentials.
        
        Args:
            client_id: Reddit app client ID
            client_secret: Reddit app client secret
            user_agent: User agent string for the bot
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
    def scrape_thread(self, thread_url: str) -> Dict[str, Any]:
        """
        Scrape a single Reddit thread and its comments.
        
        Args:
            thread_url: URL of the Reddit thread to scrape
            
        Returns:
            Dictionary containing post data and comments
        """
        try:
            submission = self.reddit.submission(url=thread_url)
            
            # Get post data
            post_data = {
                'title': submission.title,
                'author': submission.author.name if submission.author else '[deleted]',
                'text': submission.selftext,
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'num_comments': submission.num_comments,
                'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                'url': submission.url,
                'permalink': f"https://reddit.com{submission.permalink}",
                'subreddit': str(submission.subreddit)
            }
            
            # Get all comments
            submission.comments.replace_more(limit=None)
            comments = []
            
            for comment in submission.comments.list():
                if not isinstance(comment, praw.models.MoreComments):
                    comment_data = {
                        'author': comment.author.name if comment.author else '[deleted]',
                        'body': comment.body,
                        'score': comment.score,
                        'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat(),
                        'permalink': f"https://reddit.com{comment.permalink}",
                        'is_submitter': comment.is_submitter,
                        'parent_id': comment.parent_id
                    }
                    comments.append(comment_data)
            
            return {
                'post': post_data,
                'comments': comments,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping {thread_url}: {e}")
            return None
    
    def print_thread_data(self, data: Dict[str, Any]):
        """Print thread data to console in a readable format."""
        if not data:
            return
            
        post = data['post']
        comments = data['comments']
        
        print("=" * 80)
        print("REDDIT THREAD SCRAPER RESULTS")
        print("=" * 80)
        print(f"\n--- POST ---")
        print(f"Title: {post['title']}")
        print(f"Author: {post['author']}")
        print(f"Subreddit: r/{post['subreddit']}")
        print(f"Score: {post['score']} (Upvote Ratio: {post['upvote_ratio']})")
        print(f"Comments: {post['num_comments']}")
        print(f"Created: {post['created_utc']}")
        print(f"URL: {post['url']}")
        print(f"Text: {post['text']}")
        
        print(f"\n--- COMMENTS ({len(comments)}) ---")
        for i, comment in enumerate(comments, 1):
            print(f"\nComment {i}:")
            print(f"Author: {comment['author']}")
            print(f"Score: {comment['score']}")
            print(f"Created: {comment['created_utc']}")
            print(f"Text: {comment['body']}")
            print("-" * 40)
    
    def save_to_json(self, data: Dict[str, Any], filename: str):
        """Save scraped data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def save_to_csv(self, data: Dict[str, Any], filename: str):
        """Save scraped data to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write post data
            writer.writerow(['Type', 'Author', 'Content', 'Score', 'Created', 'URL'])
            post = data['post']
            writer.writerow([
                'POST',
                post['author'],
                f"{post['title']}\n\n{post['text']}",
                post['score'],
                post['created_utc'],
                post['permalink']
            ])
            
            # Write comments
            for comment in data['comments']:
                writer.writerow([
                    'COMMENT',
                    comment['author'],
                    comment['body'],
                    comment['score'],
                    comment['created_utc'],
                    comment['permalink']
                ])
        
        print(f"Data saved to {filename}")
    
    def scrape_multiple_threads(self, urls: List[str], output_format: str = 'console'):
        """
        Scrape multiple Reddit threads.
        
        Args:
            urls: List of Reddit thread URLs
            output_format: Output format ('console', 'json', 'csv', 'both')
        """
        all_data = []
        
        for i, url in enumerate(urls, 1):
            print(f"\nScraping thread {i}/{len(urls)}: {url}")
            data = self.scrape_thread(url)
            
            if data:
                all_data.append(data)
                
                if output_format in ['console', 'both']:
                    self.print_thread_data(data)
                
                if output_format in ['json', 'both']:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    json_filename = f"reddit_data_{i}_{timestamp}.json"
                    self.save_to_json(data, json_filename)
                
                if output_format in ['csv', 'both']:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    csv_filename = f"reddit_data_{i}_{timestamp}.csv"
                    self.save_to_csv(data, csv_filename)
        
        # Save combined data if multiple threads
        if len(all_data) > 1:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format in ['json', 'both']:
                combined_json = f"reddit_data_combined_{timestamp}.json"
                self.save_to_json(all_data, combined_json)
            
            if output_format in ['csv', 'both']:
                combined_csv = f"reddit_data_combined_{timestamp}.csv"
                with open(combined_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Thread', 'Type', 'Author', 'Content', 'Score', 'Created', 'URL'])
                    
                    for thread_idx, data in enumerate(all_data, 1):
                        post = data['post']
                        writer.writerow([
                            f"Thread {thread_idx}",
                            'POST',
                            post['author'],
                            f"{post['title']}\n\n{post['text']}",
                            post['score'],
                            post['created_utc'],
                            post['permalink']
                        ])
                        
                        for comment in data['comments']:
                            writer.writerow([
                                f"Thread {thread_idx}",
                                'COMMENT',
                                comment['author'],
                                comment['body'],
                                comment['score'],
                                comment['created_utc'],
                                comment['permalink']
                            ])
                
                print(f"Combined data saved to {combined_csv}")


def load_config():
    """Load configuration from config.json file."""
    config_file = 'config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        print("Config file not found. Please create config.json with your Reddit credentials.")
        return None


def main():
    parser = argparse.ArgumentParser(description='Reddit Thread Scraper')
    parser.add_argument('--urls', nargs='+', help='Reddit thread URLs to scrape')
    parser.add_argument('--format', choices=['console', 'json', 'csv', 'both'], 
                       default='console', help='Output format')
    parser.add_argument('--config', default='config.json', help='Config file path')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    if not config:
        return
    
    # Initialize scraper
    scraper = RedditScraper(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent=config['user_agent']
    )
    
    # Default URLs if none provided
    if not args.urls:
        urls = [
            "https://www.reddit.com/r/learnprogramming/comments/11fkexd/trying_to_extract_reddit_thread_contents_with/",
            "https://www.reddit.com/r/AskReddit/comments/119m3k1/how_to_export_comments_from_reddit/"
        ]
    else:
        urls = args.urls
    
    # Scrape threads
    scraper.scrape_multiple_threads(urls, args.format)


if __name__ == "__main__":
    main()