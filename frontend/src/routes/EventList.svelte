<script>
  import * as api from "../api";
  import { onMount } from "svelte";
  import EventItem from "../components/EventItem.svelte";

  let events;

  onMount(async () => {
    await api.listEvents()
       .then(data => {
       	console.log(data)
         events = data['results'];
       });
   })
  
</script>
<main>
  <h1>Recent events</h1>

  {#if events}
  <ul>
  {#each events as event }
      <li>
        <EventItem {event} />
      </li>
  {/each}
  </ul>
  {:else}
  <p class="loading">loading...</p>
  {/if}
</main>

