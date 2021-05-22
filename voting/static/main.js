var ripple = document.querySelectorAll(".ripple, .mdc-ripple-surface");
ripple.forEach(element => {
	mdc.ripple.MDCRipple.attachTo(element);
});

var candidateCards = document.querySelectorAll('.voting-option');
candidateCards.forEach(card => {
	card.addEventListener("click", e => {
		card.querySelector('.voting-option__input').checked = true;
		try {
			document.querySelector('.selected').classList.remove('selected');
		}
		catch {}
		card.classList.add('selected');
	});
});