import assert = require('assert');
import express = require('express');
import fs = require('fs');
import path = require('path');

function generateRandomString(length: number): string {
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }
    return result;
}

const app = express();
const port = process.env.PORT ?? 8083;

let graphCache: Map<string, string> = new Map();
let codeMap: Map<string, string> = new Map()

function createGraphURL(words: string[]) {
    const baseURL = 'http://127.0.0.1:8082/graph';
    const keywords = words.map(word => `keywords=${encodeURIComponent(word)}`).join('&');
    return `${baseURL}?${keywords}`;
}

async function getGraph(words: string[]): Promise<string> {
    let res = await fetch(createGraphURL(words));
    let json = await res.json()
    assert(typeof json === "object" && json !== null)

    assert("image" in json)
    let s = json.image;
    assert(typeof s === "string")
    return s
}

// Middleware
app.use(express.json());
app.use(express.static('static'));

// Add basic CORS headers manually if needed
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Types
interface NewGameQuery {
  min?: string;
  max?: string;
}

interface NewGameResponse {
  code: string;
}

interface GuessQuery {
  code?: string;
  guess?: string;
  round?: string;
}

interface GuessResponse {
  code: string;
}

interface WordListResponse {
  words: string[];
}

// Load words from wordlist.txt
function loadWordList(): string[] {
  try {
    const wordListPath = path.join(__dirname, '../../analyzer/data/wordlist.txt');
    const data = fs.readFileSync(wordListPath, 'utf-8');
    return data.split('\n')
      .map(word => word.trim())
      .filter(word => word.length > 0)
      .filter(word => /^[a-zA-Z]+$/.test(word))
      .map(word => word);
  } catch (error) {
    console.error('Error loading word list:', error);
    return [
      'brainstorm', 'bookcase', 'football', 'headphone', 'keyboard',
      'lighthouse', 'notebook', 'rainbow', 'skateboard', 'sunflower',
      'toothbrush', 'waterfall', 'workshop', 'butterfly', 'campfire'
    ];
  }
}

const wordList = loadWordList();

// Get a random word within length range
function getRandomWord(minLength: number, maxLength: number): string {
    /*
    let words = ["Mathematics", "Physics", "JavaScript", "Internet"];
    return words[Math.floor(Math.random() * words.length)] as string;
    */
  const filteredWords = wordList.filter(word => 
    word.length >= minLength && word.length <= maxLength
  );
  
  if (filteredWords.length === 0) {
    throw new Error(`No words found in the range ${minLength}-${maxLength} characters`);
  }
  
  const randomIndex = Math.floor(Math.random() * filteredWords.length);
  let out = filteredWords[randomIndex];
  assert(out !== undefined);
  return out;
}

app.get('/api/hascode', (req, res) => {
    const code = req.query.code as string;

    return res.status(200).json({
        exists: codeMap.has(code)
    })
})

// Routes
app.get('/api/newgame', (req, res) => {
  try {
    const { min, max } = req.query as NewGameQuery;
    
    const minLength = min ? parseInt(min) : 4;
    const maxLength = max ? parseInt(max) : 10;
    
    if (isNaN(minLength) || isNaN(maxLength) || minLength < 1 || maxLength < minLength) {
      return res.status(400).json({ 
        error: 'Invalid min/max parameters. min and max must be positive integers with max >= min' 
      });
    }

    const targetWord = getRandomWord(minLength, maxLength);
    
    console.log(`New game created with target word: ${targetWord}`);

    let code = generateRandomString(6);
    codeMap.set(code, targetWord)
    
    const response: NewGameResponse = { code: code };
    res.json(response);
  } catch (error) {
    console.error('Error creating new game:', error);
    res.status(500).json({ error: 'Failed to create new game' });
  }
});

app.get('/api/guess', (req, res) => {
  try {
    // Use type assertion with explicit string conversion
    let code = req.query.code as string;
    const guess = req.query.guess as string;
    const round = req.query.round as string;
    
    // Validate required parameters
    if (!code?.trim() || !guess?.trim() || !round?.trim()) {
      return res.status(400).json({ 
        error: 'Missing required parameters: code, guess, round' 
      });
    }

    const roundNum = parseInt(round);

    const codeLower = code;
    const guessLower = guess;

    if(guess === codeMap.get(code)) {
        res.status(200).json({words: []})
        return
    }

    console.log(`Guess for target "${code}": "${guess}" in round ${roundNum}`);
    
    fetch(`http://127.0.0.1:8081/gethint?guess=${guess}&secret=${codeMap.get(code)}&n=10&hint_level=2`)
        .then((response) => response.json())
        .then((json) => {
    const response: GuessResponse = json as GuessResponse
    res.json(response);
    })
  } catch (error) {
    console.error('Error processing guess:', error);
    res.status(500).json({ error: 'Failed to process guess' });
  }
});

app.get('/api/graph', async (req, res) => {
    let { code, guesses } = req.query;
    console.log(req.query)
    if(typeof guesses === "string") {
        guesses = [ guesses ]
    }

    assert(typeof code === "string")
    let word = codeMap.get(code)
    assert(word !== undefined)
    guesses ??= []

    assert (Array.isArray(guesses))

    let imagePath = await getGraph([word.toLowerCase()].concat(guesses.map(s => `${s}`.toLowerCase())))

    res.sendFile(imagePath, (err) => {
            if (err) {
                console.error('Error sending file:', err);
                res.status(500).end();
            } else {
                console.log('Image sent:', imagePath);
            }
        });
})

app.get('/api/wordlist', (req, res) => {
  try {
    const response: WordListResponse = { words: wordList };
    res.json(response);
  } catch (error) {
    console.error('Error fetching word list:', error);
    res.status(500).json({ error: 'Failed to fetch word list' });
  }
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    totalWords: wordList.length
  });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
  console.log(`Loaded ${wordList.length} words from word list`);
});

export = app;
