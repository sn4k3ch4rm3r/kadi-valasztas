var startTime = parseInt(document.getElementById('start-time').value);
var countdown = document.getElementById('countdown');

function tick() {
	let now = Math.floor(new Date().getTime() /1000);
	let delta = startTime - now;

	if(delta <= 0) {
		window.clearInterval(timer);
		location.reload();
	}

	let hrs = Math.floor(delta/3600);
	let mins = Math.floor(delta%3600/60);
	let sec = delta%60;

	countdown.innerText = hrs.toString().padStart(2, '0') + ':' + mins.toString().padStart(2, '0') + ':' + sec.toString().padStart(2, '0');
}

if(startTime != -1) {
	timer = window.setInterval(tick, 10);
}
else {
	countdown.innerText = "Nincs beállítva."
}
