$PHRASE_FORM = $('#add-phrase-form')
$FISH_COUNT = $('#fish-count')

$PHRASE_FORM.on("submit", updatePhraseCount)

let count = 0;

function updatePhraseCount() {
  count++;
  $FISH_COUNT.text(count)
}