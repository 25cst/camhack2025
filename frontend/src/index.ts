import assert = require('assert');
import express = require('express');
import fs = require('fs');
import path = require('path');

const app = express();
const port = process.env.PORT ?? 8083;

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
      .map(word => word.toLowerCase());
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
    
    const response: NewGameResponse = { code: targetWord };
    res.json(response);
  } catch (error) {
    console.error('Error creating new game:', error);
    res.status(500).json({ error: 'Failed to create new game' });
  }
});

app.get('/api/guess', (req, res) => {
  try {
    // Use type assertion with explicit string conversion
    const code = req.query.code as string;
    const guess = req.query.guess as string;
    const round = req.query.round as string;
    
    // Validate required parameters
    if (!code?.trim() || !guess?.trim() || !round?.trim()) {
      return res.status(400).json({ 
        error: 'Missing required parameters: code, guess, round' 
      });
    }

    const roundNum = parseInt(round);
    if (isNaN(roundNum) || roundNum < 1 || roundNum > 5) {
      return res.status(400).json({ 
        error: 'Round must be an integer between 1 and 5' 
      });
    }

    const codeLower = code.toLowerCase();
    const guessLower = guess.toLowerCase();

    if (!wordList.includes(codeLower)) {
      return res.status(400).json({ 
        error: 'Invalid target word' 
      });
    }

    if (!wordList.includes(guessLower)) {
      return res.status(400).json({ 
        error: 'Invalid guess - word not in word list' 
      });
    }

    console.log(`Guess for target "${code}": "${guess}" in round ${roundNum}`);
    
    const response: GuessResponse = { code };
    res.json(response);
  } catch (error) {
    console.error('Error processing guess:', error);
    res.status(500).json({ error: 'Failed to process guess' });
  }
});

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