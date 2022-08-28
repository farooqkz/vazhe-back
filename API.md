## Word defintion

Mandatory fields:

 - `id`(`int`): ID of the word. Starting with zero(auto assigned when creating a word)
 - `word`(`str`): Word in the local language
 - `word_fa`(`str`): Word meaning in Persian language

Optional fields:

 - `pron_eng`(`str`): Pronounciation in English.
 - `pron_per`(`str`): Pronounciation hint in Persian.
 - `origin`(`str`): Origin of this word.
 - `usages`(`array[str]`): Usages in a sentence.

## POST `/words`
### Rate limited(1/s)

Create a new word(req. body: word defintion).

## PUT `/words/<id>`
### Rate limited(1/s)

Modify the word with ID `<id>`. Any supplied field will be set to this, except `id` and `word`

## GET `/words/<page>/<rows_num>`

Get the page `<page>` with `<rows_num>` rows in each page.

## GET `/words/pdf`

Get a PDF dump of all words in database.

## GET `/words/json`

Get a JSON dump of all words in the database.
