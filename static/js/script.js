document.addEventListener('DOMContentLoaded', e=>{
	const form = document.getElementById('form');
	form.addEventListener('submit', event=>{
		submit_btn = form['submit'];
		submit_btn.innerHTML = 'Processing..'
		submit_btn.disabled = true;
		event.submit();
	})
})
