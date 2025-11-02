import express = require('express')
const app = express()
const port = process.env.PORT ?? 8083

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

app.use(express.static('static'))

/*
GET /api/newgame
Request: empty
Response: { code: string }

GET /api/guess?code=string&guess=string&round=int
Request: { code: string, guess: string, round: int } (round is 1 to 5)
Response: { code: string }

/api/wordlist
Request: empty
Response: { words: string[] }
*/
