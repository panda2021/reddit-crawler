# Reddit Thread Scraper

A Python bot using PRAW (Python Reddit API Wrapper) to scrape Reddit threads and their comments. This tool allows you to extract post data and comments from Reddit threads and save them in various formats.

## Features

- Scrape Reddit threads and all their comments
- Export data to JSON, CSV, or console output
- Handle multiple threads at once
- Secure credential management
- Detailed post and comment metadata
- Error handling and logging

## Prerequisites

- Python 3.6 or higher
- A Reddit account
- Reddit app credentials (see setup instructions below)

## Setup Instructions

### 1. Register a Reddit App

Before using this bot, you need to register a Reddit application:

1. Log into your Reddit account
2. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
3. Click "create an app" or "create another app"
4. Fill in the form:
   - **Name**: Give your app a name (e.g., "My Comment Bot")
   - **App type**: Select "script"
   - **Description**: Optional description
   - **About URL**: Leave blank or add a URL
   - **Redirect URI**: Use `http://localhost:8080` (this is just a placeholder)
5. Click "create app"
6. **Important**: Copy down your `client_id` (the string under "personal use script") and `client_secret`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials

1. Copy the template configuration file:
   ```bash
   cp config.json.template config.json
   ```

2. Edit `config.json` and replace the placeholder values:
   ```json
   {
     "client_id": "your_actual_client_id_here",
     "client_secret": "your_actual_client_secret_here",
     "user_agent": "Comment Extraction Bot by u/YOUR_REDDIT_USERNAME"
   }
   ```

   **Important**: Replace `YOUR_REDDIT_USERNAME` with your actual Reddit username.

### 4. Security Note

- Never commit your `config.json` file to version control
- Keep your credentials secure and private
- The `config.json` file is already included in `.gitignore` (if you're using git)

## Usage

### Basic Usage

Run the script with default Reddit threads:
```bash
python reddit_scraper.py
```

### Scrape Specific Threads

```bash
python reddit_scraper.py --urls "https://www.reddit.com/r/learnprogramming/comments/example/" "https://www.reddit.com/r/AskReddit/comments/example/"
```

### Export to Different Formats

**Console output only (default):**
```bash
python reddit_scraper.py --format console
```

**Export to JSON:**
```bash
python reddit_scraper.py --format json
```

**Export to CSV:**
```bash
python reddit_scraper.py --format csv
```

**Export to both JSON and CSV:**
```bash
python reddit_scraper.py --format both
```

### Command Line Options

- `--urls`: Space-separated list of Reddit thread URLs to scrape
- `--format`: Output format (`console`, `json`, `csv`, or `both`)
- `--config`: Path to config file (default: `config.json`)

## Output Data Structure

### JSON Output

The JSON output includes:

```json
{
  "post": {
    "title": "Post title",
    "author": "username",
    "text": "Post content",
    "score": 123,
    "upvote_ratio": 0.95,
    "num_comments": 45,
    "created_utc": "2023-01-01T12:00:00",
    "url": "https://...",
    "permalink": "https://reddit.com/r/subreddit/comments/...",
    "subreddit": "subreddit_name"
  },
  "comments": [
    {
      "author": "username",
      "body": "Comment text",
      "score": 10,
      "created_utc": "2023-01-01T12:05:00",
      "permalink": "https://reddit.com/r/subreddit/comments/...",
      "is_submitter": false,
      "parent_id": "t1_..."
    }
  ],
  "scraped_at": "2023-01-01T12:10:00"
}
```

### CSV Output

The CSV output includes columns:
- Thread (for multiple threads)
- Type (POST or COMMENT)
- Author
- Content
- Score
- Created
- URL

## File Outputs

When using JSON or CSV export, files are saved with timestamps:
- `reddit_data_1_20230101_120000.json` - Individual thread data
- `reddit_data_combined_20230101_120000.json` - Combined data from all threads
- `reddit_data_1_20230101_120000.csv` - Individual thread data
- `reddit_data_combined_20230101_120000.csv` - Combined data from all threads

## Error Handling

The script includes comprehensive error handling:
- Invalid URLs are skipped with error messages
- Network issues are handled gracefully
- Missing credentials are detected and reported
- Deleted posts/comments are handled appropriately

## Rate Limiting

Reddit has rate limits for API requests. The script respects these limits automatically through PRAW. For heavy usage:
- Consider adding delays between requests
- Monitor your API usage
- Be respectful of Reddit's resources

## Troubleshooting

### Common Issues

1. **"Config file not found"**
   - Make sure you've created `config.json` from the template
   - Check that the file is in the same directory as the script

2. **"Invalid credentials"**
   - Verify your `client_id` and `client_secret` are correct
   - Make sure you're using the "personal use script" ID, not the app name

3. **"User agent required"**
   - Ensure your `user_agent` string is properly formatted
   - Include your Reddit username in the user agent

4. **"Thread not found"**
   - Verify the Reddit URL is correct and accessible
   - Some threads may be private or deleted

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your Reddit app credentials
3. Test with a simple, public Reddit thread first
4. Check Reddit's API status if you're getting unexpected errors

## Legal and Ethical Considerations

- Respect Reddit's Terms of Service
- Don't scrape private or restricted content
- Be mindful of rate limits and Reddit's resources
- Consider the privacy of users whose content you're scraping
- Use scraped data responsibly and ethically

## License

This project is provided as-is for educational and personal use. Please ensure compliance with Reddit's Terms of Service and applicable laws when using this tool.