var ripple = document.querySelectorAll(".ripple");
ripple.forEach(element => {
	mdc.ripple.MDCRipple.attachTo(element);
});