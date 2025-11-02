import express = require('express')
const app = express()
const port = process.env.PORT ?? 8083

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

app.use(express.static('static'))
