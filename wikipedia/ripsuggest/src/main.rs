use std::{collections::{HashMap, HashSet, VecDeque}, env, fs, sync::OnceLock};

use axum::{Json, Router, routing::{get, post}};
use rand::{random_bool, rng, seq::IteratorRandom};
use serde::{Deserialize, Serialize};
use tokio::{net::TcpListener, time::Instant};

#[derive(Deserialize)]
struct Req {
    source: String,
    dest: String
}

#[derive(Serialize)]
struct Res {
    #[serde(skip_serializing_if = "Option::is_none")]
    path: Option<Vec<String>>
}

static RELATIONS: OnceLock<HashMap<String, HashSet<String>>> = OnceLock::new();
static RELATIONS_REV: OnceLock<HashMap<String, HashSet<String>>> = OnceLock::new();

fn bfs(source: &str, dest: &str) -> Option<Vec<String>> {
    let relations = RELATIONS.get().unwrap();
    let relations_rev = RELATIONS_REV.get().unwrap();
    let mut queue = VecDeque::from([(vec![], source)]);
    let mut visited = HashSet::from([source]);

    while let Some((mut path, node)) = queue.pop_front() {
        path.push(node);

        if node == dest {
            return Some(path.into_iter().map(str::to_string).collect())
        }

        if let Some(neighbours) = relations.get(node){
            for neighbour in neighbours {
                if visited.insert(neighbour) {
                    queue.push_back((path.clone(), neighbour));
                }
            }
        }

        if let Some(neighbours) = relations_rev.get(node){
            for neighbour in neighbours {
                if visited.insert(neighbour) {
                    queue.push_back((path.clone(), neighbour));
                }
            }
        }
    }

    None
}

#[tokio::main]
async fn main() {
    let port = env::var("PORT")
        .map(|s| s.parse::<u16>().unwrap())
        .unwrap_or(8080);

    println!("Loading up cache.txt");
    let mut relations: HashMap<String, HashSet<String>> = HashMap::new();
    let mut relations_rev: HashMap<String, HashSet<String>> = HashMap::new();

    for line in fs::read_to_string("../graphgen/cache.txt").unwrap().lines() {
        let mut chunks = line.split('|');
        let current = chunks.next().unwrap().to_string();

        relations.insert(current.clone(), HashSet::from_iter(chunks.map(str::to_string)));

        for chunk in line.split('|').skip(1) {
            if random_bool(0.95) {
                continue;
            }
            relations_rev.entry(chunk.to_string()).or_insert(HashSet::new()).insert(current.clone());
        }
    }

    RELATIONS.set(relations).unwrap();
    RELATIONS_REV.set(relations_rev).unwrap();

    let nodes = RELATIONS.get().unwrap().keys();
    let chosen = nodes.choose_multiple(&mut rng(), 2000);

    for i in 0..1000 {
        let instant = Instant::now();
        println!("{:?} in {}ms", bfs(chosen[2 * i], chosen[2 * i + 1]), instant.elapsed().as_millis())
    }

    let app = Router::new()
        .route("/nodelist", get(|| async move {
            RELATIONS.get().unwrap().keys().cloned().collect::<Vec<_>>().join("\n")
        }))
        .route("/getpath", post(|content: Json<Req>| async move {
            let relations = RELATIONS.get().unwrap();

            if !(relations.contains_key(&content.source) && relations.contains_key(&content.dest)) {
                return Json(Res { path: None })
            }

            Json(Res { path: bfs(&content.source, &content.dest) })
        }));

    let listener = TcpListener::bind(format!("127.0.0.1:{}", port))
        .await
        .unwrap();

    println!("server started");

    axum::serve(listener, app).await.unwrap();
}
