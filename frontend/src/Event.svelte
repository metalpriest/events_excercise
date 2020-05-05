<script>
	export let event;
</script>

<style>
	article {
		margin: 0 0 1em 0;
	}
	h1 {
		font-size: 1.4em;
		margin: 0;
		display: block;
	}
</style>

<article>
		<h1>{event.title}</h1>
		<small>
			Owner: <b>{event.owner_name}</b>
		</small><br/>
		<small>
			Date: <b>{event.date_start}</b>
		</small><br/>
		<small>
			Participants count: <b>{event.participants_count}</b>
		</small>
</article>
