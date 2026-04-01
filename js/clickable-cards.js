// Make .white-box-holder.apiapp cards fully clickable
// Navigates to the "Learn more" link href on card click
document.addEventListener('DOMContentLoaded', function() {
  document.addEventListener('click', function(e) {
    var card = e.target.closest('.white-box-holder.apiapp');
    if (!card) return;
    // Don't intercept if user clicked the link itself
    if (e.target.closest('a')) return;
    var link = card.querySelector('.button-top-margin a');
    if (link) {
      window.location.href = link.href;
    }
  });
});
