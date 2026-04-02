use serde::Deserialize;
use clap::Parser;

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    option: String,
}

#[derive(Deserialize)]
struct Story {
    title: String,
    url: Option<String>,
    score: u32,
    by: String,
}

fn main() {
    let args = Args::parse();
    let url  = format!("https://hacker-news.firebaseio.com/v0/{}.json", args.option);

    println!("Top 10 Hacker News Stories\n");

    let client = reqwest::blocking::Client::new();

    let top_ids: Vec<u64> = client
        .get(url)
        .send()
        .expect("Failed to fetch top stories")
        .json()
        .expect("Failed to parse story IDs");

    for (i, id) in top_ids.iter().take(10).enumerate() {
        let url = format!("https://hacker-news.firebaseio.com/v0/item/{id}.json");

        let story: Story = client
            .get(&url)
            .send()
            .expect("Failed to fetch story")
            .json()
            .expect("Failed to parse story");

        let link = story.url.as_deref().unwrap_or("(no URL)");
        println!("{}. {} ({} points by {})", i + 1, story.title, story.score, story.by);
        println!("   {}\n", link);
    }
}
