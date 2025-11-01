use std::{collections::HashSet, fs};

fn count_words(s: &str) -> u32 {
    let mut prev_is_lower = true;

    s.chars().filter(|c| {
        if c.is_ascii_uppercase() && prev_is_lower {
            prev_is_lower = false;
            true
        } else {
            prev_is_lower = c.is_ascii_lowercase();
            false
        }
    }).count() as u32
}

fn main() {
    let buf = fs::read_to_string("/home/siriusmart/Downloads/vital.txt").unwrap();
    let buf = buf.lines().flat_map(|s| {
        s.split_whitespace().filter(|s| {
            s.starts_with("[[") && s.trim().ends_with("]]")
        })
    });

    let out = buf
        .map(|s| &s[2..s.len() - 2])
        .filter(|s| count_words(&s) <= 1)
        .filter(|s| s.chars().filter(|c| c.is_ascii_uppercase()).count() == 1 && s.chars().next().is_some_and(|c| c.is_ascii_uppercase()))
        .filter(|s| s.len() < 9 && s.len() > 4)
        .filter(|s| s.chars().all(|c| c.is_ascii_alphabetic()))
        .map(str::to_string);

    let s: HashSet<String> = HashSet::from_iter(out);

    fs::write("words.txt", Vec::from_iter(s.into_iter()).join("\n")).unwrap();
}
